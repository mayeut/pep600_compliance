import argparse
import datetime
import json
import logging
import platform
import subprocess
import sys
import urllib.parse
from pathlib import Path

from pep600_compliance.images import get_images
from pep600_compliance.make_policies import (
    load_distros,
    make_policies,
    manylinux_analysis,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HERE = Path(__file__).resolve(strict=True).parent
CACHE_PATH = HERE / ".." / "cache"
README_PATH = HERE / ".." / "README.rst"
DETAILS_PATH = HERE / ".." / "DETAILS.rst"
EOL_PATH = HERE / ".." / "EOL.rst"
MACHINES = {"x86_64", "i686", "aarch64", "ppc64le", "s390x", "armv7l", "riscv64"}


def get_start_end(lines: list[str], start_tag: str, end_tag: str) -> tuple[int, int]:
    start = None
    end = None
    for i in range(len(lines)):
        if start_tag in lines[i]:
            start = i
        if end_tag in lines[i]:
            end = i
            break
    if start is None:
        raise LookupError(start_tag)
    if end is None:
        raise LookupError(end_tag)
    return start, end


def create_cache(machine: str, force_rolling: bool, continue_on_error: bool) -> int:
    exit_code = 0
    machine_cache_path = CACHE_PATH / machine
    machine_cache_path.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "download",
            "--no-deps",
            "--no-binary",
            ":all:",
            "-d",
            str(HERE / "tools"),
            "pyelftools==0.26",
        ]
    )
    for image in get_images(machine):
        cache_file = machine_cache_path / f"{image.name}-{image.version}.json"
        run = (not cache_file.exists()) or (force_rolling and image.eol == "rolling")
        if run:
            try:
                symbols = image.run_check(machine)
                cache_file.write_text(json.dumps(symbols, sort_keys=True))
            except BaseException as e:
                if continue_on_error:
                    exit_code |= 1
                    logger.exception(
                        f"Exception occurred while creating cache for {cache_file.stem}"
                    )
                else:
                    raise e
    return exit_code


def replace_badges(lines: list[str]) -> list[str]:
    start, end = get_start_end(lines, ".. begin distro_badges", ".. end distro_badges")
    new_lines: list[str] = []
    keys: list[str] = []
    six_months = datetime.timedelta(days=182)
    today = datetime.date.today()
    logos = {
        "centos": "centos",
        "ubuntu": "ubuntu",
        "debian": "debian",
        "fedora": "fedora",
        "rhubi": "red-hat",
        "amazonlinux": "amazon-aws",
        "oraclelinux": "oracle",
        "opensuse": "opensuse",
        "photon": "vmware",
        "archlinux": "arch-linux",
        "slackware": "slackware",
        "manylinux": "python",
    }
    for image in get_images(None):
        shortname = image.name.replace("-slim", "")
        key = f"{shortname}-{image.version}"
        if key in keys:
            continue
        keys.append(key)
        if image.eol == "rolling":
            assert isinstance(image.eol, str)
            color = "purple"
            eol = image.eol
        elif image.eol == "unknown":
            assert isinstance(image.eol, str)
            color = "lightgray"
            eol = image.eol
        else:
            assert isinstance(image.eol, tuple)
            last_eol_type, last_eol_date = image.eol[-1].split(":")
            free_eol_date = datetime.date.fromisoformat(last_eol_date)
            paid_eol_date = free_eol_date
            if last_eol_type == "ELTS":
                free_eol_date = datetime.date.fromisoformat(image.eol[-2].split(":")[1])
            eol = " / ".join([date for date in image.eol])
            if paid_eol_date < today:
                color = "black"
            elif free_eol_date < today:
                color = "red"
            elif free_eol_date > (today + six_months):
                color = "green"
            else:
                color = "yellow"
        logo = ""
        if shortname in logos.keys():
            logo = f"&logo={logos[shortname]}&logoColor=white"
        line = (
            f".. |{key}| image:: https://img.shields.io/static/v1?"
            f"label={urllib.parse.quote(shortname)}&"
            f"message={urllib.parse.quote(image.version)}%20"
            f"({urllib.parse.quote(eol)})&"
            f"color={color}{logo}"
        )
        new_lines.append(line)
    return lines[: start + 1] + new_lines + lines[end:]


