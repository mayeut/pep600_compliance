from pep600_compliance.images import base
from pep600_compliance.images import package_manager


class ClearLinux(base.Base):
    def __init__(self, image, packages):
        name, version = image.split(':')
        self._packages = packages
        super().__init__(image, name, version, None, package_manager.SWUPD())

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


CLEARLINUX_PACKAGES = ['python3-basic', 'libX11client']
CLEARLINUX_LIST = [
    ClearLinux('clearlinux:latest', [CLEARLINUX_PACKAGES]),
]
