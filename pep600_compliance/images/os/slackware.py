from pep600_compliance.images import base
from pep600_compliance.images import package_manager


class Slackware(base.Base):
    def __init__(self, image, pkg_manager, packages, python='python'):
        _, version = image.split(':')
        self._packages = packages
        super().__init__(image, 'slackware', version, pkg_manager, ['x86_64'], python=python)

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


SLACKWARE_LIST = [
    Slackware('vbatts/slackware:14.2', pkg_manager=package_manager.SLACKPKG(), packages=[['python-2.7.17', 'cxxlibs', 'libX11', 'libXext', 'libXrender', 'mesa', 'libICE', 'libSM']]),
    Slackware('vbatts/slackware:14.1', pkg_manager=package_manager.SLACKPKG(), packages=[['python-2.7.17', 'cxxlibs', 'libX11', 'libXext', 'libXrender', 'mesa', 'libICE', 'libSM']]),
    Slackware('vbatts/slackware:14.0', pkg_manager=package_manager.SLACKPKG(), packages=[['python-2.7.17', 'cxxlibs', 'libX11', 'libXext', 'libXrender', 'mesa', 'libICE', 'libSM']]),

]
