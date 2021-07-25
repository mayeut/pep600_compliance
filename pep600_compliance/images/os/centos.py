from pep600_compliance.images import base, package_manager


class CentOS(base.Base):
    def __init__(self, image, eol, pkg_manager, packages, machines):
        _, version = image.split(":")
        if "-development" in version:
            version = version.replace("-development", "")
        self._packages = packages
        super().__init__(image, "centos", version, eol, pkg_manager, machines)

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


CENTOS_YUM_OLD = [
    [
        "sed",
        "-i",
        "s/enabled=1/enabled=0/g",
        "/etc/yum/pluginconf.d/fastestmirror.conf",
    ],
    ["bash", "-ec", "sed -i 's/^mirrorlist/#mirrorlist/g' /etc/yum.repos.d/*.repo"],
    [
        "bash",
        "-ec",
        "sed -i "
        "'s;^#baseurl=http://mirror;baseurl=https://vault;g' /etc/yum.repos.d/*.repo",
    ],
]

CENTOS_LIST: list[base.Base] = [
    CentOS(
        "quay.io/centos/centos:stream9-development",
        "rolling",
        machines=["x86_64", "aarch64"],  # TODO "ppc64le", "s390x"
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
    CentOS(
        "centos:8",
        ("EOL:2029-05-31",),
        machines=["x86_64", "aarch64", "ppc64le"],
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
    CentOS(
        "centos:7",
        ("EOL:2024-06-30",),
        machines=["i686", "x86_64", "aarch64", "ppc64le"],
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
            ]
        ],
    ),
    CentOS(
        "centos:6",
        ("EOL:2020-11-30",),
        machines=["i686", "x86_64"],
        pkg_manager=package_manager.YUM(run_once=CENTOS_YUM_OLD),
        packages=[
            ["epel-release"],
            [
                "which",
                "python",
                "python34",
                "libstdc++",
                "glib2",
                "libX11",
                "libXext",
                "libXrender",
                "mesa-libGL",
                "libICE",
                "libSM",
            ],
        ],
    ),
]
