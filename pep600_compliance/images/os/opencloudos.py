from typing import TYPE_CHECKING

from pep600_compliance.images import base, package_manager

if TYPE_CHECKING:
    from docker.models.containers import Container


class OpenCloudOS(base.Base):
    def __init__(
        self,
        image: str,
        eol: tuple[str, ...] | str,
        packages: list[list[str]],
        machines: tuple[str, ...],
        python: str = "python3",
    ) -> None:
        version = image.split("/")[1].split("-")[0][11:]
        self._packages = packages
        super().__init__(
            image,
            "opencloudos",
            version,
            eol,
            package_manager.DNF(),
            python=python,
            machines=machines,
        )

    def install_packages(self, container: Container, machine: str) -> None:
        super()._install_packages(container, machine, self._packages)


OPENCLOUDOS_LIST: list[base.Base] = [
    # EOL info: https://docs.opencloudos.org/release/oc_intro/#oc8oc9
    OpenCloudOS(
        "opencloudos/opencloudos9-minimal:latest",
        ("EOL:2033-04-30",),
        machines=("x86_64", "aarch64"),
        packages=[
            [
                "which",
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
    OpenCloudOS(
        "opencloudos/opencloudos8-minimal:latest",
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
