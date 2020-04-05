from pep600_compliance.images import base
from pep600_compliance.images import package_manager


class Photon(base.Base):
    def __init__(self, image, packages, machines):
        name, version = image.split(':')
        self._packages = packages
        # no X11 on photon
        skip_lib = ['libX11.so.6', 'libXext.so.6', 'libXrender.so.1', 'libICE.so.6', 'libSM.so.6', 'libGL.so.1']
        super().__init__(image, name, version, package_manager.TDNF(), skip_lib=skip_lib, machines=machines)

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


PHOTON_LIST = [
    Photon('photon:3.0', machines=['x86_64', 'aarch64'], packages=[['python3-pip', 'libnsl', 'libstdc++', 'glib']]),
    Photon('photon:2.0', machines=['x86_64'], packages=[['python3-pip', 'libnsl', 'libstdc++', 'glib']]),
    Photon('photon:1.0', machines=['x86_64'], packages=[['python3', 'libstdc++', 'glib']]),
]
