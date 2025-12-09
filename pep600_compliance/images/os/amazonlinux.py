from typing import TYPE_CHECKING

from pep600_compliance.images import base, package_manager

if TYPE_CHECKING:
    from docker.models.containers import Container


class AmazonLinux(base.Base):
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
            "amazonlinux",
            version,
            eol,
            pkg_manager,
            machines=machines,
        )

    def install_packages(self, container: Container, machine: str) -> None:
        super()._install_packages(container, machine, self._packages)


AMAZONLINUX_LIST: list[base.Base] = [
    # https://docs.aws.amazon.com/linux/al2023/ug/release-cadence.html
    AmazonLinux(
        "amazonlinux:2023",
        ("EOL:2028-03-15",),
        machines=("x86_64", "aarch64"),
        pkg_manager=package_manager.DNF(),
        packages=[
            [
                "which",
                "python",
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
    # standard eol: https://aws.amazon.com/fr/amazon-linux-2/faqs/
    AmazonLinux(
        "amazonlinux:2",
        ("EOL:2026-06-30",),
        machines=("x86_64", "aarch64"),
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
    # extended support date rather than eol:
    # https://aws.amazon.com/fr/blogs/aws/update-on-amazon-linux-ami-end-of-life/
    AmazonLinux(
        "amazonlinux:1",
        ("EOL:2020-12-31", "LTS:2023-12-31"),
        machines=("x86_64",),
        pkg_manager=package_manager.YUM(),
        packages=[
            ["epel-release"],
            [
                "which",
                "python",
                "python34",
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
