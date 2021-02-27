from pep600_compliance.images import base
from pep600_compliance.images import package_manager


class Photon(base.Base):
    def __init__(self, image, eol, packages, machines):
        _, version = image.split(':')
        self._packages = packages
        # no X11 on photon
        skip_lib = ['libX11.so.6', 'libXext.so.6', 'libXrender.so.1', 'libICE.so.6', 'libSM.so.6', 'libGL.so.1']
        super().__init__(image, 'photon', version, eol, package_manager.TDNF(), skip_lib=skip_lib, machines=machines)

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


PHOTON_LIST = [
    Photon('photon:4.0', 'unknown', machines=['x86_64', 'aarch64'], packages=[['which', 'python3-pip', 'libnsl', 'libstdc++', 'glib']]),
    Photon('photon:3.0', 'unknown', machines=['x86_64', 'aarch64'], packages=[['which', 'python2', 'python3-pip', 'libnsl', 'libstdc++', 'glib']]),
    Photon('photon:2.0', 'unknown', machines=['x86_64'], packages=[['python2', 'python3-pip', 'libnsl', 'libstdc++', 'glib']]),
    Photon('photon:1.0', 'unknown', machines=['x86_64'], packages=[['which', 'python2', 'python3', 'libstdc++', 'glib']]),
]
