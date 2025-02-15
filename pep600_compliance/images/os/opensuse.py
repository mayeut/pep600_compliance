from pep600_compliance.images import base, package_manager


class OpenSUSE(base.Base):
    def __init__(self, image, eol, packages, machines, version=None):
        if version is None:
            _, version = image.split(":")
        self._packages = packages
        super().__init__(
            image, "opensuse", version, eol, package_manager.ZYPPER(), machines=machines
        )

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


OPENSUSE_PACKAGES = [
    "which",
    "python",
    "python3-pip",
    "libX11-6",
    "libXext6",
    "libXrender1",
    "libICE6",
    "libSM6",
    "Mesa-libGL1",
    "libglib-2_0-0",
    "libgobject-2_0-0",
    "libgthread-2_0-0",
]
OPENSUSE_LIST: list[base.Base] = [
    # EOL info: https://en.opensuse.org/Lifetime
    OpenSUSE(
        "opensuse/tumbleweed:latest",
        "rolling",
        machines=("i686", "x86_64", "aarch64", "ppc64le", "s390x", "armv7l"),
        packages=[OPENSUSE_PACKAGES, ["libnsl1"]],
        version="tumbleweed",
    ),
    OpenSUSE(
        "opensuse/leap:15.6",
        ("EOL:2025-12-31",),
        machines=("x86_64", "aarch64"),
        packages=[OPENSUSE_PACKAGES, ["libnsl1"]],
    ),
    OpenSUSE(
        "opensuse/leap:15.5",
        ("EOL:2024-12-31",),
        machines=("x86_64", "aarch64", "ppc64le", "s390x", "armv7l"),
        packages=[OPENSUSE_PACKAGES],
    ),
    OpenSUSE(
        "opensuse/leap:15.4",
        ("EOL:2023-12-07",),
        machines=("x86_64", "aarch64", "ppc64le", "s390x", "armv7l"),
        packages=[OPENSUSE_PACKAGES],
    ),
    OpenSUSE(
        "opensuse/leap:15.3",
        ("EOL:2022-12-01",),
        machines=("x86_64", "aarch64", "ppc64le", "s390x", "armv7l"),
        packages=[OPENSUSE_PACKAGES],
    ),
    OpenSUSE(
        "opensuse/leap:15.2",
        ("EOL:2021-12-01",),
        machines=("x86_64", "aarch64", "ppc64le", "armv7l"),
        packages=[OPENSUSE_PACKAGES],
    ),
    OpenSUSE(
        "opensuse/leap:15.1",
        ("EOL:2021-02-02",),
        machines=("x86_64", "aarch64", "ppc64le", "armv7l"),
        packages=[OPENSUSE_PACKAGES],
    ),
]
