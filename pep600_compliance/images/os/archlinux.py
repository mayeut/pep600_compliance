from pep600_compliance.images import base
from pep600_compliance.images import package_manager


class ArchLinux(base.Base):
    def __init__(self, image, packages):
        _, version = image.split(':')
        self._packages = packages
        super().__init__(image, 'archlinux', version, 'rolling', package_manager.PACMAN())

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


ARCHLINUX_PACKAGES = ['python-pip', 'glib2', 'libx11', 'libxext', 'libxrender', 'libice', 'libsm', 'mesa']
ARCHLINUX_LIST = [
    ArchLinux('archlinux:latest', [ARCHLINUX_PACKAGES]),
]
