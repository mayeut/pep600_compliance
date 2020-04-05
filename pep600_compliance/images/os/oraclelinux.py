from pep600_compliance.images import base
from pep600_compliance.images import package_manager


class OracleLinux(base.Base):
    def __init__(self, image, pkg_manager, packages, machines, python='python3'):
        name, version = image.split(':')
        version = version.split('-')[0]
        self._packages = packages
        super().__init__(image, name, version, pkg_manager, python=python, machines=machines)

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)

#
ORACLELINUX_LIST = [
    OracleLinux('oraclelinux:8-slim', machines=['x86_64', 'aarch64'], pkg_manager=package_manager.MICRODNF(), packages=[['python3-pip', 'libnsl', 'libstdc++', 'glib2', 'libX11', 'libXext', 'libXrender', 'mesa-libGL', 'libICE', 'libSM']]),
    OracleLinux('oraclelinux:7-slim', machines=['x86_64', 'aarch64'], pkg_manager=package_manager.YUM(), packages=[['python3-pip', 'libstdc++', 'glib2', 'libX11', 'libXext', 'libXrender', 'mesa-libGL', 'libICE', 'libSM']]),
    OracleLinux('oraclelinux:6-slim', machines=['x86_64'], pkg_manager=package_manager.YUM(run_once=[['yum-config-manager', '--enable', 'ol6_software_collections']]), packages=[['rh-python36-python-pip', 'libstdc++', 'glib2', 'libX11', 'libXext', 'libXrender', 'mesa-libGL', 'libICE', 'libSM']], python='/opt/rh/rh-python36/root/usr/bin/python3'),
]
