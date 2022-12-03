from pep600_compliance.images import base, package_manager


class Mageia(base.Base):
    def __init__(self, image, eol, pkg_manager, packages, machines):
        _, version = image.split(":")
        self._packages = packages
        super().__init__(image, "mageia", version, eol, pkg_manager, machines)

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


MAGEIA_PACKAGES = [
    "which",
    "python",
    "python3-pip",
    "libstdc++",
    "glib2",
    "libx11",
    "libxext",
    "libxrender",
    "libmesagl",
    "libice",
    "libsm",
]
MAGEIA_ARCHIVE = "https://distrib-coffee.ipsl.jussieu.fr/pub/linux/Mageia-archive"
MAGEIA6_RUNONCE = [
    "sed -i 's;mirrorlist=.*;#mirrorlist=;g' /etc/yum.repos.d/mageia-x86_64.repo",
    f"sed -i 's;#baseurl=https://mirrors.kernel.org/mageia;baseurl={MAGEIA_ARCHIVE};g' "
    "/etc/yum.repos.d/mageia-x86_64.repo",
]
MAGEIA5_RUNONCE = [
    f"sed -i 's;mirrorlist:.*;mirrorlist: {MAGEIA_ARCHIVE}/distrib/5/x86_64;g' "
    "/etc/urpmi/urpmi.cfg",
]
MAGEIA_LIST: list[base.Base] = [
    Mageia(
        "mageia:cauldron",
        "rolling",
        machines=["x86_64", "aarch64"],
        pkg_manager=package_manager.DNF(),
        packages=[
            MAGEIA_PACKAGES
            + ["libgcc1-1[2-9].*", "lib64zlib1-1.2.1[3-9]*", "libstdc++6-1[2-9].*"]
        ],
    ),  # TODO 'armv7l'
    # eol info https://www.mageia.org/en/support/
    Mageia(
        "mageia:8",
        ("EOL:2023-03-31",),
        machines=["x86_64", "aarch64"],
        pkg_manager=package_manager.DNF(),
        packages=[MAGEIA_PACKAGES],
    ),  # TODO 'armv7l'
    Mageia(
        "mageia:7",
        ("EOL:2021-05-26",),
        machines=["x86_64", "aarch64"],
        pkg_manager=package_manager.DNF(),
        packages=[MAGEIA_PACKAGES],
    ),  # TODO 'armv7l'
    Mageia(
        "mageia:6",
        ("EOL:2019-09-30",),
        machines=["x86_64"],
        pkg_manager=package_manager.DNF(run_once=MAGEIA6_RUNONCE),
        packages=[MAGEIA_PACKAGES],
    ),  # TODO 'armv7l'
    Mageia(
        "mageia:5",
        ("EOL:2017-12-31",),
        machines=["x86_64"],
        pkg_manager=package_manager.URPM(run_once=MAGEIA5_RUNONCE),
        packages=[MAGEIA_PACKAGES],
    ),
]
