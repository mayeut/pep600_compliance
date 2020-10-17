from pep600_compliance.images import base


class Manylinux(base.Base):
    def __init__(self, image, eol, machines):
        version = image.split('/')[-1].split('_')[0][9:]
        python = '/opt/python/cp39-cp39/bin/python'
        self._packages = []
        super().__init__(image, 'manylinux', version, eol, None, machines, python=python)

    def install_packages(self, container, machine):
        pass


_MANYLINUX_2014 = [
    Manylinux(f'quay.io/pypa/manylinux2014_{machine}:latest', ('EOL:2024-06-30',), machines=[f'{machine}'])
    for machine in {'x86_64', 'i686', 'aarch64', 'ppc64le', 's390x'}
]
_MANYLINUX_2010 = [
    Manylinux(f'quay.io/pypa/manylinux2010_{machine}:latest', ('EOL:2020-11-30',), machines=[f'{machine}'])
    for machine in {'x86_64', 'i686'}
]
_MANYLINUX_1 = [
    Manylinux(f'quay.io/pypa/manylinux1_{machine}:latest', ('EOL:2017-03-31',), machines=[f'{machine}'])
    for machine in {'x86_64', 'i686'}
]
MANYLINUX_LIST = \
    _MANYLINUX_2014 + \
    _MANYLINUX_2010 + \
    _MANYLINUX_1
