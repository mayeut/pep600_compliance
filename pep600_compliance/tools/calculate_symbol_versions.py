"""
Calculate symbol_versions for a policy in policy.json by collection
defined version (.gnu.version_d) from libraries in lib_whitelist.
This should be run inside a manylinux Docker container.
"""
import argparse
import ctypes
import json
import os
import platform
import sys

from elftools.elf.dynamic import DynamicSection
from elftools.elf.elffile import ELFFile
from elftools.elf.gnuversions import (
    GNUVerDefSection,
    GNUVerNeedSection,
    GNUVerSymSection,
)
from elftools.elf.sections import SymbolTableSection

MACHINE = platform.machine()
IS_64BITS = sys.maxsize > 2 ** 32
if MACHINE == "x86_64" and not IS_64BITS:
    MACHINE = "i686"
elif MACHINE in ["i386", "i486", "i586"]:
    MACHINE = "i686"

if MACHINE == "x86_64":
    LIBRARY_PATHS = [
        "/lib/x86_64-linux-gnu",
        "/usr/lib/x86_64-linux-gnu",
        "/usr/lib/x86_64-linux-gnu/mesa",
        "/lib64",
        "/usr/lib64",
    ]
elif MACHINE == "i686":
    LIBRARY_PATHS = [
        "/lib/i386-linux-gnu",
        "/usr/lib/i386-linux-gnu",
        "/usr/lib/i386-linux-gnu/mesa",
        "/lib",
        "/usr/lib",
    ]
elif MACHINE == "aarch64":
    LIBRARY_PATHS = [
        "/lib/aarch64-linux-gnu",
        "/usr/lib/aarch64-linux-gnu",
        "/usr/lib/aarch64-linux-gnu/mesa",
        "/lib64",
        "/usr/lib64",
    ]
elif MACHINE == "ppc64le":
    LIBRARY_PATHS = [
        "/lib/powerpc64le-linux-gnu",
        "/usr/lib/powerpc64le-linux-gnu",
        "/usr/lib/powerpc64le-linux-gnu/mesa",
        "/lib64",
        "/usr/lib64",
    ]
elif MACHINE == "s390x":
    LIBRARY_PATHS = [
        "/lib/s390x-linux-gnu",
        "/usr/lib/s390x-linux-gnu",
        "/usr/lib/s390x-linux-gnu/mesa",
        "/lib64",
        "/usr/lib64",
    ]
elif MACHINE == "armv7l":
    LIBRARY_PATHS = [
        "/lib/arm-linux-gnueabihf",
        "/usr/lib/arm-linux-gnueabihf",
        "/usr/lib/arm-linux-gnueabihf/mesa",
        "/lib",
        "/usr/lib",
    ]
elif MACHINE == "riscv64":
    LIBRARY_PATHS = [
        "/lib/riscv64-linux-gnu",
        "/usr/lib/riscv64-linux-gnu",
        "/usr/lib/riscv64-linux-gnu/mesa",
        "/lib64",
        "/usr/lib64",
    ]
elif MACHINE == "loongarch64":
    LIBRARY_PATHS = [
        "/lib/loongarch64-linux-gnu",
        "/usr/lib/loongarch64-linux-gnu",
        "/usr/lib/loongarch64-linux-gnu/mesa",
        "/lib64",
        "/usr/lib64",
    ]
else:
    raise NotImplementedError("Platform not supported")

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
        return next(policy for policy in policies if policy["name"] == name)
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
        result = [int(n) for n in version_string.split(".")]
        assert len(result) <= 4
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
                "Library {} has been found but is in the skip_lib list".format(library)
            )
        with open(library_path, "rb") as f:
            elf = ELFFile(f)
            section = elf.get_section_by_name(".gnu.version_d")
            if section:
                for _, verdef_iter in section.iter_versions():
                    for vernaux in verdef_iter:
                        for _ in symbol_versions:
                            try:
                                name, version = vernaux.name.split("_", 1)
                            except ValueError:
                                continue
                            if (
                                name in calculated_symbol_versions
                                and version != "PRIVATE"
                            ):
                                calculated_symbol_versions[name].add(version)
    return {k: sorted(v, key=versionify) for k, v in calculated_symbol_versions.items()}


