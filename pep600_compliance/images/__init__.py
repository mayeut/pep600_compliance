from typing import TYPE_CHECKING

from pep600_compliance.images.os.almalinux import ALMALINUX_LIST
from pep600_compliance.images.os.alt import ALT_LIST
from pep600_compliance.images.os.amazonlinux import AMAZONLINUX_LIST
from pep600_compliance.images.os.anolisos import ANOLISOS_LIST
from pep600_compliance.images.os.archlinux import ARCHLINUX_LIST
from pep600_compliance.images.os.centos import CENTOS_LIST
from pep600_compliance.images.os.clefos import CLEFOS_LIST
from pep600_compliance.images.os.debian import DEBIAN_LIST
from pep600_compliance.images.os.fedora import FEDORA_LIST
from pep600_compliance.images.os.mageia import MAGEIA_LIST
from pep600_compliance.images.os.manylinux import MANYLINUX_LIST
from pep600_compliance.images.os.opencloudos import OPENCLOUDOS_LIST
from pep600_compliance.images.os.openeuler import OPENEULER_LIST
from pep600_compliance.images.os.opensuse import OPENSUSE_LIST
from pep600_compliance.images.os.oraclelinux import ORACLELINUX_LIST
from pep600_compliance.images.os.photon import PHOTON_LIST
from pep600_compliance.images.os.rhubi import RHUBI_LIST
from pep600_compliance.images.os.rockylinux import ROCKYLINUX_LIST
from pep600_compliance.images.os.slackware import SLACKWARE_LIST
from pep600_compliance.images.os.ubuntu import UBUNTU_LIST

if TYPE_CHECKING:
    from collections.abc import Iterator

    from pep600_compliance.images.base import Base

IMAGE_LIST = (
    ALMALINUX_LIST
    + ALT_LIST
    + AMAZONLINUX_LIST
    + ANOLISOS_LIST
    + ARCHLINUX_LIST
    + CENTOS_LIST
    + CLEFOS_LIST
    + DEBIAN_LIST
    + FEDORA_LIST
    + MAGEIA_LIST
    + MANYLINUX_LIST
    + OPENCLOUDOS_LIST
    + OPENEULER_LIST
    + OPENSUSE_LIST
    + ORACLELINUX_LIST
    + PHOTON_LIST
    + RHUBI_LIST
    + ROCKYLINUX_LIST
    + SLACKWARE_LIST
    + UBUNTU_LIST
)


def get_images(machine: str | None) -> Iterator[Base]:
    for image in IMAGE_LIST:
        if machine is None or machine in image.machines:
            yield image