def update_details():
    lines = DETAILS_PATH.read_text().splitlines()

    lines = replace_badges(lines)

    for machine in MACHINES:
        base_images, distros, _ = manylinux_analysis(CACHE_PATH, machine)
        start, end = get_start_end(
            lines, f".. begin base_images_{machine}", f".. end base_images_{machine}"
        )
        new_lines = [f".. csv-table:: {machine}", '   :header: "policy", "distros"', ""]
        for policy_name in base_images.keys():
            distros_ = " ".join(
                [f'|{d.replace(" ", "-")}|' for d in base_images[policy_name]]
            )
            line = f'   "{policy_name}", "{distros_}"'
            new_lines.append(line)
        lines = lines[: start + 1] + new_lines + lines[end:]

        start, end = get_start_end(
            lines,
            f".. begin compatibility_{machine}",
            f".. end compatibility_{machine}",
        )
        new_lines = [f".. csv-table:: {machine}", '   :header: "policy", "distros"', ""]
        for policy_name in distros.keys():
            distros_ = " ".join(
                [f'|{d.replace(" ", "-")}|' for d in distros[policy_name]]
            )
            line = f'   "{policy_name}", "{distros_}"'
            new_lines.append(line)
        lines = lines[: start + 1] + new_lines + lines[end:]

    DETAILS_PATH.write_text("\n".join(lines) + "\n")


def update_readme():
    lines = README_PATH.read_text().splitlines()

    lines = replace_badges(lines)

    base_images, distros, incompatibilities = manylinux_analysis(CACHE_PATH, None)

    start, end = get_start_end(lines, ".. begin base_images", ".. end base_images")
    new_lines = [".. csv-table:: base images", '   :header: "policy", "distros"', ""]
    for policy_name in base_images.keys():
        if base_images[policy_name]:
            distros_ = " ".join(
                [f'|{d.replace(" ", "-")}|' for d in base_images[policy_name]]
            )
            line = f'   "{policy_name}", "{distros_}"'
            new_lines.append(line)
    lines = lines[: start + 1] + new_lines + lines[end:]

    start, end = get_start_end(lines, ".. begin compatibility", ".. end compatibility")
    new_lines = [".. csv-table:: compatibility", '   :header: "policy", "distros"', ""]
    for policy_name in distros.keys():
        distros_ = " ".join([f'|{d.replace(" ", "-")}|' for d in distros[policy_name]])
        line = f'   "{policy_name}", "{distros_}"'
        new_lines.append(line)
    lines = lines[: start + 1] + new_lines + lines[end:]

    start, end = get_start_end(
        lines, ".. begin compatibility_issues", ".. end compatibility_issues"
    )
    new_lines = [
        ".. csv-table:: Compatibility Issues",
        '   :header: "distro", "incompatible policy", "unavailable libraries"',
        "",
    ]
    for distro in incompatibilities.keys():
        name = f'|{distro.replace(" ", "-")}|'
        policy = incompatibilities[distro].policy or ""
        libraries = ", ".join(sorted(incompatibilities[distro].libs))
        line = f'   "{name}", "{policy}", "{libraries}"'
        new_lines.append(line)
    lines = lines[: start + 1] + new_lines + lines[end:]

    README_PATH.write_text("\n".join(lines) + "\n")


def update_eol():
    lines = EOL_PATH.read_text().splitlines()
    start, end = get_start_end(
        lines, ".. begin eol_information", ".. end eol_information"
    )
    old_name = ""
    new_lines: list[str] = []
    done: set[str] = set()
    for image in get_images(None):
        shortname = image.name.replace("-slim", "")
        if shortname != old_name:
            old_name = shortname
            new_lines.extend(
                [
                    f".. csv-table:: {shortname}",
                    '   :header: "distro", "EOL", "LTS", "ELTS"',
                    "",
                ]
            )
        distro_version = f"{shortname} {image.version}"
        if distro_version in done:
            continue
        done.add(distro_version)
        dates = {
            "EOL": "",
            "LTS": "",
            "ELTS": "",
        }
        if image.eol in {"rolling", "unknown"}:
            dates["EOL"] = image.eol
        else:
            for eol_info in image.eol:
                kind, date = eol_info.split(":")
                dates[kind] = date
        line = (
            f'   "{distro_version}",'
            f' "{dates["EOL"]}", "{dates["LTS"]}", "{dates["ELTS"]}"'
        )
        new_lines.append(line)
    lines = lines[: start + 1] + new_lines + lines[end:]

    EOL_PATH.write_text("\n".join(lines) + "\n")


def versionify(version_string: str) -> tuple[int | str, ...]:
    try:
        result = tuple(int(n) for n in version_string.split("."))
        assert len(result) <= 4
    except ValueError:
        return 999999, 999999, 999999, version_string
    return result


