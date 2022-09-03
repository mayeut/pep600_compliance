from pep600_compliance.images import base, package_manager


class Slackware(base.Base):
    def __init__(self, image, eol, pkg_manager, packages, python="python"):
        _, version = image.split(":")
        self._packages = packages
        super().__init__(
            image, "slackware", version, eol, pkg_manager, ["x86_64"], python=python
        )

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


SLACKWARE_LIST: list[base.Base] = [
    Slackware(
        "vbatts/slackware:current",
        "rolling",
        pkg_manager=package_manager.SLACKPKG(True),
        packages=[
            [
                "aaa_glibc-solibs",
                "python2",
                "python3",
                "cxxlibs",
                "libX11",
                "libXext",
                "libXrender",
                "mesa",
                "libICE",
                "libSM",
                "libglvnd",
            ]
        ],
        python="python3",
    ),
    Slackware(
        "vbatts/slackware:15.0",
        "unknown",
        pkg_manager=package_manager.SLACKPKG(),
        packages=[
            [
                "python2",
                "python3",
                "cxxlibs",
                "libX11",
                "libXext",
                "libXrender",
                "mesa",
                "libICE",
                "libSM",
                "libglvnd",
            ]
        ],
        python="python3",
    ),
    Slackware(
        "vbatts/slackware:14.2",
        "unknown",
        pkg_manager=package_manager.SLACKPKG(),
        packages=[
            [
                "python-2.7.17",
                "cxxlibs",
                "libX11",
                "libXext",
                "libXrender",
                "mesa",
                "libICE",
                "libSM",
            ]
        ],
    ),
    Slackware(
        "vbatts/slackware:14.1",
        "unknown",
        pkg_manager=package_manager.SLACKPKG(),
        packages=[
            [
                "python-2.7.17",
                "cxxlibs",
                "libX11",
                "libXext",
                "libXrender",
                "mesa",
                "libICE",
                "libSM",
            ]
        ],
    ),
    Slackware(
        "vbatts/slackware:14.0",
        "unknown",
        pkg_manager=package_manager.SLACKPKG(),
        packages=[
            [
                "python-2.7.17",
                "cxxlibs",
                "libX11",
                "libXext",
                "libXrender",
                "mesa",
                "libICE",
                "libSM",
            ]
        ],
    ),
]
