from pep600_compliance.images import base
from pep600_compliance.images import package_manager


class Ubuntu(base.Base):
    def __init__(self, image, machines, packages, apt_sources_update=[], ppa_list=[], python='python3'):
        name, version = image.split(':')
        self._packages = packages
        super().__init__(image, name, version, package_manager.APT(run_once=apt_sources_update, ppa_list=ppa_list), machines=machines, python=python)

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


UBUNTU_APT_OLD = [
    ['sed', '-i', 's,archive.ubuntu.com,old-releases.ubuntu.com,g', '/etc/apt/sources.list'],
    ['sed', '-i', 's,security.ubuntu.com,old-releases.ubuntu.com,g', '/etc/apt/sources.list'],
    ['sed', '-i', 's,ports.ubuntu.com/ubuntu-ports,old-releases.ubuntu.com/ubuntu,g', '/etc/apt/sources.list'],
]
UBUNTU_PYTHON_PPA = [
    'ppa:fkrull/deadsnakes'
]

UBUNTU_PACKAGES = ['libx11-6', 'libxext6', 'libxrender1', 'libice6', 'libsm6', 'libgl1-mesa-glx', 'libglib2.0-0']
UBUNTU_LIST = [
    Ubuntu('ubuntu:20.04', machines=['x86_64', 'aarch64', 's390x', 'armv7'], packages=[['python3-pip'] + UBUNTU_PACKAGES]),  # TODO 'ppc64le'
    Ubuntu('ubuntu:19.10', machines=['i686', 'x86_64', 'aarch64', 's390x', 'armv7'], packages=[['python3-pip'] + UBUNTU_PACKAGES]),  # TODO 'ppc64le'
    Ubuntu('ubuntu:19.04', machines=['i686', 'x86_64', 'aarch64', 'ppc64le', 's390x', 'armv7'], packages=[['python3-pip'] + UBUNTU_PACKAGES]),
    Ubuntu('ubuntu:18.10', machines=['i686', 'x86_64', 'aarch64', 'ppc64le', 's390x', 'armv7'], packages=[['python3-pip'] + UBUNTU_PACKAGES], apt_sources_update=UBUNTU_APT_OLD),
    Ubuntu('ubuntu:18.04', machines=['i686', 'x86_64', 'aarch64', 'ppc64le', 's390x', 'armv7'], packages=[['python3-pip'] + UBUNTU_PACKAGES]),
    Ubuntu('ubuntu:17.10', machines=['i686', 'x86_64', 'aarch64', 'ppc64le', 's390x', 'armv7'], packages=[['python3-pip'] + UBUNTU_PACKAGES], apt_sources_update=UBUNTU_APT_OLD),
    Ubuntu('ubuntu:17.04', machines=['i686', 'x86_64', 'aarch64', 'ppc64le', 's390x', 'armv7'], packages=[['python3-pip'] + UBUNTU_PACKAGES], apt_sources_update=UBUNTU_APT_OLD),
    Ubuntu('ubuntu:16.10', machines=['x86_64'], packages=[['python3-pip'] + UBUNTU_PACKAGES], apt_sources_update=UBUNTU_APT_OLD),
    Ubuntu('ubuntu:16.04', machines=['i686', 'x86_64', 'aarch64', 'ppc64le', 's390x', 'armv7'], packages=[['python3-pip'] + UBUNTU_PACKAGES]),
    Ubuntu('ubuntu:15.10', machines=['x86_64'], packages=[['python3-pip'] + UBUNTU_PACKAGES], apt_sources_update=UBUNTU_APT_OLD),
    Ubuntu('ubuntu:15.04', machines=['x86_64'], packages=[['python3-pip'] + UBUNTU_PACKAGES], apt_sources_update=UBUNTU_APT_OLD),
    Ubuntu('ubuntu:14.10', machines=['x86_64'], packages=[['python3-pip'] + UBUNTU_PACKAGES], apt_sources_update=UBUNTU_APT_OLD),
    Ubuntu('ubuntu:14.04', machines=['i686', 'x86_64', 'aarch64', 'ppc64le', 'armv7'], packages=[['python3-pip'] + UBUNTU_PACKAGES]),
    Ubuntu('ubuntu:13.10', machines=['x86_64'], packages=[['python3-pip'] + UBUNTU_PACKAGES], apt_sources_update=UBUNTU_APT_OLD),
    Ubuntu('ubuntu:13.04', machines=['x86_64'], packages=[['python3-pip'] + UBUNTU_PACKAGES], apt_sources_update=UBUNTU_APT_OLD),
    Ubuntu('ubuntu:12.10', machines=['x86_64'], packages=[['python3.4'] + UBUNTU_PACKAGES], apt_sources_update=UBUNTU_APT_OLD, python='python3.4', ppa_list=UBUNTU_PYTHON_PPA),
    Ubuntu('ubuntu:12.04', machines=['x86_64'], packages=[['python3.5', 'curl'] + UBUNTU_PACKAGES], python='python3.5', ppa_list=UBUNTU_PYTHON_PPA),
]
