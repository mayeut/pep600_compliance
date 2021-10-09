from pep600_compliance.images import base
from pep600_compliance.images.package_manager import DNF, YUM


class Fedora(base.Base):
    def __init__(self, image, eol, pkg_manager, packages, machines):
        _, version = image.split(":")
        self._packages = packages
        super().__init__(image, "fedora", version, eol, pkg_manager, machines=machines)

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


FEDORA_PACKAGES = [
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
FEDORA_LIST: list[base.Base] = [
    Fedora(
        "fedora:rawhide",
        "rolling",
        machines=["x86_64", "aarch64"],
        pkg_manager=DNF(),
        packages=[["libnsl"] + FEDORA_PACKAGES],
    ),
    Fedora(
        "fedora:35",
        "unknown",
        machines=["x86_64", "aarch64"],
        pkg_manager=DNF(),
        packages=[["libnsl"] + FEDORA_PACKAGES],
    ),
    Fedora(
        "fedora:34",
        # https://fedorapeople.org/groups/schedule/f-36/f-36-key-tasks.html
        ("EOL:2022-05-17",),
        machines=["x86_64", "aarch64"],
        pkg_manager=DNF(),
        packages=[["libnsl"] + FEDORA_PACKAGES],
    ),
    # EOL: https://fedoraproject.org/wiki/End_of_life
    Fedora(
        "fedora:33",
        ("EOL:2021-11-16",),
        machines=["x86_64", "aarch64", "ppc64le", "s390x", "armv7l"],
        pkg_manager=DNF(),
        packages=[["libnsl"] + FEDORA_PACKAGES],
    ),
    Fedora(
        "fedora:32",
        ("EOL:2021-05-18",),
        machines=["x86_64", "aarch64", "ppc64le", "s390x", "armv7l"],
        pkg_manager=DNF(),
        packages=[["libnsl"] + FEDORA_PACKAGES],
    ),
    Fedora(
        "fedora:31",
        ("EOL:2020-11-24",),
        machines=["x86_64", "aarch64", "ppc64le", "s390x"],
        pkg_manager=DNF(),
        packages=[["libnsl"] + FEDORA_PACKAGES],
    ),
    Fedora(
        "fedora:30",
        ("EOL:2020-05-26",),
        machines=["x86_64", "aarch64", "ppc64le", "s390x"],
        pkg_manager=DNF(),
        packages=[["libnsl"] + FEDORA_PACKAGES],
    ),
    Fedora(
        "fedora:29",
        ("EOL:2019-11-26",),
        machines=["x86_64", "aarch64", "ppc64le", "s390x"],
        pkg_manager=DNF(),
        packages=[["libnsl"] + FEDORA_PACKAGES],
    ),  # TODO 'armv7l'
    Fedora(
        "fedora:28",
        ("EOL:2019-05-28",),
        machines=["x86_64", "aarch64", "ppc64le", "s390x"],
        pkg_manager=DNF(),
        packages=[["libnsl"] + FEDORA_PACKAGES],
    ),  # TODO 'armv7l'
    Fedora(
        "fedora:27",
        ("EOL:2018-11-30",),
        machines=["x86_64", "aarch64", "ppc64le"],
        pkg_manager=DNF(),
        packages=[FEDORA_PACKAGES],
    ),  # TODO 'armv7l'
    Fedora(
        "fedora:26",
        ("EOL:2018-05-29",),
        machines=["x86_64", "aarch64", "ppc64le"],
        pkg_manager=DNF(),
        packages=[FEDORA_PACKAGES],
    ),  # TODO 'armv7l'
    Fedora(
        "fedora:25",
        ("EOL:2017-12-12",),
        machines=["x86_64"],
        pkg_manager=DNF(),
        packages=[FEDORA_PACKAGES],
    ),  # TODO 'armv7l'
    Fedora(
        "fedora:24",
        ("EOL:2017-08-08",),
        machines=["x86_64"],
        pkg_manager=DNF(),
        packages=[FEDORA_PACKAGES],
    ),
    Fedora(
        "fedora:23",
        ("EOL:2016-12-20",),
        machines=["x86_64"],
        pkg_manager=DNF(),
        packages=[FEDORA_PACKAGES],
    ),
    Fedora(
        "fedora:22",
        ("EOL:2016-07-19",),
        machines=["x86_64"],
        pkg_manager=DNF(),
        packages=[FEDORA_PACKAGES],
    ),
    Fedora(
        "fedora:21",
        ("EOL:2015-12-01",),
        machines=["x86_64"],
        pkg_manager=YUM(),
        packages=[FEDORA_PACKAGES],
    ),
    Fedora(
        "fedora:20",
        ("EOL:2015-06-23",),
        machines=["x86_64"],
        pkg_manager=YUM(),
        packages=[FEDORA_PACKAGES],
    ),
]
