from pep600_compliance.images import base
from pep600_compliance.images import package_manager


class ClefOS(base.Base):
    def __init__(self, image, eol, pkg_manager, packages, machines):
        _, version = image.split(':')
        self._packages = packages
        super().__init__(image, 'clefos', version, eol, pkg_manager, machines)

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


CLEFOS_LIST = [
    ClefOS('clefos:7', ('EOL:2024-06-30',), machines=['s390x'], pkg_manager=package_manager.YUM(), packages=[['python3-pip', 'libstdc++', 'glib2', 'libX11', 'libXext', 'libXrender', 'mesa-libGL', 'libICE', 'libSM']]),
]
