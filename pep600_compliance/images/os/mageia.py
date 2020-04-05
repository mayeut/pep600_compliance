from pep600_compliance.images import base
from pep600_compliance.images import package_manager


class Mageia(base.Base):
    def __init__(self, image, pkg_manager, packages, machines):
        name, version = image.split(':')
        self._packages = packages
        super().__init__(image, name, version, pkg_manager, machines)

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


MAGEIA_PACKAGES = ['python3-pip', 'libstdc++', 'glib2', 'libx11', 'libxext', 'libxrender', 'libmesagl', 'libice', 'libsm']
MAGEIA_LIST = [
    Mageia('mageia:7', machines=['x86_64', 'aarch64'], pkg_manager=package_manager.DNF(), packages=[MAGEIA_PACKAGES]),  # TODO 'armv7l'
    Mageia('mageia:6', machines=['x86_64'], pkg_manager=package_manager.DNF(), packages=[MAGEIA_PACKAGES]),  # TODO 'armv7l'
    Mageia('mageia:5', machines=['x86_64'], pkg_manager=package_manager.URPM(), packages=[MAGEIA_PACKAGES]),
]
