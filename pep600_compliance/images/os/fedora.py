from pep600_compliance.images import base
from pep600_compliance.images.package_manager import DNF, DNF5


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
    "libatomic",
]
FEDORA_LIST: list[base.Base] = [
    Fedora(
        "fedora:rawhide",
        "rolling",
        machines=("x86_64", "aarch64", "ppc64le", "s390x"),
        pkg_manager=DNF5(),
        packages=[["libnsl"] + FEDORA_PACKAGES],
    ),
    Fedora(
        "fedora:42",
        # https://fedorapeople.org/groups/schedule/f-44/f-44-key-tasks.html
        ("EOL:2026-05-13",),
        machines=("x86_64", "aarch64", "ppc64le", "s390x"),
        pkg_manager=DNF5(),
        packages=[["libnsl"] + FEDORA_PACKAGES],
    ),
    Fedora(
        "fedora:41",
        # https://fedorapeople.org/groups/schedule/f-43/f-43-key-tasks.html
        ("EOL:2025-12-15",),
        machines=("x86_64", "aarch64", "ppc64le", "s390x"),
        pkg_manager=DNF5(),
        packages=[["libnsl"] + FEDORA_PACKAGES],
    ),
    Fedora(
        "fedora:40",
        # https://fedorapeople.org/groups/schedule/f-42/f-42-key-tasks.html
        ("EOL:2025-05-13",),
        machines=("x86_64", "aarch64", "ppc64le", "s390x"),
        pkg_manager=DNF(),
        packages=[["libnsl"] + FEDORA_PACKAGES],
    ),
    Fedora(
        "fedora:39",
        # https://fedorapeople.org/groups/schedule/f-41/f-41-key-tasks.html
        ("EOL:2024-11-19",),
        machines=("x86_64", "aarch64", "ppc64le", "s390x"),
        pkg_manager=DNF(),
        packages=[["libnsl"] + FEDORA_PACKAGES],
    ),
    Fedora(
        "fedora:38",
        # https://fedorapeople.org/groups/schedule/f-40/f-40-key-tasks.html
        ("EOL:2024-05-21",),
        machines=("x86_64", "aarch64", "ppc64le", "s390x"),
        pkg_manager=DNF(),
        packages=[["libnsl"] + FEDORA_PACKAGES],
    ),
    Fedora(
        "fedora:37",
        # https://fedorapeople.org/groups/schedule/f-39/f-39-key-tasks.html
        ("EOL:2023-11-14",),
        machines=("x86_64", "aarch64", "ppc64le", "s390x"),
        pkg_manager=DNF(),
        packages=[["libnsl"] + FEDORA_PACKAGES],
    ),
    Fedora(
        "fedora:36",
        # https://fedorapeople.org/groups/schedule/f-38/f-38-key-tasks.html
        ("EOL:2023-05-16",),
        machines=("x86_64", "aarch64", "ppc64le", "s390x"),
        pkg_manager=DNF(),
        packages=[["libnsl"] + FEDORA_PACKAGES],
    ),
    Fedora(
        "fedora:35",
        # https://fedorapeople.org/groups/schedule/f-37/f-37-key-tasks.html
        ("EOL:2022-11-15",),
        machines=("x86_64", "aarch64", "ppc64le", "s390x"),
        pkg_manager=DNF(),
        packages=[["libnsl"] + FEDORA_PACKAGES],
    ),
    Fedora(
        "fedora:34",
        # https://fedorapeople.org/groups/schedule/f-36/f-36-key-tasks.html
        ("EOL:2022-05-17",),
        machines=("x86_64", "aarch64", "ppc64le", "s390x"),
        pkg_manager=DNF(),
        packages=[["libnsl"] + FEDORA_PACKAGES],
    ),
    # EOL: https://fedoraproject.org/wiki/End_of_life
    Fedora(
        "fedora:33",
        ("EOL:2021-11-16",),
        machines=("x86_64", "aarch64", "ppc64le", "s390x", "armv7l"),
        pkg_manager=DNF(),
        packages=[["libnsl"] + FEDORA_PACKAGES],
    ),
    Fedora(
        "fedora:32",
        ("EOL:2021-05-18",),
        machines=("x86_64", "aarch64", "ppc64le", "s390x", "armv7l"),
        pkg_manager=DNF(),
        packages=[["libnsl"] + FEDORA_PACKAGES],
    ),
]
