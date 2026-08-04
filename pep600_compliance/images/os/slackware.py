from pep600_compliance.images import base, package_manager

TYPE_CHECKING = False
if TYPE_CHECKING:
    from docker.models.containers import Container


class Slackware(base.Base):
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
        super().__init__(
            image,
            "slackware",
            version,
            eol,
            pkg_manager,
            machines=machines,
        )

    def install_packages(self, container: Container, machine: str) -> None:
        super()._install_packages(container, machine, self._packages)


SLACKWARE_LIST: list[base.Base] = [
    Slackware(
        "aclemons/slackware:current",
        "rolling",
        machines=("x86_64", "i686", "aarch64"),
        pkg_manager=package_manager.SLACKPKG(current=True),
        packages=[
            [
                "aaa_glibc-solibs",
                "python2",
                "python3",
                "cxxlibs",
                "libX11",
                "libXext",
                "libXrender",
                "mesa",
                "libICE",
                "libSM",
                "libglvnd",
            ],
        ],
    ),
    Slackware(
        "vbatts/slackware:15.0",
        "unknown",
        machines=("x86_64",),
        pkg_manager=package_manager.SLACKPKG(),
        packages=[
            [
                "python2",
                "python3",
                "cxxlibs",
                "libX11",
                "libXext",
                "libXrender",
                "mesa",
                "libICE",
                "libSM",
                "libglvnd",
            ],
        ],
    ),
]
