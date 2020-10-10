from pep600_compliance.images import base
from pep600_compliance.images import package_manager


class Manylinux(base.Base):
    def __init__(self, image, machines):
        name = 'manylinux'
        version = image.split('/')[-1].split('_')[0][9:]
        python = '/opt/python/cp39-cp39/bin/python'
        self._packages = []
        super().__init__(image, name, version, None, machines, python=python)

    def install_packages(self, container, machine):
        pass


_MANYLINUX_2014 = [
    Manylinux(f'quay.io/pypa/manylinux2014_{machine}:latest', machines=[f'{machine}'])
    for machine in {'x86_64', 'i686', 'aarch64', 'ppc64le', 's390x'}
]

_MANYLINUX_2010 = [
    Manylinux(f'quay.io/pypa/manylinux2010_{machine}:latest', machines=[f'{machine}'])
    for machine in {'x86_64', 'i686'}
]

_MANYLINUX_1 = [
    Manylinux(f'quay.io/pypa/manylinux1_{machine}:latest', machines=[f'{machine}'])
    for machine in {'x86_64', 'i686'}
]

MANYLINUX_LIST = \
    _MANYLINUX_2014 + \
    _MANYLINUX_2010 + \
    _MANYLINUX_1
