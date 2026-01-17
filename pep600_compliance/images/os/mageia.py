from typing import TYPE_CHECKING

from pep600_compliance.images import base, package_manager

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
MAGEIA_ARCHIVE = "https://distrib-coffee.ipsl.jussieu.fr/pub/linux/Mageia-archive"
MAGEIA6_RUNONCE = [
    "sed -i 's;mirrorlist=.*;#mirrorlist=;g' /etc/yum.repos.d/mageia-x86_64.repo",
    f"sed -i 's;#baseurl=https://mirrors.kernel.org/mageia;baseurl={MAGEIA_ARCHIVE};g' "
    "/etc/yum.repos.d/mageia-x86_64.repo",
]
MAGEIA5_RUNONCE = [
    f"sed -i 's;mirrorlist:.*;mirrorlist: {MAGEIA_ARCHIVE}/distrib/5/x86_64;g' "
    "/etc/urpmi/urpmi.cfg",
]
MAGEIA_LIST: list[base.Base] = [
    Mageia(
        "mageia:cauldron",
        "rolling",
        machines=("x86_64", "aarch64"),
        pkg_manager=package_manager.DNF(),
        packages=[MAGEIA_PACKAGES],
    ),  # TODO 'armv7l'
    # eol info https://www.mageia.org/en/support/
    Mageia(
        "mageia:9",
        ("EOL:2025-03-31",),
        machines=("x86_64", "aarch64"),
        pkg_manager=package_manager.DNF(),
        packages=[MAGEIA_PACKAGES],
    ),
    Mageia(
        "mageia:8",
        ("EOL:2023-11-30",),
        machines=("x86_64", "aarch64"),
        pkg_manager=package_manager.DNF(),
        packages=[MAGEIA_PACKAGES],
    ),  # TODO 'armv7l'
]
