from typing import TYPE_CHECKING

from pep600_compliance.images import base, package_manager

if TYPE_CHECKING:
    from docker.models.containers import Container


class Photon(base.Base):
    def __init__(
        self,
        image: str,
        eol: tuple[str, ...] | str,
        packages: list[list[str]],
        machines: tuple[str, ...],
    ) -> None:
        _, version = image.split(":")
        self._packages = packages
        # no X11 on photon
        skip_lib = frozenset(
            (
                "libX11.so.6",
                "libXext.so.6",
                "libXrender.so.1",
                "libICE.so.6",
                "libSM.so.6",
                "libGL.so.1",
            ),
        )
        super().__init__(
            image,
            "photon",
            version,
            eol,
            package_manager.TDNF(),
            skip_lib=skip_lib,
            machines=machines,
        )

    def install_packages(self, container: Container, machine: str) -> None:
        super()._install_packages(container, machine, self._packages)


PHOTON_PACKAGES = ["which", "libnsl", "libstdc++", "glib", "libgcc-atomic"]

PHOTON_LIST: list[base.Base] = [
    # EOL info:
    # https://blogs.vmware.com/vsphere/2022/01/photon-1-x-end-of-support-announcement.html
    Photon(
        "photon:5.0",
        "unknown",
        machines=("x86_64", "aarch64"),
        packages=[["python3-pip", *PHOTON_PACKAGES]],
    ),
    Photon(
        "photon:4.0",
        ("EOL:2026-03-01",),
        machines=("x86_64", "aarch64"),
        packages=[["python3-pip", *PHOTON_PACKAGES]],
    ),
    Photon(
        "photon:3.0",
        ("EOL:2024-03-01",),
        machines=("x86_64", "aarch64"),
        packages=[["python2", "python3-pip", *PHOTON_PACKAGES]],
    ),
    Photon(
        "photon:2.0",
        ("EOL:2022-12-31",),
        machines=("x86_64",),
        packages=[["python2", "python3-pip", *PHOTON_PACKAGES]],
    ),
    Photon(
        "photon:1.0",
        ("EOL:2022-02-28",),
        machines=("x86_64",),
        packages=[["python2", "python3", *PHOTON_PACKAGES]],
    ),
]
