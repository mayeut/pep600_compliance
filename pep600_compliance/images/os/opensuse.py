from pep600_compliance.images import base
from pep600_compliance.images import package_manager


class OpenSUSE(base.Base):
    def __init__(self, image, eol, packages, machines, version=None):
        if version is None:
            _, version = image.split(':')
        self._packages = packages
        super().__init__(image, 'opensuse', version, eol, package_manager.ZYPPER(), machines=machines)

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


OPENSUSE_PACKAGES = ['which', 'python', 'python3-pip', 'libX11-6', 'libXext6', 'libXrender1', 'libICE6', 'libSM6', 'Mesa-libGL1', 'libglib-2_0-0', 'libgobject-2_0-0', 'libgthread-2_0-0']
OPENSUSE_LIST = [
    #EOL info: https://en.opensuse.org/Lifetime
    OpenSUSE('opensuse/tumbleweed:latest', 'rolling', machines=['i686', 'x86_64', 'aarch64', 'ppc64le', 'armv7l'], packages=[OPENSUSE_PACKAGES], version='tumbleweed'),  # TODO 's390x'
    OpenSUSE('opensuse/leap:15.2', ('EOL:2021-12-31',), machines=['x86_64', 'aarch64', 'ppc64le', 'armv7l'], packages=[OPENSUSE_PACKAGES]),
    OpenSUSE('opensuse/leap:15.1', ('EOL:2020-11-30',), machines=['x86_64', 'aarch64', 'ppc64le', 'armv7l'], packages=[OPENSUSE_PACKAGES]),
    OpenSUSE('opensuse/leap:15.0', ('EOL:2019-12-03',), machines=['x86_64', 'aarch64', 'ppc64le'], packages=[OPENSUSE_PACKAGES]),
    OpenSUSE('opensuse/leap:42.3', ('EOL:2019-07-01',), machines=['x86_64'], packages=[OPENSUSE_PACKAGES]),
    OpenSUSE('opensuse/archive:42.2', ('EOL:2018-01-26',), machines=['x86_64'], packages=[OPENSUSE_PACKAGES]),
    OpenSUSE('opensuse/archive:42.1', ('EOL:2017-05-17',), machines=['x86_64'], packages=[OPENSUSE_PACKAGES]),
    OpenSUSE('opensuse/archive:13.2', ('EOL:2017-01-17',), machines=['x86_64'], packages=[OPENSUSE_PACKAGES]),
]