def get_zlib_blacklist(min_glibc_version):
    zlib_symbols = {}
    for machine in ["i686", "x86_64", "aarch64", "s390x", "armv7l", "ppc64le"]:
        cache_path = CACHE_PATH / machine
        distros = load_distros(cache_path)
        for distro in distros:
            glibc_version = distro.glibc_version_tuple
            zlib_versions = distro.symbols["ZLIB"]
            zlib_version = "-1" if len(zlib_versions) == 0 else zlib_versions[-1]
            symbols = [symbol.split("@")[0] for symbol in distro.libz_so_1]
            if zlib_version not in zlib_symbols:
                zlib_symbols[zlib_version] = {"union": set()}
            zlib_symbols[zlib_version]["union"] |= set(symbols)
            if glibc_version >= min_glibc_version:
                if "inter" not in zlib_symbols[zlib_version]:
                    zlib_symbols[zlib_version]["inter"] = set(symbols)
                else:
                    zlib_symbols[zlib_version]["inter"] &= set(symbols)
    keys = list(zlib_symbols.keys())
    keys.sort(key=versionify, reverse=True)
    for i in range(len(keys) - 1):
        if "inter" in zlib_symbols[keys[i + 1]]:
            zlib_symbols[keys[i + 1]]["inter"] &= zlib_symbols[keys[i]]["inter"]
    keys.sort(key=versionify)
    for i in range(len(keys) - 1):
        zlib_symbols[keys[i + 1]]["union"] |= zlib_symbols[keys[i]]["union"]
    blacklist = set()
    for key in keys:
        if "inter" in zlib_symbols[key]:
            blacklist |= zlib_symbols[key]["union"] - zlib_symbols[key]["inter"]
    return sorted(blacklist)


def print_zlib_blacklist():
    print(f"zlib blacklist: {get_zlib_blacklist((2, 35))}")


def create_policy(glibc_version):
    machines = ["i686", "x86_64", "aarch64", "ppc64le", "s390x", "armv7l"]
    policy = {
        "name": f"manylinux_{glibc_version.replace('.', '_')}",
        "aliases": [],
        "priority": 64,
        "symbol_versions": {},
        "lib_whitelist": [
            "libgcc_s.so.1",
            "libstdc++.so.6",
            "libm.so.6",
            "libdl.so.2",
            "librt.so.1",
            "libc.so.6",
            "libnsl.so.1",
            "libutil.so.1",
            "libpthread.so.0",
            "libX11.so.6",
            "libXext.so.6",
            "libXrender.so.1",
            "libICE.so.6",
            "libSM.so.6",
            "libGL.so.1",
            "libgobject-2.0.so.0",
            "libgthread-2.0.so.0",
            "libglib-2.0.so.0",
            "libresolv.so.2",
            "libexpat.so.1",
            "libz.so.1",
        ],
        "blacklist": {
            "libz.so.1": get_zlib_blacklist(
                tuple(int(part) for part in glibc_version.split("."))
            ),
        },
    }
    for machine in machines:
        cache_path = CACHE_PATH / machine
        distros = load_distros(cache_path)
        policies = make_policies(distros)
        try:
            machine_policy = next(
                policy_
                for policy_ in policies
                if policy_.glibc_version == glibc_version
            )
        except StopIteration:
            continue
        policy["symbol_versions"][machine] = {
            k: sorted(machine_policy.symbols[k], key=lambda x: versionify(x))
            for k in sorted(machine_policy.symbols.keys())
        }
    print(json.dumps(policy))


def main():
    platform_machine = platform.machine()
    platform_machine = {"arm64": "aarch64"}.get(platform_machine, platform_machine)
    default_machine = [platform_machine]
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--force-rolling", action="store_true")
    parser.add_argument("-c", "--continue-on-error", action="store_true")
    parser.add_argument("--machine", nargs="*", default=default_machine)
    args = parser.parse_args()
    exit_code = 0
    for machine in args.machine:
        exit_code |= create_cache(machine, args.force_rolling, args.continue_on_error)
        base_images, _, _ = manylinux_analysis(CACHE_PATH, machine)
        for policy_name in base_images.keys():
            distros_ = base_images[policy_name]
            print(f"{policy_name}: {distros_}")
    update_readme()
    update_details()
    update_eol()
    # print_zlib_blacklist()
    # create_policy("2.34")
    exit(exit_code)


if __name__ == "__main__":
    main()
