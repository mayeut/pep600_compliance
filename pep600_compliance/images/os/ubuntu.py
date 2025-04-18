from pep600_compliance.images import base, package_manager


class Ubuntu(base.Base):
    def __init__(
        self,
        image,
        eol,
        machines,
        packages,
        apt_sources_update=[],
        ppa_list=[],
        python="python3",
    ):
        _, version = image.split(":")
        self._packages = packages
        super().__init__(
            image,
            "ubuntu",
            version,
            eol,
            package_manager.APT(run_once=apt_sources_update, ppa_list=ppa_list),
            machines=machines,
            python=python,
        )

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


UBUNTU_APT_OLD = [
    [
        "sed",
        "-i",
        "s,archive.ubuntu.com,old-releases.ubuntu.com,g",
        "/etc/apt/sources.list",
    ],
    [
        "sed",
        "-i",
        "s,security.ubuntu.com,old-releases.ubuntu.com,g",
        "/etc/apt/sources.list",
    ],
    [
        "sed",
        "-i",
        "s,ports.ubuntu.com/ubuntu-ports,old-releases.ubuntu.com/ubuntu,g",
        "/etc/apt/sources.list",
    ],
]
UBUNTU_PYTHON_PPA = ["ppa:fkrull/deadsnakes"]

UBUNTU_PACKAGES = [
    "libx11-6",
    "libxext6",
    "libxrender1",
    "libice6",
    "libsm6",
    "libgl1",
    "libglib2.0-0t64",
    "libatomic1",
]
UBUNTU_PACKAGES_OLD = [
    "libx11-6",
    "libxext6",
    "libxrender1",
    "libice6",
    "libsm6",
    "libgl1",
    "libglib2.0-0",
    "libatomic1",
]

UBUNTU_LIST: list[base.Base] = [
    # EOL info: https://wiki.ubuntu.com/Releases
    Ubuntu(
        "ubuntu:devel",
        "rolling",
        machines=("x86_64", "aarch64", "ppc64le", "s390x", "armv7l", "riscv64"),
        packages=[["python3-pip", *UBUNTU_PACKAGES]],
    ),
    Ubuntu(
        "ubuntu:rolling",
        "rolling",
        machines=("x86_64", "aarch64", "ppc64le", "s390x", "armv7l", "riscv64"),
        packages=[["python3-pip", *UBUNTU_PACKAGES]],
    ),
    Ubuntu(
        "ubuntu:25.04",
        ("EOL:2026-01-31",),
        machines=("x86_64", "aarch64", "ppc64le", "s390x", "armv7l", "riscv64"),
        packages=[["python3-pip", *UBUNTU_PACKAGES]],
    ),
    Ubuntu(
        "ubuntu:24.10",
        ("EOL:2025-07-11",),
        machines=("x86_64", "aarch64", "ppc64le", "s390x", "armv7l"),
        packages=[["python3-pip", *UBUNTU_PACKAGES]],
    ),
    Ubuntu(
        "ubuntu:24.04",
        ("EOL:2029-04-30", "ELTS:2036-04-30"),
        machines=("x86_64", "aarch64", "ppc64le", "s390x", "armv7l", "riscv64"),
        packages=[["python3-pip", *UBUNTU_PACKAGES]],
    ),
    Ubuntu(
        "ubuntu:23.10",
        ("EOL:2024-07-14",),
        machines=("x86_64", "aarch64", "ppc64le", "s390x", "armv7l"),
        packages=[["python3-pip", *UBUNTU_PACKAGES_OLD]],
        apt_sources_update=UBUNTU_APT_OLD,
    ),
    Ubuntu(
        "ubuntu:23.04",
        ("EOL:2024-01-31",),
        machines=("x86_64", "aarch64", "ppc64le", "s390x", "armv7l", "riscv64"),
        packages=[["python3-pip", *UBUNTU_PACKAGES_OLD]],
        apt_sources_update=UBUNTU_APT_OLD,
    ),
    Ubuntu(
        "ubuntu:22.10",
        ("EOL:2023-07-20",),
        machines=("x86_64", "aarch64", "ppc64le", "s390x", "armv7l", "riscv64"),
        packages=[["python3-pip", *UBUNTU_PACKAGES_OLD]],
        apt_sources_update=UBUNTU_APT_OLD,
    ),
    Ubuntu(
        "ubuntu:22.04",
        ("EOL:2027-04-30", "ELTS:2032-04-09"),
        machines=("x86_64", "aarch64", "ppc64le", "s390x", "armv7l", "riscv64"),
        packages=[["python3-pip", *UBUNTU_PACKAGES_OLD]],
    ),
    Ubuntu(
        "ubuntu:21.10",
        ("EOL:2022-07-31",),
        machines=("x86_64", "aarch64", "ppc64le", "s390x", "armv7l"),
        packages=[["python", "python3-pip", *UBUNTU_PACKAGES_OLD]],
        apt_sources_update=UBUNTU_APT_OLD,
    ),
    Ubuntu(
        "ubuntu:21.04",
        ("EOL:2022-01-31",),
        machines=("x86_64", "aarch64", "ppc64le", "s390x", "armv7l"),
        packages=[["python", "python3-pip", *UBUNTU_PACKAGES_OLD]],
        apt_sources_update=UBUNTU_APT_OLD,
    ),
    Ubuntu(
        "ubuntu:20.10",
        ("EOL:2021-07-17",),
        machines=("x86_64", "aarch64", "ppc64le", "s390x", "armv7l"),
        packages=[["python", "python3-pip", *UBUNTU_PACKAGES_OLD]],
        apt_sources_update=UBUNTU_APT_OLD,
    ),
    Ubuntu(
        "ubuntu:20.04",
        ("EOL:2025-04-02", "ELTS:2030-04-02"),
        machines=("x86_64", "aarch64", "ppc64le", "s390x", "armv7l", "riscv64"),
        packages=[["python", "python3-pip", *UBUNTU_PACKAGES_OLD]],
    ),
    Ubuntu(
        "ubuntu:18.04",
        ("EOL:2023-05-31", "ELTS:2028-04-01"),
        machines=("i686", "x86_64", "aarch64", "ppc64le", "s390x", "armv7l"),
        packages=[["python", "python3-pip", *UBUNTU_PACKAGES_OLD]],
    ),
    Ubuntu(
        "ubuntu:16.04",
        ("EOL:2021-04-30", "ELTS:2024-04-30"),
        machines=("i686", "x86_64", "aarch64", "ppc64le", "s390x", "armv7l"),
        packages=[["python", "python3-pip", *UBUNTU_PACKAGES_OLD]],
    ),
    Ubuntu(
        "ubuntu:14.04",
        ("EOL:2019-04-25", "ELTS:2022-04-30"),
        machines=("i686", "x86_64", "aarch64", "ppc64le", "armv7l"),
        packages=[
            [
                "python",
                "python3-pip",
                "libx11-6",
                "libxext6",
                "libxrender1",
                "libice6",
                "libsm6",
                "libgl1-mesa-glx",
                "libglib2.0-0",
                "libatomic1",
            ]
        ],
    ),
]
