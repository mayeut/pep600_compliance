from pep600_compliance.images import base, package_manager


class OracleLinux(base.Base):
    def __init__(self, image, eol, pkg_manager, packages, machines, python="python3"):
        _, version = image.split(":")
        version = version.split("-")[0]
        self._packages = packages
        super().__init__(
            image,
            "oraclelinux",
            version,
            eol,
            pkg_manager,
            python=python,
            machines=machines,
        )

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


ORACLELINUX_LIST: list[base.Base] = [
    # EOL info: https://www.oracle.com/a/ocom/docs/elsp-lifetime-069338.pdf
    OracleLinux(
        "oraclelinux:10-slim",
        ("EOL:2035-06-30", "ELTS:2038-06-30"),
        machines=("x86_64", "aarch64"),
        pkg_manager=package_manager.MICRODNF(),
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
    OracleLinux(
        "oraclelinux:9-slim",
        ("EOL:2032-06-30", "ELTS:2035-06-30"),
        machines=("x86_64", "aarch64"),
        pkg_manager=package_manager.MICRODNF(),
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
    OracleLinux(
        "oraclelinux:8-slim",
        ("EOL:2029-07-31", "ELTS:2032-07-31"),
        machines=("x86_64", "aarch64"),
        pkg_manager=package_manager.MICRODNF(),
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
    OracleLinux(
        "oraclelinux:7-slim",
        ("EOL:2024-12-31", "ELTS:2028-06-30"),
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
    # Extended support
    OracleLinux(
        "oraclelinux:6-slim",
        ("EOL:2021-03-31", "ELTS:2024-12-31"),
        machines=("x86_64",),
        pkg_manager=package_manager.YUM(
            run_once=[["yum-config-manager", "--enable", "ol6_software_collections"]],
        ),
        packages=[
            [
                "which",
                "python",
                "rh-python36-python-pip",
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
