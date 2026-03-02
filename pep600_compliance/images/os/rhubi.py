from typing import TYPE_CHECKING

from pep600_compliance.images import base, package_manager

if TYPE_CHECKING:
    from docker.models.containers import Container


class RHUBI(base.Base):
    def __init__(
        self,
        image: str,
        eol: tuple[str, ...] | str,
        pkg_manager: package_manager._PackageManager,
        packages: list[list[str]],
        machines: tuple[str, ...],
        python: str = "python3",
        skip_lib: frozenset[str] = frozenset(),
    ) -> None:
        version = image.split(":")[1].split(".", maxsplit=1)[0]
        self._packages = packages
        super().__init__(
            image,
            "rhubi",
            version,
            eol,
            pkg_manager,
            machines,
            python=python,
            skip_lib=skip_lib,
        )

    def install_packages(self, container: Container, machine: str) -> None:
        super()._install_packages(container, machine, self._packages)


RHUBI_LIST: list[base.Base] = [
    # EOL info: https://access.redhat.com/support/policy/updates/errata#Life_Cycle_Dates
    RHUBI(
        "redhat/ubi10:10.0",
        ("EOL:2035-05-31", "ELTS:2038-05-31"),
        machines=("x86_64", "aarch64", "ppc64le", "s390x"),
        pkg_manager=package_manager.DNF(),
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
        skip_lib=frozenset(("libnsl.so.1",)),
    ),
    RHUBI(
        "redhat/ubi9:9.4",
        ("EOL:2032-05-31", "ELTS:2035-05-31"),
        machines=("x86_64", "aarch64", "ppc64le", "s390x"),
        pkg_manager=package_manager.DNF(),
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
        skip_lib=frozenset(("libnsl.so.1",)),
    ),
    RHUBI(
        "redhat/ubi8:8.10",
        ("EOL:2029-05-31", "ELTS:2032-05-31"),
        machines=("x86_64", "aarch64", "ppc64le", "s390x"),
        pkg_manager=package_manager.DNF(),
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
        skip_lib=frozenset(("libnsl.so.1",)),
    ),
    RHUBI(
        "registry.access.redhat.com/ubi7/ubi:7.8",
        ("EOL:2024-06-30", "ELTS:2028-06-30"),
        machines=("x86_64", "ppc64le", "s390x"),
        pkg_manager=package_manager.YUM(),
        packages=[
            [
                "which",
                "python",
                "rh-python36",
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
        python="/opt/rh/rh-python36/root/usr/bin/python3",
    ),
]
