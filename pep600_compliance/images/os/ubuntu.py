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
    "libgl1-mesa-glx",
    "libglib2.0-0",
]
UBUNTU_LIST: list[base.Base] = [
    # EOL info: https://wiki.ubuntu.com/Releases
    Ubuntu(
        "ubuntu:devel",
        "rolling",
        machines=["x86_64", "aarch64", "ppc64le", "s390x", "armv7l", "riscv64"],
        packages=[["python3-pip"] + UBUNTU_PACKAGES],
    ),
    Ubuntu(
        "ubuntu:rolling",
        "rolling",
        machines=["x86_64", "aarch64", "ppc64le", "s390x", "armv7l", "riscv64"],
        packages=[["python3-pip"] + UBUNTU_PACKAGES],
    ),
    Ubuntu(
        "ubuntu:23.04",
        ("EOL:2024-01-31",),
        machines=["x86_64", "aarch64", "ppc64le", "s390x", "armv7l", "riscv64"],
        packages=[["python3-pip"] + UBUNTU_PACKAGES],
    ),
    Ubuntu(
        "ubuntu:22.10",
        ("EOL:2023-07-20",),
        machines=["x86_64", "aarch64", "ppc64le", "s390x", "armv7l", "riscv64"],
        packages=[["python3-pip"] + UBUNTU_PACKAGES],
    ),
    Ubuntu(
        "ubuntu:22.04",
        ("EOL:2027-04-30", "ELTS:2032-04-30"),
        machines=["x86_64", "aarch64", "ppc64le", "s390x", "armv7l", "riscv64"],
        packages=[["python3-pip"] + UBUNTU_PACKAGES],
    ),
    Ubuntu(
        "ubuntu:21.10",
        ("EOL:2022-07-31",),
        machines=["x86_64", "aarch64", "ppc64le", "s390x", "armv7l"],
        packages=[["python", "python3-pip"] + UBUNTU_PACKAGES],
    ),
    Ubuntu(
        "ubuntu:21.04",
        ("EOL:2022-01-31",),
        machines=["x86_64", "aarch64", "ppc64le", "s390x", "armv7l"],
        packages=[["python", "python3-pip"] + UBUNTU_PACKAGES],
    ),
    Ubuntu(
        "ubuntu:20.10",
        ("EOL:2021-07-17",),
        machines=["x86_64", "aarch64", "ppc64le", "s390x", "armv7l"],
        packages=[["python", "python3-pip"] + UBUNTU_PACKAGES],
    ),
    Ubuntu(
        "ubuntu:20.04",
        ("EOL:2025-04-30", "ELTS:2030-04-30"),
        machines=["x86_64", "aarch64", "ppc64le", "s390x", "armv7l", "riscv64"],
        packages=[["python", "python3-pip"] + UBUNTU_PACKAGES],
    ),
    Ubuntu(
        "ubuntu:19.10",
        ("EOL:2020-07-17",),
        machines=["i686", "x86_64", "aarch64", "ppc64le", "s390x", "armv7l"],
        packages=[["python", "python3-pip"] + UBUNTU_PACKAGES],
        apt_sources_update=UBUNTU_APT_OLD,
    ),
    Ubuntu(
        "ubuntu:19.04",
        ("EOL:2020-01-23",),
        machines=["i686", "x86_64", "aarch64", "ppc64le", "s390x", "armv7l"],
        packages=[["python", "python3-pip"] + UBUNTU_PACKAGES],
        apt_sources_update=UBUNTU_APT_OLD,
    ),
    Ubuntu(
        "ubuntu:18.10",
        ("EOL:2019-07-18",),
        machines=["i686", "x86_64", "aarch64", "ppc64le", "s390x", "armv7l"],
        packages=[["python", "python3-pip"] + UBUNTU_PACKAGES],
        apt_sources_update=UBUNTU_APT_OLD,
    ),
    Ubuntu(
        "ubuntu:18.04",
        ("EOL:2023-04-30", "ELTS:2028-04-30"),
        machines=["i686", "x86_64", "aarch64", "ppc64le", "s390x", "armv7l"],
        packages=[["python", "python3-pip"] + UBUNTU_PACKAGES],
    ),
    Ubuntu(
        "ubuntu:17.10",
        ("EOL:2018-07-19",),
        machines=["i686", "x86_64", "aarch64", "ppc64le", "s390x", "armv7l"],
        packages=[["python", "python3-pip"] + UBUNTU_PACKAGES],
        apt_sources_update=UBUNTU_APT_OLD,
    ),
    Ubuntu(
        "ubuntu:17.04",
        ("EOL:2018-01-13",),
        machines=["i686", "x86_64", "aarch64", "ppc64le", "s390x", "armv7l"],
        packages=[["python", "python3-pip"] + UBUNTU_PACKAGES],
        apt_sources_update=UBUNTU_APT_OLD,
    ),
    Ubuntu(
        "ubuntu:16.10",
        ("EOL:2017-07-20",),
        machines=["i686", "x86_64", "aarch64", "ppc64le", "s390x", "armv7l"],
        packages=[["python", "python3-pip"] + UBUNTU_PACKAGES],
        apt_sources_update=UBUNTU_APT_OLD,
    ),
    Ubuntu(
        "ubuntu:16.04",
        ("EOL:2021-04-30", "ELTS:2024-04-30"),
        machines=["i686", "x86_64", "aarch64", "ppc64le", "s390x", "armv7l"],
        packages=[["python", "python3-pip"] + UBUNTU_PACKAGES],
    ),
    Ubuntu(
        "ubuntu:15.10",
        ("EOL:2016-07-28",),
        machines=["i686", "x86_64"],
        packages=[["python", "python3-pip"] + UBUNTU_PACKAGES],
        apt_sources_update=UBUNTU_APT_OLD,
    ),
    Ubuntu(
        "ubuntu:15.04",
        ("EOL:2016-02-04",),
        machines=["i686", "x86_64"],
        packages=[["python", "python3-pip"] + UBUNTU_PACKAGES],
        apt_sources_update=UBUNTU_APT_OLD,
    ),
    Ubuntu(
        "ubuntu:14.10",
        ("EOL:2015-07-23",),
        machines=["x86_64"],
        packages=[["python", "python3-pip"] + UBUNTU_PACKAGES],
        apt_sources_update=UBUNTU_APT_OLD,
    ),
    Ubuntu(
        "ubuntu:14.04",
        ("EOL:2019-04-25", "ELTS:2022-04-30"),
        machines=["i686", "x86_64", "aarch64", "ppc64le", "armv7l"],
        packages=[["python", "python3-pip"] + UBUNTU_PACKAGES],
    ),
    Ubuntu(
        "ubuntu:13.10",
        ("EOL:2014-07-17",),
        machines=["x86_64"],
        packages=[["python", "python3-pip"] + UBUNTU_PACKAGES],
        apt_sources_update=UBUNTU_APT_OLD,
    ),
    Ubuntu(
        "ubuntu:13.04",
        ("EOL:2014-01-27",),
        machines=["x86_64"],
        packages=[["python", "python3-pip"] + UBUNTU_PACKAGES],
        apt_sources_update=UBUNTU_APT_OLD,
    ),
    Ubuntu(
        "ubuntu:12.10",
        ("EOL:2014-05-16",),
        machines=["x86_64"],
        packages=[["python", "python3.4"] + UBUNTU_PACKAGES],
        apt_sources_update=UBUNTU_APT_OLD,
        python="python3.4",
        ppa_list=UBUNTU_PYTHON_PPA,
    ),
    Ubuntu(
        "ubuntu:12.04",
        ("EOL:2017-04-28", "ELTS:2019-04-30"),
        machines=["i686", "x86_64"],
        packages=[["python", "python3.5", "curl"] + UBUNTU_PACKAGES],
        apt_sources_update=UBUNTU_APT_OLD,
        python="python3.5",
        ppa_list=UBUNTU_PYTHON_PPA,
    ),
]