def _glibc_version_string_ctypes():
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


def _symbol_version(versioninfo, nsym):
    symbol_version = dict.fromkeys(("index", "name", "filename", "hidden"))

    if not versioninfo["versym"] or nsym >= versioninfo["versym"].num_symbols():
        return None

    symbol = versioninfo["versym"].get_symbol(nsym)
    index = symbol.entry["ndx"]
    if index not in ("VER_NDX_LOCAL", "VER_NDX_GLOBAL"):
        index = int(index)

        if versioninfo["type"] == "GNU":
            # In GNU versioning mode, the highest bit is used to
            # store whether the symbol is hidden or not
            if index & 0x8000:
                index &= ~0x8000
                symbol_version["hidden"] = True

        if versioninfo["verdef"] and index <= versioninfo["verdef"].num_versions():
            _, verdaux_iter = versioninfo["verdef"].get_version(index)
            symbol_version["name"] = next(verdaux_iter).name
        else:
            verneed, vernaux = versioninfo["verneed"].get_version(index)
            symbol_version["name"] = vernaux.name
            symbol_version["filename"] = verneed.name

    symbol_version["index"] = index
    return symbol_version


def _get_symbols(library):
    library_path = find_library(library)
    with open(library_path, "rb") as f:
        e = ELFFile(f)

        version_info = {"versym": None, "verdef": None, "verneed": None, "type": None}
        for section in e.iter_sections():
            if isinstance(section, GNUVerSymSection):
                version_info["versym"] = section
            elif isinstance(section, GNUVerDefSection):
                version_info["verdef"] = section
            elif isinstance(section, GNUVerNeedSection):
                version_info["verneed"] = section
            elif isinstance(section, DynamicSection):
                for tag in section.iter_tags():
                    if tag["d_tag"] == "DT_VERSYM":
                        version_info["type"] = "GNU"
                        break
        if not version_info["type"] and (
            version_info["verneed"] or version_info["verdef"]
        ):
            version_info["type"] = "Solaris"

        assert version_info["type"] == "GNU"

        symbol_tables = [
            (idx, s)
            for idx, s in enumerate(e.iter_sections())
            if isinstance(s, SymbolTableSection)
        ]
        symbols = []
        for section_index, section in symbol_tables:
            for nsym, symbol in enumerate(section.iter_symbols()):
                version_str = ""
                version = _symbol_version(version_info, nsym)
                if version is None or version["name"] == symbol.name:
                    continue
                if version["index"] not in ("VER_NDX_LOCAL", "VER_NDX_GLOBAL"):
                    if version["filename"]:
                        # external symbol
                        version_str = "@%(name)s (%(index)i)" % version
                    else:
                        # internal symbol
                        if version["hidden"]:
                            version_str = "@%(name)s" % version
                        else:
                            version_str = "@@%(name)s" % version
                if symbol["st_info"]["bind"] == "STB_LOCAL":
                    continue
                if symbol["st_other"]["visibility"] == "STV_HIDDEN":
                    continue
                if symbol["st_shndx"] == "SHN_UNDEF":
                    continue
                if symbol.name in {"__bss_start", "_end", "_edata", "_fini", "_init"}:
                    continue
                symbols.append("{}{}".format(symbol.name, version_str))
    return sorted(symbols)


def main():
    args = parser.parse_args()
    policies = load_policies(args.policyjson)
    policy = choose_policy(args.policy, policies)
    arch, _ = platform.architecture()
    skip_lib = set(args.skip_lib)
    if MACHINE not in {"x86_64", "aarch64"}:
        skip_lib.add("libmvec.so.1")
    if MACHINE == "loongarch64":
        skip_lib.add("libanl.so.1")
        skip_lib.add("libnsl.so.1")
        skip_lib.add("libutil.so.1")
    print(
        json.dumps(
            {
                "glibc_version": _glibc_version_string_ctypes(),
                "symbols": calculate_symbol_versions(
                    policy["lib_whitelist"],
                    policy["symbol_versions"][MACHINE],
                    skip_lib,
                ),
                "libz.so.1": _get_symbols("libz.so.1"),
            },
            sort_keys=True,
        )
    )


main()
