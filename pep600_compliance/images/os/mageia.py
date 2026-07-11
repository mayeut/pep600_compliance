from pep600_compliance.images import base, package_manager

TYPE_CHECKING = False
if TYPE_CHECKING:
    from docker.models.containers import Container


class Mageia(base.Base):
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
        super().__init__(image, "mageia", version, eol, pkg_manager, machines)

    def install_packages(self, container: Container, machine: str) -> None:
        super()._install_packages(container, machine, self._packages)


MAGEIA_PACKAGES = [
    "which",
    "python",
    "python3-pip",
    "libstdc++",
    "glib2",
    "libx11",
    "libxext",
    "libxrender",
    "libmesagl",
    "libice",
    "libsm",
    "libatomic",
]
MAGEIA_LIST: list[base.Base] = [
    Mageia(
        "mageia:cauldron",
        "rolling",
        machines=("x86_64", "aarch64"),
        pkg_manager=package_manager.DNF5([["dnf", "upgrade", "-y", "--refresh"]]),
        packages=[MAGEIA_PACKAGES],
    ),  # TODO 'armv7l'
    # eol info https://www.mageia.org/en/support/
    Mageia(
        "mageia:9",
        ("EOL:2026-09-29",),
        machines=("x86_64", "aarch64"),
        pkg_manager=package_manager.DNF(),
        packages=[MAGEIA_PACKAGES],
    ),
]
