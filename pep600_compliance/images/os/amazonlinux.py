from pep600_compliance.images import base, package_manager


class AmazonLinux(base.Base):
    def __init__(self, image, eol, pkg_manager, packages, machines):
        _, version = image.split(":")
        self._packages = packages
        super().__init__(
            image, "amazonlinux", version, eol, pkg_manager, machines=machines
        )

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


AMAZONLINUX_LIST: list[base.Base] = [
    # https://docs.aws.amazon.com/linux/al2023/ug/release-cadence.html
    AmazonLinux(
        "amazonlinux:2023",
        ("EOL:2028-01-01",),
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
            ]
        ],
    ),
    # standard eol: https://aws.amazon.com/fr/amazon-linux-2/faqs/
    AmazonLinux(
        "amazonlinux:2",
        ("EOL:2025-06-30",),
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
            ]
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
            ],
        ],
    ),
]
