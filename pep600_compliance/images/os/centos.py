from typing import TYPE_CHECKING

from pep600_compliance.images import base, package_manager

if TYPE_CHECKING:
    from docker.models.containers import Container


class CentOS(base.Base):
    def __init__(
        self,
        image: str,
        eol: tuple[str, ...] | str,
        pkg_manager: package_manager._PackageManager,
        packages: list[list[str]],
        machines: tuple[str, ...],
    ) -> None:
        _, version = image.split(":")
        if "-development" in version:
            version = version.replace("-development", "")
        self._packages = packages
        super().__init__(image, "centos", version, eol, pkg_manager, machines)

    def install_packages(self, container: Container, machine: str) -> None:
        super()._install_packages(container, machine, self._packages)


CENTOS_YUM_OLD = [
    [
        "sed",
        "-i",
        "s/enabled=1/enabled=0/g",
        "/etc/yum/pluginconf.d/fastestmirror.conf",
    ],
    ["bash", "-ec", "sed -i 's/^mirrorlist/#mirrorlist/g' /etc/yum.repos.d/*.repo"],
    [
        "bash",
        "-ec",
        "sed -i 's;^#baseurl=http://mirror;baseurl=https://vault;g' /etc/yum.repos.d/*.repo",
    ],
]

CENTOS_LIST: list[base.Base] = [
    CentOS(
        "quay.io/centos/centos:stream10",
        ("EOL:2030-01-01",),
        machines=("x86_64", "aarch64", "ppc64le", "s390x"),
        pkg_manager=package_manager.DNF(),
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
    CentOS(
        "quay.io/centos/centos:stream9",
        ("EOL:2027-05-31",),
        machines=("x86_64", "aarch64", "ppc64le", "s390x"),
        pkg_manager=package_manager.DNF(),
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
    CentOS(
        "quay.io/centos/centos:stream8",
        ("EOL:2024-05-31",),
        machines=("x86_64", "aarch64", "ppc64le"),
        pkg_manager=package_manager.DNF(),
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
    CentOS(
        "centos:7",
        ("EOL:2024-06-30",),
        machines=("i686", "x86_64", "aarch64", "ppc64le"),
        pkg_manager=package_manager.YUM(run_once=CENTOS_YUM_OLD),
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
