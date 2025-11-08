from pep600_compliance.images import base, package_manager


class AnolisOS(base.Base):
    def __init__(
        self,
        image: str,
        eol: tuple[str, ...] | str,
        pkg_manager,
        packages: list[list[str]],
        machines: tuple[str, ...],
        python: str = "python3",
    ):
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
        packages = self._packages
        if machine == "loongarch64":
            packages = [
                [package for package in packages_ if package != "libnsl"]
                for packages_ in packages
            ]
        super()._install_packages(container, machine, packages)


ANOLISOS_LIST: list[base.Base] = [
    AnolisOS(
        "openanolis/anolisos:23",
        ("EOL:2030-06-30",),
        machines=("x86_64", "aarch64", "loongarch64"),
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
            ]
        ],
    ),
    # https://www.alibabacloud.com/help/en/ecs/user-guide/end-of-support-for-operating-systems
    AnolisOS(
        "openanolis/anolisos:8",
        ("EOL:2031-03-31",),
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
                "libatomic",
            ]
        ],
    ),
]
