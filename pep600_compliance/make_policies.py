import dataclasses
import json
from collections import defaultdict
from copy import deepcopy
from pathlib import Path

from pep600_compliance.images import get_images

MACHINES = {"x86_64", "i686", "aarch64", "ppc64le", "s390x", "armv7l"}
HERE = Path(__file__).resolve(strict=True).parent
OFFICIAL_POLICIES = json.loads(
    HERE.joinpath("tools", "manylinux-policy.json").read_text()
)


@dataclasses.dataclass(frozen=True)
class Distribution:
    name: str
    version: str
    glibc_version: str
    machine: str
    symbols: dict[str, set[str]]
    extra: list[str]
    libz_so_1: list[str]

    @property
    def glibc_version_tuple(self) -> tuple[int, ...]:
        return tuple(int(v) for v in self.glibc_version.split("."))


@dataclasses.dataclass
class Policy:
    glibc_version: str
    machine: str
    symbols: dict[str, set[str]]
    official: bool = False

    @property
    def glibc_version_tuple(self) -> tuple[int, ...]:
        return tuple(int(v) for v in self.glibc_version.split("."))


@dataclasses.dataclass
class Incompatibility:
    policy: str | None = None
    libs: frozenset[str] = dataclasses.field(default_factory=frozenset)


def load_distros(path: Path) -> list[Distribution]:
    result: list[Distribution] = []
    for cache_file_path in path.glob("*.json"):
        distro_parts = cache_file_path.stem.split("-", 1)
        distro_dict = json.loads(cache_file_path.read_text())
        distro = Distribution(
            name=distro_parts[0],
            version=distro_parts[1].replace("-slim", ""),
            glibc_version=distro_dict["glibc_version"],
            machine=cache_file_path.parent.name,
            symbols={k: set(v) for k, v in distro_dict["symbols"].items()},
            extra=distro_dict["extra"],
            libz_so_1=distro_dict["libz.so.1"],
        )
        result.append(distro)
    result.sort(key=lambda x: x.glibc_version_tuple)
    return result


def get_policy(
    policies: list[Policy], glibc_version: str, machine: str | None
) -> Policy | None:
    for policy in policies:
        if policy.glibc_version == glibc_version:
            return policy
    assert machine is not None
    # retrieve official policy
    for official_policy in OFFICIAL_POLICIES:
        if official_policy["name"] == f'manylinux_{"_".join(glibc_version.split("."))}':
            policy_symbols = official_policy["symbol_versions"][machine]
            new_symbols = {}
            for key in policy_symbols.keys():
                new_symbols[key] = set(policy_symbols[key])
            new_policy = Policy(
                glibc_version=glibc_version,
                machine=machine,
                symbols=new_symbols,
                official=True,
            )
            policies.append(new_policy)
            return new_policy
    return None


def make_policies(distros: list[Distribution]) -> list[Policy]:
    result: list[Policy] = []
    for distro in distros:
        policy = get_policy(result, distro.glibc_version, distro.machine)
        if policy is None:
            policy = Policy(
                glibc_version=distro.glibc_version,
                machine=distro.machine,
                symbols=deepcopy(distro.symbols),
            )
            result.append(policy)
        elif not policy.official:
            for symbol in distro.symbols.keys():
                policy.symbols[symbol] &= distro.symbols[symbol]
    # make sure symbol policies from official policies are in the next ones
    for i in range(0, len(result) - 1):
        if not result[i].official:
            continue
        official_symbols = result[i].symbols
        for j in range(i + 1, len(result)):
            for symbol in official_symbols.keys():
                result[j].symbols[symbol] |= official_symbols[symbol]
    # make sure a previous policy is compatible with the next one
    for i in range(len(result) - 1, 0, -1):
        next_symbols = result[i].symbols
        previous_symbols = result[i - 1].symbols
        for symbol in previous_symbols.keys():
            previous_symbols[symbol] &= next_symbols[symbol]
    return result


def can_create_manylinux_wheel(distro: Distribution, policy: Policy) -> bool:
    for symbol in distro.symbols.keys():
        if not policy.symbols[symbol].issuperset(distro.symbols[symbol]):
            return False
    return True


def has_symbol_conflict(distro: Distribution, policy: Policy) -> bool:
    conflicts = {}
    for symbol in distro.symbols.keys():
        conflicting_symbols = policy.symbols[symbol] - distro.symbols[symbol]
        if conflicting_symbols:
            conflicts[symbol] = conflicting_symbols
    # if conflicts:
    #     print(f"{distro.name} {distro.version} conflicts: {conflicts}")
    return bool(conflicts)


