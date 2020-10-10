from pep600_compliance.images import base
from pep600_compliance.images import package_manager


class ArchLinux(base.Base):
    def __init__(self, image, packages):
        name, version = image.split(':')
        self._packages = packages
        super().__init__(image, name, version, None, package_manager.PACMAN())

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


ARCHLINUX_PACKAGES = ['python-pip', 'glib2', 'libx11', 'libxext', 'libxrender', 'libice', 'libsm', 'mesa']
ARCHLINUX_LIST = [
    ArchLinux('archlinux:20200908', [ARCHLINUX_PACKAGES]),
    ArchLinux('archlinux:20200306', [ARCHLINUX_PACKAGES]),
    ArchLinux('archlinux:20200205', [ARCHLINUX_PACKAGES]),
    ArchLinux('archlinux:20200106', [ARCHLINUX_PACKAGES]),
    ArchLinux('archlinux:20191205', [ARCHLINUX_PACKAGES]),
    ArchLinux('archlinux:20191105', [ARCHLINUX_PACKAGES]),
    ArchLinux('archlinux:20191006', [ARCHLINUX_PACKAGES]),
]
