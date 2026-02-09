from typing import TYPE_CHECKING

from pep600_compliance.images import base

if TYPE_CHECKING:
    from docker.models.containers import Container


class Manylinux(base.Base):
    def __init__(
        self,
        image: str,
        eol: tuple[str, ...] | str,
        machines: tuple[str, ...],
    ) -> None:
        manylinux_parts = image.rsplit("/", maxsplit=1)[-1].split("_")
        if manylinux_parts[0] == "manylinux":
            # PEP600
            version = f"{manylinux_parts[1]}_{manylinux_parts[2]}"
        else:
            # manylinux1 / manylinux2010 / manylinux2014
            version = manylinux_parts[0][9:]
        python = "/opt/python/cp39-cp39/bin/python"
        self._packages: list[list[str]] = []
        super().__init__(
            image,
            "manylinux",
            version,
            eol,
            None,
            machines,
            python=python,
        )

    def install_packages(self, container: Container, machine: str) -> None:
        pass


_MANYLINUX_2_39: list[base.Base] = [
    Manylinux(
        f"quay.io/pypa/manylinux_2_39_{machine}:latest",
        ("EOL:2035-05-31",),
        machines=(machine,),
    )
    for machine in ("aarch64", "riscv64")
]
_MANYLINUX_2_34: list[base.Base] = [
    Manylinux(
        f"quay.io/pypa/manylinux_2_34_{machine}:latest",
        ("EOL:2032-05-31",),
        machines=(machine,),
    )
    for machine in ("x86_64", "aarch64", "ppc64le", "s390x", "i686")
]
_MANYLINUX_2_31: list[base.Base] = [
    Manylinux(
        f"quay.io/pypa/manylinux_2_31_{machine}:latest",
        ("EOL:2030-04-02",),
        machines=(machine,),
    )
    for machine in ("armv7l",)
]
_MANYLINUX_2_28: list[base.Base] = [
    Manylinux(
        f"quay.io/pypa/manylinux_2_28_{machine}:latest",
        ("EOL:2029-05-31",),
        machines=(machine,),
    )
    for machine in ("x86_64", "aarch64", "ppc64le", "s390x", "i686")
]
_MANYLINUX_2_24: list[base.Base] = [
    Manylinux(
        f"quay.io/pypa/manylinux_2_24_{machine}:latest",
        ("EOL:2020-07-05", "LTS:2022-06-30"),
        machines=(machine,),
    )
    for machine in ("x86_64", "i686", "aarch64", "ppc64le", "s390x")
]
_MANYLINUX_2014: list[base.Base] = [
    Manylinux(
        f"quay.io/pypa/manylinux2014_{machine}:latest",
        ("EOL:2024-06-30",),
        machines=(machine,),
    )
    for machine in ("x86_64", "i686", "aarch64", "ppc64le", "s390x")
]
_MANYLINUX_2010: list[base.Base] = [
    Manylinux(
        f"quay.io/pypa/manylinux2010_{machine}:latest",
        ("EOL:2020-11-30",),
        machines=(machine,),
    )
    for machine in ("x86_64", "i686")
]
MANYLINUX_LIST = (
    _MANYLINUX_2_39
    + _MANYLINUX_2_34
    + _MANYLINUX_2_31
    + _MANYLINUX_2_28
    + _MANYLINUX_2_24
    + _MANYLINUX_2014
    + _MANYLINUX_2010
)
