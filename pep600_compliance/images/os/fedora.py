from pep600_compliance.images import base
from pep600_compliance.images.package_manager import DNF, YUM


class Fedora(base.Base):
    def __init__(self, image, eol, pkg_manager, packages, machines):
        name, version = image.split(':')
        self._packages = packages
        super().__init__(image, name, version, eol, pkg_manager, machines=machines)

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


FEDORA_PACKAGES = ['python3-pip', 'libstdc++', 'glib2', 'libX11', 'libXext', 'libXrender', 'mesa-libGL', 'libICE', 'libSM']
FEDORA_LIST = [
    Fedora('fedora:34', None, machines=['x86_64', 'aarch64'], pkg_manager=DNF(), packages=[['libnsl'] + FEDORA_PACKAGES]),
    Fedora('fedora:33', None, machines=['x86_64', 'aarch64'], pkg_manager=DNF(), packages=[['libnsl'] + FEDORA_PACKAGES]),
    Fedora('fedora:32', None, machines=['x86_64', 'aarch64', 'ppc64le', 's390x'], pkg_manager=DNF(), packages=[['libnsl'] + FEDORA_PACKAGES]),
    Fedora('fedora:31', '2020-11-17', machines=['x86_64', 'aarch64', 'ppc64le', 's390x'], pkg_manager=DNF(), packages=[['libnsl'] + FEDORA_PACKAGES]),
    # EOL: https://fedoraproject.org/wiki/End_of_life
    Fedora('fedora:30', '2020-05-26', machines=['x86_64', 'aarch64', 'ppc64le', 's390x'], pkg_manager=DNF(), packages=[['libnsl'] + FEDORA_PACKAGES]),
    Fedora('fedora:29', '2019-11-26', machines=['x86_64', 'aarch64', 'ppc64le', 's390x'], pkg_manager=DNF(), packages=[['libnsl'] + FEDORA_PACKAGES]),  # TODO 'armv7l'
    Fedora('fedora:28', '2019-05-28', machines=['x86_64', 'aarch64', 'ppc64le', 's390x'], pkg_manager=DNF(), packages=[['libnsl'] + FEDORA_PACKAGES]),  # TODO 'armv7l'
    Fedora('fedora:27', '2018-11-30', machines=['x86_64', 'aarch64', 'ppc64le'], pkg_manager=DNF(), packages=[FEDORA_PACKAGES]),  # TODO 'armv7l'
    Fedora('fedora:26', '2018-05-29', machines=['x86_64', 'aarch64', 'ppc64le'], pkg_manager=DNF(), packages=[FEDORA_PACKAGES]),  # TODO 'armv7l'
    Fedora('fedora:25', '2017-12-12', machines=['x86_64'], pkg_manager=DNF(), packages=[FEDORA_PACKAGES]),  # TODO 'armv7l'
    Fedora('fedora:24', '2017-08-08', machines=['x86_64'], pkg_manager=DNF(), packages=[FEDORA_PACKAGES]),
    Fedora('fedora:23', '2016-12-20', machines=['x86_64'], pkg_manager=DNF(), packages=[FEDORA_PACKAGES]),
    Fedora('fedora:22', '2016-07-19', machines=['x86_64'], pkg_manager=DNF(), packages=[FEDORA_PACKAGES]),
    Fedora('fedora:21', '2015-12-01', machines=['x86_64'], pkg_manager=YUM(), packages=[FEDORA_PACKAGES]),
    Fedora('fedora:20', '2015-06-23', machines=['x86_64'], pkg_manager=YUM(), packages=[FEDORA_PACKAGES]),
]
