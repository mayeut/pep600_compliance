from pep600_compliance.images import base, package_manager


class OpenEuler(base.Base):
    def __init__(self, image, eol, packages, machines, python="python3"):
        _, version = image.split(":")
        self._packages = packages
        super().__init__(
            image,
            "openeuler",
            version,
            eol,
            package_manager.DNF(),
            python=python,
            machines=machines,
        )

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


OPENEULER_LIST: list[base.Base] = [
    # EOL info: https://www.openeuler.org/en/other/lifecycle/
    OpenEuler(
        "openeuler/openeuler:24.03",
        ("EOL:2028-03-31",),
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
            ]
        ],
    ),
]
