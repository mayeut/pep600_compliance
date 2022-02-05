from pep600_compliance.images import base, package_manager


class RockyLinux(base.Base):
    def __init__(self, image, eol, packages, machines):
        _, version = image.split(":")
        self._packages = packages
        super().__init__(
            image, "rockylinux", version, eol, package_manager.DNF(), machines
        )

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


ROCKYLINUX_LIST: list[base.Base] = [
    RockyLinux(
        "rockylinux:8",
        ("EOL:2029-05-31",),
        machines=["x86_64", "aarch64"],
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
            ]
        ],
    ),
]
