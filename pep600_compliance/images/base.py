from contextlib import contextmanager
import json
import logging
import os
import platform
import docker
import docker.errors


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_docker_platform(machine):
    if machine == 'x86_64':
        return 'linux/amd64'
    if machine == 'i686':
        return 'linux/i386'
    if machine == 'aarch64':
        return 'linux/arm64/v8'
    if machine == 'ppc64le':
        return 'linux/ppc64le'
    if machine == 's390x':
        return 'linux/s390x'
    if machine == 'armv7l':
        return 'linux/arm/v7'
    raise LookupError(f'No docker platform defined for {machine}')


def get_docker_platform_prefix(machine):
    if machine == 'i686':
        return 'i386'
    if machine == 'aarch64':
        return 'arm64v8'
    if machine == 'ppc64le':
        return 'ppc64le'
    if machine == 's390x':
        return 's390x'
    if machine == 'armv7l':
        return 'arm32v7'
    raise LookupError(f'No docker platform defined for {machine}')


class Base:
    def __init__(
            self, image, name, version, eol, package_manager,
            machines=['x86_64'], skip_lib=[], python='python3'):
        self.image = image
        self.name = name
        self.version = version
        self.eol = eol
        self.package_manager = package_manager
        self.machines = machines
        self.skip_lib = skip_lib
        self.python = python

    @contextmanager
    def docker_container(self, machine):
        client = docker.from_env()

        image_name = self.image
        image = None
        has_image = True
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
                image = client.images.pull(
                    *image_name.split(':'),
                    platform=get_docker_platform(machine)
                )
                logger.info("Pulled image %r", image_name)

        src_folder = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'tools'))
        volumes = {
            src_folder: {'bind': '/home/pep600_compliance', 'mode': 'rw'}}

        logger.info("Starting container with image %r (%r)", image_name,
                    image.id)
        run_kwargs = {}
        if machine == 'i686' and f'{self.name}-{self.version}' in {
            'opensuse-tumbleweed', 'debian-testing', 'debian-unstable',
            'debian-experimental'}:
            run_kwargs['security_opt'] = ['seccomp:unconfined']
        container = client.containers.run(
            image.id, ['sleep', '10000'], detach=True, volumes=volumes,
            **run_kwargs
        )
        logger.info("Started container %s", container.id[:12])

        try:
            exit_code, output = container.exec_run(['uname', '-m'], demux=True)
            assert exit_code == 0, output[1].decode('utf-8')
            machine_started = output[0].decode('utf-8').strip()
            if machine == 'i686':
                assert machine_started in ['i686', 'x86_64']
            else:
                assert machine_started == machine, \
                    f'{machine_started} vs {machine}'
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

    def install_packages(self, container, machine):
        raise NotImplementedError()

    def _ensure_pip(self, container):
        logger.info("Installing pip")
        exit_code, _ = container.exec_run([self.python, '-m', 'pip', '-V'])
        if exit_code == 0:
            return
        exit_code, output = container.exec_run([self.python, '-m', 'ensurepip'])
        if exit_code == 0:
            return
        exit_code, output = container.exec_run([
            self.python, '-c',
            'import sys; print("{}.{}".format(*sys.version_info[0:2]))'
        ])
        assert exit_code == 0
        version = output.decode('utf-8').strip()
        version_url = ''
        if version in ['2.6', '2.7', '3.2', '3.3', '3.4', '3.5']:
            version_url = version + '/'
        exit_code, output = container.exec_run([
            'bash', '-exo', 'pipefail', '-c',
            f'curl -fksSL https://bootstrap.pypa.io/{version_url}get-pip.py '
            f'| {self.python}'
        ])
        assert exit_code == 0, output.decode('utf-8')
        exit_code, _ = container.exec_run([self.python, '-m', 'pip', '-V'])
        assert exit_code == 0

    def _install_pyelftools(self, container):
        self._ensure_pip(container)
        logger.info("Installing pyelftools")
        exit_code, output = container.exec_run([
            self.python, '-m', 'pip', 'install', 'pyelftools'
        ])
        if exit_code == 0:
            return
        exit_code, output = container.exec_run([
            self.python, '-m', 'pip', 'install',
            '/home/pep600_compliance/pyelftools-0.26.tar.gz'
        ])
        assert exit_code == 0, output.decode('utf-8')

    def _get_symbols(self, container):
        logger.info("Running symbol script")
        exit_code, output = container.exec_run(
            [
                self.python,
                '/home/pep600_compliance/calculate_symbol_versions.py',
                'manylinux_2_17', '/home/pep600_compliance/policy.json'
            ] + self.skip_lib,
            demux=True
        )
        assert exit_code == 0, output[1].decode('utf-8')
        return json.loads(output[0].decode('utf-8'))

    def _get_python_dependencies(self, container):
        def _get_dependencies(python_path_):
            result_ = []
            exit_code_, output_ = container.exec_run(
                ['ldd', python_path_],
                demux=True
            )
            assert exit_code_ == 0, output_[1].decode('utf-8')
            for line in output_[0].decode('utf-8').splitlines():
                lib = line.strip().split()[0]
                if lib in {'linux-gate.so.1', 'linux-vdso.so.1',
                           'libpthread.so.0', 'libdl.so.2', 'libutil.so.1',
                           'libm.so.6', 'libc.so.6', 'librt.so.1',
                           'libgcc_s.so.1'}:
                    continue
                if lib.startswith('/lib'):
                    continue
                if lib.startswith('libpython'):
                    continue
                result_.append(lib)
            return result_

        logger.info("Running python dependencies")
        if self.image in {'fedora:rawhide', 'opensuse/tumbleweed:latest',
                          'vbatts/slackware:current'}:
            logger.info("Patch ldd")
            # workaround ldd not working (in fact bash builtin 'test -r'...)
            exit_code, output = container.exec_run(
                ['sed', '-i', 's; test ; /usr/bin/test ;g', '/usr/bin/ldd'],
                demux=True
            )
            assert exit_code == 0, output[1].decode('utf-8')

        result = []
        # check self.python
        exit_code, output = container.exec_run(
            ['which', self.python],
            demux=True
        )
        assert exit_code == 0, output[1].decode('utf-8')
        python_path = output[0].decode('utf-8').strip()
        result.extend(_get_dependencies(python_path))
        if python_path.startswith('/opt/python/cp'):
            # we are on manylinux, check all versions
            exit_code, output = container.exec_run(
                ['find', '/opt/python', '-mindepth', '1', '-maxdepth', '1'],
                demux=True
            )
            assert exit_code == 0, output[1].decode('utf-8')
            for line in output[0].decode('utf-8').strip().splitlines():
                line = line.strip() + '/bin/python'
                result.extend(_get_dependencies(line))
        # check python
        exit_code, output = container.exec_run(['which', 'python'], demux=True)
        if exit_code == 0:
            python_path = output[0].decode('utf-8').strip()
            result.extend(_get_dependencies(python_path))
        # check python2
        exit_code, output = container.exec_run(['which', 'python2'], demux=True)
        if exit_code == 0:
            python_path = output[0].decode('utf-8').strip()
            result.extend(_get_dependencies(python_path))
        # check python3
        exit_code, output = container.exec_run(['which', 'python3'], demux=True)
        if exit_code == 0:
            python_path = output[0].decode('utf-8').strip()
            result.extend(_get_dependencies(python_path))
        return sorted(set(result))

    def run_check(self, machine):
        assert machine in self.machines
        with self.docker_container(machine) as container:
            self.install_packages(container, machine)
            self._install_pyelftools(container)
            extra = self._get_python_dependencies(container)
            result = self._get_symbols(container)
            result['extra'] = extra
            return result
