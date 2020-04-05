from pep600_compliance.images import base
from pep600_compliance.images import package_manager


class Debian(base.Base):
    def __init__(self, image, packages, machines):
        name, version = image.split(':')
        version = version.split('-')[0]
        self._packages = packages
        super().__init__(image, name, version, package_manager.APT(), machines=machines)

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


DEBIAN_PACKAGES = ['python3-pip', 'libx11-6', 'libxext6', 'libxrender1', 'libice6', 'libsm6', 'libgl1-mesa-glx', 'libglib2.0-0']
DEBIAN_LIST = [
    Debian('debian:bullseye-slim', machines=['i686', 'x86_64', 'aarch64', 'ppc64le', 's390x', 'armv7l'], packages=[DEBIAN_PACKAGES]),
    Debian('debian:10-slim', machines=['i686', 'x86_64', 'aarch64', 'ppc64le', 's390x', 'armv7l'], packages=[DEBIAN_PACKAGES]),
    Debian('debian:9-slim', machines=['i686', 'x86_64', 'aarch64', 'ppc64le', 's390x', 'armv7l'], packages=[DEBIAN_PACKAGES]),
    Debian('debian:8-slim', machines=['i686', 'x86_64', 'aarch64', 'ppc64le', 's390x', 'armv7l'], packages=[DEBIAN_PACKAGES]),
]