def filter_image(distro_name, distro_version):
    if distro_name not in [
        "almalinux",
        "centos",
        "clefos",
        "debian",
        "rockylinux",
        "ubuntu",
        "manylinux",
    ]:
        return True
    if distro_name == "debian":
        if distro_version in {"testing", "unstable", "experimental"}:
            return True
    if distro_name == "ubuntu":
        if distro_version in {"rolling", "devel"}:
            return True
        major, minor = (int(v) for v in distro_version.split("."))
        if major & 1:
            return True
        if minor != 4:
            return True
    return False


def make_manylinux_images(
    distros: list[Distribution], policies: list[Policy]
) -> dict[str, list[str]]:
    result: dict[str, list[str]] = defaultdict(list)
    for distro in distros:
        distro_glibc_version = distro.glibc_version_tuple
        if filter_image(distro.name, distro.version):  # keep only LTS distros
            continue
        for policy in policies:
            policy_glibc_version = policy.glibc_version_tuple
            if distro_glibc_version != policy_glibc_version:
                continue
            if distro.name == "manylinux" or can_create_manylinux_wheel(distro, policy):
                distro_description = f"{distro.name} {distro.version}"
                policy_name = "manylinux_{}_{}".format(*policy_glibc_version)
                result[policy_name].append(distro_description)
                break
    return result


def make_distros(
    distros: list[Distribution], policies: list[Policy]
) -> tuple[dict[str, list[str]], dict[str, Incompatibility]]:
    result: dict[str, list[str]] = defaultdict(list)
    incompatibilities: dict[str, Incompatibility] = defaultdict(Incompatibility)
    for distro in distros:
        distro_glibc_version = distro.glibc_version_tuple
        distro_description = f"{distro.name} {distro.version}"
        if len(distro_glibc_version) == 3:
            # using a future version, seen on fedora upcoming release
            assert distro_glibc_version[2] == 9000
            policy_name = "manylinux_{}_{}_{}".format(*distro_glibc_version)
        else:
            assert len(distro_glibc_version) == 2
            policy_name = "manylinux_{}_{}".format(*distro_glibc_version)
        result[policy_name].append(distro_description)
        policy = get_policy(policies, distro.glibc_version, None)
        assert policy is not None
        if has_symbol_conflict(distro, policy):
            incompatibilities[distro_description].policy = policy_name
        for image in get_images(None):
            if image.name == distro.name and image.version == distro.version:
                if image.skip_lib:
                    incompatibilities[distro_description].libs = image.skip_lib

    return result, incompatibilities


def manylinux_analysis(path: Path, machine: str | None):
    machines = {machine} if machine else MACHINES
    base_images_set: dict[str, set[str]] = defaultdict(set)
    distros_set: dict[str, set[str]] = defaultdict(set)
    incompatibilities: dict[str, Incompatibility] = defaultdict(Incompatibility)
    for machine_ in machines:
        machine_distros_ = load_distros(path / machine_)
        policies = make_policies(machine_distros_)
        machine_base_images = make_manylinux_images(machine_distros_, policies)
        # print(machine_)
        machine_distros, incompatibilities_machine = make_distros(
            machine_distros_, policies
        )
        incompatibilities.update(incompatibilities_machine)

        # we want a kind of intersection for base_images
        for policy_name in machine_distros.keys():
            # remove invalid base_image
            for base_image in machine_distros[policy_name]:
                if (
                    base_image in base_images_set[policy_name]
                    and base_image not in machine_base_images[policy_name]
                ):
                    base_images_set[policy_name].remove(base_image)
            # add new base_image
            for base_image in machine_base_images[policy_name]:
                if base_image not in distros_set[policy_name]:
                    base_images_set[policy_name].add(base_image)
        # update distros
        for policy_name in machine_distros.keys():
            distros_set[policy_name] |= set(machine_distros[policy_name])

    base_images = {}
    policy_names = sorted(
        base_images_set.keys(), key=lambda x: [int(v) for v in x.split("_")[1:]]
    )
    for policy_name in policy_names:
        if base_images_set[policy_name]:
            base_images[policy_name] = sorted(list(base_images_set[policy_name]))

    distros: dict[str, list[str]] = {}
    all_distros: set[str] = set()
    policy_names = sorted(
        distros_set.keys(), key=lambda x: [int(v) for v in x.split("_")[1:]]
    )
    for policy_name in policy_names:
        current_distros = distros_set[policy_name] - all_distros
        all_distros |= current_distros
        if current_distros:
            distros[policy_name] = sorted(list(current_distros))

    incompatibilities = dict(sorted(incompatibilities.items()))

    return base_images, distros, incompatibilities
