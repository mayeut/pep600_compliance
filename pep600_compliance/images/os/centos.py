from pep600_compliance.images import base
from pep600_compliance.images import package_manager


class CentOS(base.Base):
    def __init__(self, image, eol, pkg_manager, packages, machines):
        _, version = image.split(':')
        self._packages = packages
        super().__init__(image, 'centos', version, eol, pkg_manager, machines)

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


CENTOS_LIST = [
    CentOS('centos:8', ('EOL:2029-05-31',), machines=['x86_64', 'aarch64', 'ppc64le'], pkg_manager=package_manager.DNF(), packages=[['python3-pip', 'libnsl', 'libstdc++', 'glib2', 'libX11', 'libXext', 'libXrender', 'mesa-libGL', 'libICE', 'libSM']]),
    CentOS('centos:7', ('EOL:2024-06-30',), machines=['i686', 'x86_64', 'aarch64', 'ppc64le'], pkg_manager=package_manager.YUM(), packages=[['python3-pip', 'libstdc++', 'glib2', 'libX11', 'libXext', 'libXrender', 'mesa-libGL', 'libICE', 'libSM']]),
    CentOS('centos:6', ('EOL:2020-11-30',), machines=['i686', 'x86_64'], pkg_manager=package_manager.YUM(), packages=[['epel-release'], ['python34', 'libstdc++', 'glib2', 'libX11', 'libXext', 'libXrender', 'mesa-libGL', 'libICE', 'libSM']]),
]
