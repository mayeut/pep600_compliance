from pep600_compliance.images import base, package_manager


class AnolisOS(base.Base):
    def __init__(self, image, eol, pkg_manager, packages, machines, python="python3"):
        _, version = image.split(":")
        self._packages = packages
        super().__init__(
            image,
            "anolisos",
            version,
            eol,
            pkg_manager,
            python=python,
            machines=machines,
        )

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


ANOLISOS_LIST: list[base.Base] = [
    # https://www.alibabacloud.com/help/en/ecs/user-guide/end-of-support-for-operating-systems
    AnolisOS(
        "openanolis/anolisos:8",
        ("EOL:2031-06-30",),
        machines=("x86_64", "aarch64"),
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
            ]
        ],
    ),
]
