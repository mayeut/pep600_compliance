from typing import TYPE_CHECKING

from pep600_compliance.images import base, package_manager

if TYPE_CHECKING:
    from docker.models.containers import Container


class OpenSUSE(base.Base):
    def __init__(
        self,
        image: str,
        eol: tuple[str, ...] | str,
        packages: list[list[str]],
        machines: tuple[str, ...],
        version: str | None = None,
        skip_lib: frozenset[str] = frozenset(),
    ) -> None:
        if version is None:
            _, version = image.split(":")
        self._packages = packages
        super().__init__(
            image,
            "opensuse",
            version,
            eol,
            package_manager.ZYPPER(),
            machines=machines,
            skip_lib=skip_lib,
        )

    def install_packages(self, container: Container, machine: str) -> None:
        super()._install_packages(container, machine, self._packages)


OPENSUSE_PACKAGES = [
    "which",
    "python3",
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
    "libatomic1",
]
OPENSUSE_LIST: list[base.Base] = [
    # EOL info: https://en.opensuse.org/Lifetime
    OpenSUSE(
        "opensuse/tumbleweed:latest",
        "rolling",
        machines=("i686", "x86_64", "aarch64", "ppc64le", "s390x", "armv7l", "riscv64"),
        packages=[OPENSUSE_PACKAGES],
        version="tumbleweed",
        skip_lib=frozenset(("libnsl.so.1",)),
    ),
    OpenSUSE(
        "opensuse/leap:16.0",
        ("EOL:2027-10-31",),
        machines=("x86_64", "aarch64", "ppc64le"),
        packages=[OPENSUSE_PACKAGES],
        skip_lib=frozenset(("libnsl.so.1",)),
    ),
    OpenSUSE(
        "opensuse/leap:15.6",
        ("EOL:2026-04-30",),
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
]
