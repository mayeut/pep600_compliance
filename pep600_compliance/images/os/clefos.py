from typing import TYPE_CHECKING

from pep600_compliance.images import base, package_manager

if TYPE_CHECKING:
    from docker.models.containers import Container


class ClefOS(base.Base):
    def __init__(
        self,
        image: str,
        eol: tuple[str, ...] | str,
        pkg_manager: package_manager._PackageManager,
        packages: list[list[str]],
        machines: tuple[str, ...],
    ) -> None:
        _, version = image.split(":")
        self._packages = packages
        super().__init__(image, "clefos", version, eol, pkg_manager, machines)

    def install_packages(self, container: Container, machine: str) -> None:
        super()._install_packages(container, machine, self._packages)


CLEFOS_LIST: list[base.Base] = [
    ClefOS(
        "clefos:7",
        ("EOL:2024-06-30",),
        machines=("s390x",),
        pkg_manager=package_manager.YUM(),
        packages=[
            [
                "which",
                "python",
                "python3-pip",
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
