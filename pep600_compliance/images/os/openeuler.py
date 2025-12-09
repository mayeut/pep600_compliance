from typing import TYPE_CHECKING

from pep600_compliance.images import base, package_manager

if TYPE_CHECKING:
    from docker.models.containers import Container


class OpenEuler(base.Base):
    def __init__(
        self,
        image: str,
        eol: tuple[str, ...] | str,
        packages: list[list[str]],
        machines: tuple[str, ...],
        python: str = "python3",
    ) -> None:
        _, version = image.split(":")
        self._packages = packages
        super().__init__(
            image,
            "openeuler",
            version,
            eol,
            package_manager.DNF(),
            python=python,
            machines=machines,
        )

    def install_packages(self, container: Container, machine: str) -> None:
        packages = self._packages
        if machine == "loongarch64":
            packages = [
                [package for package in packages_ if package != "libnsl"] for packages_ in packages
            ]
        super()._install_packages(container, machine, packages)


OPENEULER_LIST: list[base.Base] = [
    # EOL info: https://www.openeuler.org/en/other/lifecycle/
    OpenEuler(
        "openeuler/openeuler:24.03",
        ("EOL:2028-03-31",),
        machines=("x86_64", "aarch64", "loongarch64"),
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
