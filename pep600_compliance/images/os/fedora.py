from pep600_compliance.images import base
from pep600_compliance.images.package_manager import DNF, YUM


class Fedora(base.Base):
    def __init__(self, image, pkg_manager, packages, machines):
        name, version = image.split(':')
        self._packages = packages
        super().__init__(image, name, version, pkg_manager, machines=machines)

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


FEDORA_PACKAGES = ['python3-pip', 'libstdc++', 'glib2', 'libX11', 'libXext', 'libXrender', 'mesa-libGL', 'libICE', 'libSM']
FEDORA_LIST = [
    Fedora('fedora:32', machines=['x86_64', 'aarch64', 'ppc64le', 's390x'],  pkg_manager=DNF(), packages=[['libnsl'] + FEDORA_PACKAGES]),
    Fedora('fedora:31', machines=['x86_64', 'aarch64', 'ppc64le', 's390x'], pkg_manager=DNF(), packages=[['libnsl'] + FEDORA_PACKAGES]),
    Fedora('fedora:30', machines=['x86_64', 'aarch64', 'ppc64le', 's390x'], pkg_manager=DNF(), packages=[['libnsl'] + FEDORA_PACKAGES]),
    Fedora('fedora:29', machines=['x86_64', 'aarch64', 'ppc64le', 's390x'], pkg_manager=DNF(), packages=[['libnsl'] + FEDORA_PACKAGES]),  # TODO 'armv7l'
    Fedora('fedora:28', machines=['x86_64', 'aarch64', 'ppc64le', 's390x'], pkg_manager=DNF(), packages=[['libnsl'] + FEDORA_PACKAGES]),  # TODO 'armv7l'
    Fedora('fedora:27', machines=['x86_64', 'aarch64', 'ppc64le'], pkg_manager=DNF(), packages=[FEDORA_PACKAGES]),  # TODO 'armv7l'
    Fedora('fedora:26', machines=['x86_64', 'aarch64', 'ppc64le'], pkg_manager=DNF(), packages=[FEDORA_PACKAGES]),  # TODO 'armv7l'
    Fedora('fedora:25', machines=['x86_64'], pkg_manager=DNF(), packages=[FEDORA_PACKAGES]),  # TODO 'armv7l'
    Fedora('fedora:24', machines=['x86_64'], pkg_manager=DNF(), packages=[FEDORA_PACKAGES]),
    Fedora('fedora:23', machines=['x86_64'], pkg_manager=DNF(), packages=[FEDORA_PACKAGES]),
    Fedora('fedora:22', machines=['x86_64'], pkg_manager=DNF(), packages=[FEDORA_PACKAGES]),
    Fedora('fedora:21', machines=['x86_64'], pkg_manager=YUM(), packages=[FEDORA_PACKAGES]),
    Fedora('fedora:20', machines=['x86_64'], pkg_manager=YUM(), packages=[FEDORA_PACKAGES]),
]
