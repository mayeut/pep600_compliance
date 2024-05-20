from pep600_compliance.images import base, package_manager


class Alt(base.Base):
    def __init__(self, image, eol, packages, machines):
        _, version = image.split(":")
        self._packages = packages
        super().__init__(
            image,
            "alt",
            version,
            eol,
            package_manager.APT(has_no_install_recommends=False),
            machines=machines,
        )

    def install_packages(self, container, machine):
        super()._install_packages(container, machine, self._packages)


ALT_PACKAGES = [
    "which",
    "python-strict",
    "python3-module-pip",
    "libX11",
    "libXext",
    "libXrender",
    "libICE",
    "libSM",
    "libGL",
    "glib2",
]
ALT_LIST: list[base.Base] = [
    Alt(
        "alt:sisyphus",
        "rolling",
        machines=("i686", "x86_64", "aarch64", "ppc64le"),
        packages=[["libnsl1", "glibc-pthread"] + ALT_PACKAGES],
    ),
    Alt(
        "alt:p10",
        "unknown",
        machines=("i686", "x86_64", "aarch64", "ppc64le"),
        packages=[["libnsl1"] + ALT_PACKAGES],
    ),
    Alt(
        "alt:p9",
        "unknown",
        machines=("i686", "x86_64", "aarch64", "ppc64le"),
        packages=[["libnsl1"] + ALT_PACKAGES],
    ),
    Alt("alt:p8", "unknown", machines=("i686", "x86_64"), packages=[ALT_PACKAGES]),
]
