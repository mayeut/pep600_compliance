from pep600_compliance.images import base
from pep600_compliance.images import package_manager


class RHUBI(base.Base):
    def __init__(self, image, eol, pkg_manager, packages, machines, python='python3', skip_lib=[]):
        version = image.split(':')[1].split('.')[0]
        self._packages = packages
        super().__init__(image, 'rhubi', version, eol, pkg_manager, machines, python=python, skip_lib=skip_lib)

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


RHUBI_LIST = [
    # EOL info: https://access.redhat.com/support/policy/updates/errata#Life_Cycle_Dates
    RHUBI('registry.access.redhat.com/ubi8/ubi:8.2', '2029-05-31', machines=['x86_64', 'aarch64', 'ppc64le', 's390x'], pkg_manager=package_manager.DNF(), packages=[['python3-pip', 'libstdc++', 'glib2', 'libX11', 'libXext', 'libXrender', 'mesa-libGL', 'libICE', 'libSM']], skip_lib=['libnsl.so.1']),
    RHUBI('registry.access.redhat.com/ubi7/ubi:7.8', '2024-06-30', machines=['x86_64', 'ppc64le', 's390x'], pkg_manager=package_manager.YUM(), packages=[['rh-python36', 'libstdc++', 'glib2', 'libX11', 'libXext', 'libXrender', 'mesa-libGL', 'libICE', 'libSM']], python='/opt/rh/rh-python36/root/usr/bin/python3'),
]
