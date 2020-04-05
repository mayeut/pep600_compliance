from pep600_compliance.images import base
from pep600_compliance.images import package_manager


class AmazonLinux(base.Base):
    def __init__(self, image, pkg_manager, packages, machines):
        name, version = image.split(':')
        self._packages = packages
        super().__init__(image, name, version, pkg_manager, machines=machines)

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


AMAZONLINUX_LIST = [
    AmazonLinux('amazonlinux:2', machines=['x86_64', 'aarch64'], pkg_manager=package_manager.YUM(), packages=[['python3-pip', 'libstdc++', 'glib2', 'libX11', 'libXext', 'libXrender', 'mesa-libGL', 'libICE', 'libSM']]),
    AmazonLinux('amazonlinux:1', machines=['x86_64'], pkg_manager=package_manager.YUM(), packages=[['epel-release'], ['python34', 'libstdc++', 'glib2', 'libX11', 'libXext', 'libXrender', 'mesa-libGL', 'libICE', 'libSM']]),
]
