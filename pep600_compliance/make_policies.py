import json
import os

from collections import defaultdict
from glob import glob


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


def get_policy(policies, glibc_version):
    for policy in policies:
        if policy['glibc_version'] == glibc_version:
            return policy
    return None


def make_policies(distros):
    result = []
    for distro in distros:
        glibc_version = distro['glibc_version']
        policy = get_policy(result, glibc_version)
        if policy is None:
            policy = {'glibc_version': glibc_version, 'symbols': {}}
            symbols = policy['symbols']
            for symbol in distro['symbols'].keys():
                symbols[symbol] = set(distro['symbols'][symbol])
            result.append(policy)
        else:
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


def filter_image(distro_name, distro_version):
    #return False
    if distro_name not in ['centos', 'clefos', 'ubuntu', 'debian']:
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
        distro_glibc_version = tuple([int(v) for v in distro['glibc_version'].split('.')])
        if filter_image(distro_name, distro_version):  # keep only LTS distros
            continue
        for policy in policies:
            policy_glibc_version = tuple(
                [int(v) for v in policy['glibc_version'].split('.')])
            if distro_glibc_version != policy_glibc_version:
                continue
            #if distro_glibc_version < policy_glibc_version:
            #    break
            if can_create_manylinux_wheel(distro, policy):
                distro_description = '{} {}'.format(distro_name, distro_version)
                policy_name = 'manylinux_{}_{}'.format(*policy_glibc_version)
                result[policy_name].append(distro_description)
                break
    return result


def make_distros(distros):
    result = defaultdict(list)
    for distro in distros:
        distro_name = distro['distro_name']
        distro_version = distro['distro_version']
        distro_glibc_version = tuple([int(v) for v in distro['glibc_version'].split('.')])
        distro_description = f'{distro_name} {distro_version}'
        if len(distro_glibc_version) == 3:
            # using a future version, seen on fedora upcoming release
            assert distro_glibc_version[2] == 9000
            policy_name = 'manylinux_{}_{}_{}'.format(*distro_glibc_version)
        else:
            assert len(distro_glibc_version) == 2
            policy_name = 'manylinux_{}_{}'.format(*distro_glibc_version)
        result[policy_name].append(distro_description)
    return result


def manylinux_analysis(path, machine):
    cache_path = os.path.join(path, machine)
    distros = load_distros(cache_path)
    policies = make_policies(distros)
    base_images = make_manylinux_images(distros, policies)
    distros = make_distros(distros)
    return base_images, distros
