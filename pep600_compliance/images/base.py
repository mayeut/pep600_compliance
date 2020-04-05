from contextlib import contextmanager
import json
import logging
import os
import platform
import docker


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_docker_platform(machine):
    if machine in ('x86_64'):
        return 'linux/amd64'
    if machine in ('i686'):
        return 'linux/i386'
    if machine in ('aarch64'):
        return 'linux/arm64/v8'
    if machine in ('ppc64le'):
        return 'linux/ppc64le'
    if machine in ('s390x'):
        return 'linux/s390x'
    if machine in ('armv7l'):
        return 'linux/arm/v7'
    raise LookupError('No docker platform defined for {}'.format(machine))


def get_docker_platform_prefix(machine):
    if machine in ('i686'):
        return 'i386'
    if machine in ('aarch64'):
        return 'arm64v8'
    if machine in ('ppc64le'):
        return 'ppc64le'
    if machine in ('s390x'):
        return 's390x'
    if machine in ('armv7l'):
        return 'arm32v7'
    raise LookupError('No docker platform defined for {}'.format(machine))


class Base:
    def __init__(self, image, name, version, package_manager, machines=['x86_64'], skip_lib=[], python='python3'):
        self.image = image
        self.name = name
        self.version = version
        self.package_manager = package_manager
        self.machines = machines
        self.skip_lib = skip_lib
        self.python = python

    @contextmanager
    def docker_container(self, machine):
        client = docker.from_env()

        image_name = self.image
        image = None
        if machine != 'x86_64':
            image_name = get_docker_platform_prefix(machine) + '/' + image_name
            try:
                image = client.images.get(image_name)
                has_image = True
            except docker.errors.ImageNotFound:
                has_image = False
                logger.info("Pulling image %r", image_name)
                try:
                    image = client.images.pull(*image_name.split(':'))
                    logger.info("Pulled image %r", image_name)
                except:
                    image_name = self.image

        if image is None:
            try:
                image = client.images.get(image_name)
                if platform.machine() != machine:
                    raise NotImplementedError("too dangerous")
                has_image = True
            except docker.errors.ImageNotFound:
                has_image = False
                logger.info("Pulling image %r", image_name)
                image = client.images.pull(*image_name.split(':'), platform=get_docker_platform(machine))
                logger.info("Pulled image %r", image_name)

        src_folder = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'tools'))
        volumes = {
            src_folder: {'bind': '/home/pep600_compliance', 'mode': 'rw'}}

        logger.info("Starting container with image %r (%r)", image_name,
                    image.id)
        if self.name == 'opensuse' and self.version == 'tumbleweed' and machine == 'i686':
            container = client.containers.run(image.id, ['sleep', '10000'],
                                              detach=True, volumes=volumes,
                                              security_opt=[
                                                  'seccomp:unconfined'])
        else:
            container = client.containers.run(image.id, ['sleep', '10000'],
                                              detach=True, volumes=volumes)
        logger.info("Started container %s", container.id[:12])

        try:
            exit_code, output = container.exec_run(['uname', '-m'], demux=True)
            assert exit_code == 0, output[1].decode('utf-8')
            machine_started = output[0].decode('utf-8').strip()
            if machine == 'i686':
                assert machine_started in ['i686', 'x86_64']
            else:
                assert machine_started == machine, '{} vs {}'.format(
                    machine_started, machine)
            yield container
        finally:
            container.remove(force=True)
            if not has_image:
                logger.info("Removing image %r", image_name)
                client.images.remove(image.id)
                logger.info("Removed image %r", image_name)

    def _install_packages(self, container, machine, packages):
        logger.info("Installing system packages %r", packages)
        self.package_manager.install(container, machine, packages)

    def _ensure_pip(self, container):
        logger.info("Installing pip")
        exit_code, _ = container.exec_run([self.python, '-m', 'pip', '-V'])
        if exit_code == 0:
            return
        exit_code, output = container.exec_run([self.python, '-m', 'ensurepip'])
        if exit_code == 0:
            return
        exit_code, output = container.exec_run(['bash', '-c', 'curl https://bootstrap.pypa.io/get-pip.py | {}'.format(self.python)])
        assert exit_code == 0, output.decode('utf-8')

    def _install_pyelftools(self, container):
        self._ensure_pip(container)
        logger.info("Installing pyelftools")
        exit_code, output = container.exec_run([self.python, '-m', 'pip', 'install', 'pyelftools'])
        if exit_code == 0:
            return
        exit_code, output = container.exec_run([self.python, '-m', 'pip', 'install', '/home/pep600_compliance/pyelftools-0.26.tar.gz'])
        assert exit_code == 0, output.decode('utf-8')

    def _get_symbols(self, container):
        logger.info("Running symbol script")
        exit_code, output = container.exec_run(
            [self.python, '/home/pep600_compliance/calculate_symbol_versions.py',
             'manylinux2010', '/home/pep600_compliance/policy.json'] + self.skip_lib,
            demux=True
        )
        assert exit_code == 0, output[1].decode('utf-8')
        return json.loads(output[0].decode('utf-8'))

    def run_check(self, machine):
        assert machine in self.machines
        with self.docker_container(machine) as container:
            self.install_packages(container, machine)
            self._install_pyelftools(container)
            return self._get_symbols(container)
