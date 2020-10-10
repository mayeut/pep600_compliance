from pep600_compliance.images import base
from pep600_compliance.images import package_manager


class Debian(base.Base):
    def __init__(self, image, eol, packages, machines, apt_sources_update=[]):
        name, version = image.split(':')
        version = version.split('-')[0]
        self._packages = packages
        super().__init__(image, name, version, eol, package_manager.APT(run_once=apt_sources_update), machines=machines)

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


DEBIAN_APT_OLD = [
    ['sed', '-i', 's,deb.debian.org,archive.debian.org,g', '/etc/apt/sources.list'],
    ['sed', '-i', 's,.*security.*,,g', '/etc/apt/sources.list'],
    ['sed', '-i', 's,.*updates.*,,g', '/etc/apt/sources.list'],
]
DEBIAN_PACKAGES = ['python3-pip', 'libx11-6', 'libxext6', 'libxrender1', 'libice6', 'libsm6', 'libgl1-mesa-glx', 'libglib2.0-0']
DEBIAN_LIST = [
    Debian('debian:bullseye-slim', None, machines=['i686', 'x86_64', 'aarch64', 'ppc64le', 's390x', 'armv7l'], packages=[DEBIAN_PACKAGES]),
    # LTS: https://wiki.debian.org/LTS
    Debian('debian:10-slim', '2024-06-30', machines=['i686', 'x86_64', 'aarch64', 'ppc64le', 's390x', 'armv7l'], packages=[DEBIAN_PACKAGES]),
    Debian('debian:9-slim', '2022-06-30', machines=['i686', 'x86_64', 'aarch64', 'ppc64le', 's390x', 'armv7l'], packages=[DEBIAN_PACKAGES]),
    # ELTS: https://wiki.debian.org/LTS/Extended
    Debian('debian:8-slim', '2022-06-30', machines=['i686', 'x86_64', 'armv7l'], packages=[DEBIAN_PACKAGES]),  # TODO 'aarch64', 'ppc64le', 's390x'
    Debian('debian:7-slim', '2020-06-30', machines=['i686', 'x86_64', 'armv7l'], packages=[DEBIAN_PACKAGES + ['curl']], apt_sources_update=DEBIAN_APT_OLD),
]
