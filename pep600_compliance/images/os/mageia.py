from pep600_compliance.images import base
from pep600_compliance.images import package_manager


class Mageia(base.Base):
    def __init__(self, image, eol, pkg_manager, packages, machines):
        _, version = image.split(':')
        self._packages = packages
        super().__init__(image, 'mageia', version, eol, pkg_manager, machines)

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


MAGEIA_PACKAGES = ['which', 'python', 'python3-pip', 'libstdc++', 'glib2', 'libx11', 'libxext', 'libxrender', 'libmesagl', 'libice', 'libsm']
MAGEIA_LIST = [
    # eol info https://www.mageia.org/en/support/
    Mageia('mageia:7', ('EOL:2021-02-08',), machines=['x86_64', 'aarch64'], pkg_manager=package_manager.DNF(), packages=[MAGEIA_PACKAGES]),  # TODO 'armv7l'
    Mageia('mageia:6', ('EOL:2019-09-30',), machines=['x86_64'], pkg_manager=package_manager.DNF(), packages=[MAGEIA_PACKAGES]),  # TODO 'armv7l'
    Mageia('mageia:5', ('EOL:2017-12-31',), machines=['x86_64'], pkg_manager=package_manager.URPM(), packages=[MAGEIA_PACKAGES]),
]
