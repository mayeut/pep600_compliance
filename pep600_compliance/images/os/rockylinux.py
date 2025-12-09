from typing import TYPE_CHECKING

from pep600_compliance.images import base, package_manager

if TYPE_CHECKING:
    from docker.models.containers import Container


class RockyLinux(base.Base):
    def __init__(
        self,
        image: str,
        eol: tuple[str, ...] | str,
        packages: list[list[str]],
        machines: tuple[str, ...],
    ) -> None:
        _, version = image.split(":")
        self._packages = packages
        super().__init__(
            image,
            "rockylinux",
            version,
            eol,
            package_manager.DNF(),
            machines,
        )

    def install_packages(self, container: Container, machine: str) -> None:
        super()._install_packages(container, machine, self._packages)


ROCKYLINUX_LIST: list[base.Base] = [
    RockyLinux(
        "rockylinux/rockylinux:10",
        ("EOL:2035-05-31",),
        machines=("x86_64", "aarch64", "ppc64le", "s390x", "riscv64"),
        packages=[
            [
                "which",
                "python3-pip",
                "libnsl",
                "libstdc++",
                "glib2",
                "libX11",
                "libXext",
                "libXrender",
                "mesa-libGL",
                "libICE",
                "libSM",
                "libatomic",
            ],
        ],
    ),
    RockyLinux(
        "rockylinux:9",
        ("EOL:2032-05-31",),
        machines=("x86_64", "aarch64", "ppc64le", "s390x"),
        packages=[
            [
                "which",
                "python3-pip",
                "libnsl",
                "libstdc++",
                "glib2",
                "libX11",
                "libXext",
                "libXrender",
                "mesa-libGL",
                "libICE",
                "libSM",
                "libatomic",
            ],
        ],
    ),
    RockyLinux(
        "rockylinux:8",
        ("EOL:2029-05-31",),
        machines=("x86_64", "aarch64"),
        packages=[
            [
                "which",
                "python3-pip",
                "libnsl",
                "libstdc++",
                "glib2",
                "libX11",
                "libXext",
                "libXrender",
                "mesa-libGL",
                "libICE",
                "libSM",
                "libatomic",
            ],
        ],
    ),
]
