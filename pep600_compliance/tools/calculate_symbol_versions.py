"""
Calculate symbol_versions for a policy in policy.json by collection
defined version (.gnu.version_d) from libraries in lib_whitelist.
This should be run inside a manylinux Docker container.
"""
import argparse
import ctypes
import os
import platform
import json
import sys
from elftools.elf.elffile import ELFFile


MACHINE = platform.machine()
IS_64BITS = sys.maxsize > 2**32
if MACHINE == 'x86_64' and not IS_64BITS:
    MACHINE = 'i686'
elif MACHINE in ['i386', 'i486', 'i586']:
    MACHINE = 'i686'

if MACHINE == 'x86_64':
    LIBRARY_PATHS = [
        '/lib/x86_64-linux-gnu',
        '/usr/lib/x86_64-linux-gnu',
        '/usr/lib/x86_64-linux-gnu/mesa',
        '/lib64',
        '/usr/lib64'
    ]
elif MACHINE == 'i686':
    LIBRARY_PATHS = [
        '/lib/i386-linux-gnu',
        '/usr/lib/i386-linux-gnu',
        '/usr/lib/i386-linux-gnu/mesa',
        '/lib',
        '/usr/lib'
    ]
elif MACHINE == 'aarch64':
    LIBRARY_PATHS = [
        '/lib/aarch64-linux-gnu',
        '/usr/lib/aarch64-linux-gnu',
        '/usr/lib/aarch64-linux-gnu/mesa',
        '/lib64',
        '/usr/lib64'
    ]
elif MACHINE == 'ppc64le':
    LIBRARY_PATHS = [
        '/lib/powerpc64le-linux-gnu',
        '/usr/lib/powerpc64le-linux-gnu',
        '/usr/lib/powerpc64le-linux-gnu/mesa',
        '/lib64',
        '/usr/lib64'
    ]
elif MACHINE == 's390x':
    LIBRARY_PATHS = [
        '/lib/s390x-linux-gnu',
        '/usr/lib/s390x-linux-gnu',
        '/usr/lib/s390x-linux-gnu/mesa',
        '/lib64',
        '/usr/lib64'
    ]
elif MACHINE == 'armv7l':
    LIBRARY_PATHS = [
        '/lib/arm-linux-gnueabihf',
        '/usr/lib/arm-linux-gnueabihf',
        '/usr/lib/arm-linux-gnueabihf/mesa',
        '/lib',
        '/usr/lib'
    ]
else:
    raise NotImplementedError('Platform not supported')

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("policy", help="The policy name")
parser.add_argument("policyjson", help="The policy.json file.")
parser.add_argument(
    "skip_lib", nargs=argparse.REMAINDER, help="libraries to skip in the check"
)


def load_policies(path):
    with open(path) as f:
        return json.load(f)


def choose_policy(name, policies):
    try:
        return next(policy for policy in policies if policy['name'] == name)
    except StopIteration:
        raise RuntimeError("Unknown policy {}".format(name))


def find_library(library):
    for p in LIBRARY_PATHS:
        path = os.path.join(p, library)
        if os.path.exists(path):
            return path
    else:
        raise RuntimeError("Unknown library {}".format(library))


def versionify(version_string):
    try:
        result = [int(n) for n in version_string.split('.')]
        assert len(result) <= 3
    except ValueError:
        result = [999999, 999999, 999999, version_string]
    return result


def calculate_symbol_versions(libraries, symbol_versions, skip_lib):
    calculated_symbol_versions = {k: set() for k in symbol_versions}
    for library in libraries:
        try:
            library_path = find_library(library)
        except RuntimeError as e:
            if library in skip_lib:
                continue
            raise e
        if library in skip_lib:
            raise RuntimeError(
                "Library {} has been found but is in the skip_lib list".format(
                    library
                )
            )
        with open(library_path, 'rb') as f:
            e = ELFFile(f)
            section = e.get_section_by_name('.gnu.version_d')
            if section:
                for _, verdef_iter in section.iter_versions():
                    for vernaux in verdef_iter:
                        for _ in symbol_versions:
                            try:
                                name, version = vernaux.name.split('_', 1)
                            except ValueError:
                                pass
                            if name in calculated_symbol_versions \
                               and version != 'PRIVATE':
                                calculated_symbol_versions[name].add(version)
    return {
        k: sorted(v, key=versionify)
        for k, v in calculated_symbol_versions.items()
    }


def _glibc_version_string_ctypes():
    # type: () -> Optional[str]
    """
    Fallback implementation of glibc_version_string using ctypes.
    """

    # ctypes.CDLL(None) internally calls dlopen(NULL), and as the dlopen
    # manpage says, "If filename is NULL, then the returned handle is for the
    # main program". This way we can let the linker do the work to figure out
    # which libc our process is actually using.
    #
    # Note: typeshed is wrong here so we are ignoring this line.
    process_namespace = ctypes.CDLL(None)  # type: ignore
    gnu_get_libc_version = process_namespace.gnu_get_libc_version

    # Call gnu_get_libc_version, which returns a string like "2.5"
    gnu_get_libc_version.restype = ctypes.c_char_p
    version_str = gnu_get_libc_version()  # type: str
    # py2 / py3 compatibility:
    if not isinstance(version_str, str):
        version_str = version_str.decode("ascii")

    return version_str


def main():
    args = parser.parse_args()
    policies = load_policies(args.policyjson)
    policy = choose_policy(args.policy, policies)
    arch, _ = platform.architecture()
    print(
        json.dumps({
            'glibc_version': _glibc_version_string_ctypes(),
            'symbols': calculate_symbol_versions(
                policy['lib_whitelist'],
                policy['symbol_versions'][MACHINE],
                args.skip_lib,
            )
        }, sort_keys=True)
    )


main()
