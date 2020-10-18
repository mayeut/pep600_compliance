import json
import os

from collections import defaultdict
from glob import glob
from pep600_compliance.images import get_images


MACHINES = {'x86_64', 'i686', 'aarch64', 'ppc64le', 's390x', 'armv7l'}
HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, 'tools', 'policy.json'), 'rb') as f:
    OFFICIAL_POLICIES = json.load(f)


def load_distros(path):
    result = []
    for path in glob(os.path.join(path, '*.json')):
        filename, _ = os.path.splitext(os.path.basename(path))
        distro_parts = filename.split('-', 1)
        distro_name = distro_parts[0]
        distro_version = distro_parts[1].replace('-slim', '')
        try:
            with open(path, 'rt') as f:
                distro_dict = json.load(f)
        except:
            raise
        distro_dict['distro_name'] = distro_name
        distro_dict['distro_version'] = distro_version
        result.append(distro_dict)

    result.sort(
        key=lambda x: tuple([int(v) for v in x['glibc_version'].split('.')])
    )
    return result


def get_policy(policies, glibc_version, machine):
    for policy in policies:
        if policy['glibc_version'] == glibc_version:
            return policy
    # retrieve official policy
    for policy in OFFICIAL_POLICIES:
        if policy['name'] == f'manylinux_{"_".join(glibc_version.split("."))}':
            policy_symbols = policy['symbol_versions'][machine]
            new_symbols = {}
            for key in policy_symbols.keys():
                new_symbols[key] = set(policy_symbols[key])
            new_policy = {
                'glibc_version': glibc_version,
                'symbols': new_symbols,
                'official': True,
            }
            policies.append(new_policy)
            return new_policy
    return None


def make_policies(distros, machine):
    result = []
    for distro in distros:
        glibc_version = distro['glibc_version']
        policy = get_policy(result, glibc_version, machine)
        if policy is None:
            policy = {
                'glibc_version': glibc_version,
                'symbols': {},
                'official': False,
            }
            symbols = policy['symbols']
            for symbol in distro['symbols'].keys():
                symbols[symbol] = set(distro['symbols'][symbol])
            result.append(policy)
        elif not policy['official']:
            symbols = policy['symbols']
            for symbol in distro['symbols'].keys():
                symbols[symbol] &= set(distro['symbols'][symbol])
    # make sure a previous policy is compatible with the next one
    for i in range(len(result) - 1, 0, -1):
        next_symbols = result[i]['symbols']
        previous_symbols = result[i - 1]['symbols']
        for symbol in previous_symbols.keys():
            previous_symbols[symbol] &= next_symbols[symbol]
    return result


def can_create_manylinux_wheel(distro, policy):
    distro_symbols = distro['symbols']
    policy_symbols = policy['symbols']
    for symbol in distro_symbols.keys():
        if not policy_symbols[symbol].issuperset(set(distro_symbols[symbol])):
            return False
    return True


def has_symbol_conflict(distro, policy):
    distro_symbols = distro['symbols']
    policy_symbols = policy['symbols']
    for symbol in distro_symbols.keys():
        if not policy_symbols[symbol].issubset(set(distro_symbols[symbol])):
            return True
    return False


def filter_image(distro_name, distro_version):
    if distro_name not in ['centos', 'clefos', 'debian', 'ubuntu', 'manylinux']:
        return True
    if distro_name == 'debian':
        if distro_version in {'testing', 'unstable'}:
            return True
    if distro_name == 'ubuntu':
        major, minor = [int(v) for v in distro_version.split('.')]
        if major & 1:
            return True
        if minor != 4:
            return True
    return False


def make_manylinux_images(distros, policies):
    result = defaultdict(list)
    for distro in distros:
        distro_name = distro['distro_name']
        distro_version = distro['distro_version']
        distro_glibc_version = tuple(
            [int(v) for v in distro['glibc_version'].split('.')]
        )
        if filter_image(distro_name, distro_version):  # keep only LTS distros
            continue
        for policy in policies:
            policy_glibc_version = tuple(
                [int(v) for v in policy['glibc_version'].split('.')])
            if distro_glibc_version != policy_glibc_version:
                continue
            if can_create_manylinux_wheel(distro, policy):
                distro_description = '{} {}'.format(distro_name, distro_version)
                policy_name = 'manylinux_{}_{}'.format(*policy_glibc_version)
                result[policy_name].append(distro_description)
                break
    return result


def make_distros(distros, policies):
    result = defaultdict(list)
    incompatibilities = defaultdict(dict)
    for distro in distros:
        distro_name = distro['distro_name']
        distro_version = distro['distro_version']
        distro_glibc_version = tuple(
            [int(v) for v in distro['glibc_version'].split('.')]
        )
        distro_description = f'{distro_name} {distro_version}'
        if len(distro_glibc_version) == 3:
            # using a future version, seen on fedora upcoming release
            assert distro_glibc_version[2] == 9000
            policy_name = 'manylinux_{}_{}_{}'.format(*distro_glibc_version)
        else:
            assert len(distro_glibc_version) == 2
            policy_name = 'manylinux_{}_{}'.format(*distro_glibc_version)
        result[policy_name].append(distro_description)
        glibc_version = distro['glibc_version']
        policy = get_policy(policies, glibc_version, None)
        if has_symbol_conflict(distro, policy):
            incompatibilities[distro_description]['policy'] = \
                f'{policy_name}'
        for image in get_images(None):
            if image.name == distro_name and image.version == distro_version:
                if image.skip_lib:
                    incompatibilities[distro_description]['lib'] = \
                        image.skip_lib

    return result, incompatibilities


def manylinux_analysis(path, machine):
    machines = {machine} if machine else MACHINES
    base_images_set = defaultdict(set)
    distros_set = defaultdict(set)
    incompatibilities = defaultdict(dict)
    for machine_ in machines:
        cache_path = os.path.join(path, machine_)
        machine_distros = load_distros(cache_path)
        policies = make_policies(machine_distros, machine_)
        machine_base_images = make_manylinux_images(machine_distros, policies)
        machine_distros, incompatibilities_machine = \
            make_distros(machine_distros, policies)
        incompatibilities.update(incompatibilities_machine)

        # we want a kind of intersection for base_images
        for policy_name in machine_distros.keys():
            # remove invalid base_image
            for base_image in machine_distros[policy_name]:
                if base_image in base_images_set[policy_name] and \
                        base_image not in machine_base_images[policy_name]:
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
        base_images_set.keys(),
        key=lambda x: [int(v) for v in x.split('_')[1:]]
    )
    for policy_name in policy_names:
        if base_images_set[policy_name]:
            base_images[policy_name] = sorted(list(
                base_images_set[policy_name]
            ))

    distros = {}
    all_distros = set()
    policy_names = sorted(
        distros_set.keys(),
        key=lambda x: [int(v) for v in x.split('_')[1:]]
    )
    for policy_name in policy_names:
        current_distros = distros_set[policy_name] - all_distros
        all_distros |= current_distros
        if current_distros:
            distros[policy_name] = sorted(list(current_distros))

    incompatibilities_ = {}
    for distro in sorted(incompatibilities.keys()):
        incompatibilities_[distro] = incompatibilities[distro]
    return base_images, distros, incompatibilities_
