from typing import TYPE_CHECKING

from pep600_compliance.images import base, package_manager

if TYPE_CHECKING:
    from docker.models.containers import Container


class AlmaLinux(base.Base):
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
            "almalinux",
            version,
            eol,
            package_manager.DNF(),
            machines,
        )

    def install_packages(self, container: Container, machine: str) -> None:
        super()._install_packages(container, machine, self._packages)


ALMALINUX_LIST: list[base.Base] = [
    AlmaLinux(
        "almalinux:10",
        ("EOL:2035-05-31",),
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
    AlmaLinux(
        "almalinux:9",
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
    AlmaLinux(
        "almalinux:8",
        ("EOL:2029-03-01",),
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
]
