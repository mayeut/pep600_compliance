import argparse
import datetime
import json
import logging
import os
import platform
import subprocess
import sys
import urllib.parse
from collections import defaultdict
from pep600_compliance.images import get_images
from pep600_compliance.make_policies import manylinux_analysis


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HERE = os.path.abspath(os.path.dirname(__file__))
CACHE_PATH = os.path.abspath(os.path.join(HERE, '..', 'cache'))
README_PATH = os.path.abspath(os.path.join(HERE, '..', 'README.rst'))
DETAILS_PATH = os.path.abspath(os.path.join(HERE, '..', 'DETAILS.rst'))
EOL_PATH = os.path.abspath(os.path.join(HERE, '..', 'EOL.rst'))
MACHINES = {'x86_64', 'i686', 'aarch64', 'ppc64le', 's390x', 'armv7l'}


def create_cache(machine):
    machine_cache_path = os.path.join(CACHE_PATH, machine)
    if not os.path.exists(machine_cache_path):
        os.makedirs(machine_cache_path)
    subprocess.check_call([
        sys.executable, '-m', 'pip', 'download', '--no-deps', '--no-binary',
        ':all:', '-d', os.path.join(HERE, 'tools'),
        'pyelftools==0.26'
    ])
    for image in get_images(machine):
        cache_name = f'{image.name}-{image.version}'
        cache_file = os.path.join(machine_cache_path, cache_name + '.json')
        if not os.path.exists(cache_file):
            symbols = image.run_check(machine)
            with open(cache_file, 'wt') as f:
                json.dump(symbols, f, sort_keys=True)


def replace_badges(lines):
    for i in range(len(lines)):
        if f'.. begin distro_badges' in lines[i]:
            start = i
        if f'.. end distro_badges' in lines[i]:
            end = i
            break
    new_lines = []
    keys = []
    six_months = datetime.timedelta(days=182)
    today = datetime.date.today()
    logos = {
        'centos': 'centos',
        'ubuntu': 'ubuntu',
        'debian': 'debian',
        'fedora': 'fedora',
        'rhubi': 'red-hat',
        'amazonlinux': 'amazon-aws',
        'oraclelinux': 'oracle',
        'opensuse': 'opensuse',
        'photon': 'vmware',
        'archlinux': 'arch-linux',
        'slackware': 'slackware',
    }
    for image in get_images(None):
        shortname = image.name.replace("-slim", "")
        key = f'{shortname}-{image.version}'
        if key in keys:
            continue
        keys.append(key)
        if image.eol == 'rolling':
            color = 'purple'
            eol = image.eol
        elif image.eol == 'unknown':
            color = 'lightgray'
            eol = image.eol
        else:
            last_eol_type, last_eol_date = image.eol[-1].split(':')
            free_eol_date = datetime.date.fromisoformat(last_eol_date)
            paid_eol_date = free_eol_date
            if last_eol_type == 'ELTS':
                free_eol_date = datetime.date.fromisoformat(image.eol[-2].split(':')[1])
            eol = ' / '.join([date for date in image.eol])
            if paid_eol_date < today:
                color = 'black'
            elif free_eol_date < today:
                color = 'red'
            elif free_eol_date > (today + six_months):
                color = 'green'
            else:
                color = 'yellow'
        logo = ''
        if shortname in logos.keys():
            logo = f'&logo={logos[shortname]}&logoColor=white'
        line = f'.. |{key}| image:: https://img.shields.io/static/v1?label={urllib.parse.quote(shortname)}&message={urllib.parse.quote(image.version)}%20({urllib.parse.quote(eol)})&color={color}{logo}'
        new_lines.append(line)
    lines = lines[:start + 1] + new_lines + lines[end:]
    return lines


def update_details():
    with open(DETAILS_PATH, 'rt') as f:
        content = f.read()
    lines = content.splitlines()

    lines = replace_badges(lines)

    for machine in MACHINES:
        base_images, distros = manylinux_analysis(CACHE_PATH, machine)
        for i in range(len(lines)):
            if f'.. begin base_images_{machine}' in lines[i]:
                start = i
            if f'.. end base_images_{machine}' in lines[i]:
                end = i
                break
        new_lines = [f'.. csv-table:: {machine}', '   :header: "policy", "distros"', '']
        policy_names = sorted(
            base_images.keys(),
            key=lambda x: [int(v) for v in x.split('_')[1:]]
        )
        for policy_name in policy_names:
            distros_ = ' '.join([f'|{d.replace(" ", "-")}|' for d in sorted(base_images[policy_name])])
            line = f'   "{policy_name}", "{distros_}"'
            new_lines.append(line)
        lines = lines[:start + 1] + new_lines + lines[end:]

        for i in range(len(lines)):
            if f'.. begin compatibility_{machine}' in lines[i]:
                start = i
            if f'.. end compatibility_{machine}' in lines[i]:
                end = i
                break
        new_lines = [f'.. csv-table:: {machine}', '   :header: "policy", "distros"', '']
        policy_names = sorted(
            distros.keys(),
            key=lambda x: [int(v) for v in x.split('_')[1:]]
        )
        for policy_name in policy_names:
            distros_ = ' '.join([f'|{d.replace(" ", "-")}|' for d in sorted(distros[policy_name])])
            line = f'   "{policy_name}", "{distros_}"'
            new_lines.append(line)
        lines = lines[:start + 1] + new_lines + lines[end:]

    content = '\n'.join(lines) + '\n'
    with open(DETAILS_PATH, 'wt') as f:
        f.write(content)


def update_readme():
    with open(README_PATH, 'rt') as f:
        content = f.read()
    lines = content.splitlines()

    lines = replace_badges(lines)

    base_images = defaultdict(set)
    distros = defaultdict(set)
    for machine in MACHINES:
        machine_base_images, machine_distros = manylinux_analysis(CACHE_PATH, machine)
        # we want a kind of intersection for base_images
        for policy_name in machine_distros.keys():
            # remove invalid base_image
            for base_image in machine_distros[policy_name]:
                if base_image in base_images[policy_name] and base_image not in machine_base_images[policy_name]:
                    base_images[policy_name].remove(base_image)
            # add new base_image
            for base_image in machine_base_images[policy_name]:
                if base_image not in distros[policy_name]:
                    base_images[policy_name].add(base_image)
        # update distros
        for policy_name in machine_distros.keys():
            distros[policy_name] |= set(machine_distros[policy_name])
    for i in range(len(lines)):
        if f'.. begin base_images' in lines[i]:
            start = i
        if f'.. end base_images' in lines[i]:
            end = i
            break
    new_lines = [f'.. csv-table:: base images', '   :header: "policy", "distros"', '']
    policy_names = sorted(
        base_images.keys(),
        key=lambda x: [int(v) for v in x.split('_')[1:]]
    )
    for policy_name in policy_names:
        if base_images[policy_name]:
            distros_ = ' '.join([
                f'|{d.replace(" ", "-")}|' for d in sorted(base_images[policy_name])
            ])
            line = f'   "{policy_name}", "{distros_}"'
            new_lines.append(line)
    lines = lines[:start + 1] + new_lines + lines[end:]

    for i in range(len(lines)):
        if f'.. begin compatibility' in lines[i]:
            start = i
        if f'.. end compatibility' in lines[i]:
            end = i
            break
    new_lines = [
        f'.. csv-table:: compatibility', '   :header: "policy", "distros"', ''
    ]
    policy_names = sorted(
        distros.keys(),
        key=lambda x: [int(v) for v in x.split('_')[1:]]
    )
    all_distros = set()
    for policy_name in policy_names:
        current_distros = distros[policy_name] - all_distros
        all_distros |= current_distros
        distros_ = ' '.join([
            f'|{d.replace(" ", "-")}|' for d in sorted(current_distros)
        ])
        line = f'   "{policy_name}", "{distros_}"'
        new_lines.append(line)
    lines = lines[:start + 1] + new_lines + lines[end:]

    content = '\n'.join(lines) + '\n'
    with open(README_PATH, 'wt') as f:
        f.write(content)


def update_eol():
    with open(EOL_PATH, 'rt') as f:
        content = f.read()
    lines = content.splitlines()
    for i in range(len(lines)):
        if f'.. begin eol_information' in lines[i]:
            start = i
        if f'.. end eol_information' in lines[i]:
            end = i
            break

    old_name = ''
    new_lines = []
    done = set()
    for image in get_images(None):
        shortname = image.name.replace("-slim", "")
        if shortname != old_name:
            old_name = shortname
            new_lines.extend([
                f'.. csv-table:: {shortname}', '   :header: "distro", "EOL", "LTS", "ELTS"', ''
            ])
        distro_version = f'{shortname} {image.version}'
        if distro_version in done:
            continue
        done.add(distro_version)
        dates = {
            'EOL': '',
            'LTS': '',
            'ELTS': '',
        }
        if image.eol in {'rolling', 'unknown'}:
            dates['EOL'] = image.eol
        else:
            for eol_info in image.eol:
                kind, date = eol_info.split(':')
                dates[kind] = date
        line = f'   "{distro_version}", "{dates["EOL"]}", "{dates["LTS"]}", "{dates["ELTS"]}"'
        new_lines.append(line)
    lines = lines[:start + 1] + new_lines + lines[end:]

    content = '\n'.join(lines) + '\n'
    with open(EOL_PATH, 'wt') as f:
        f.write(content)

def main():
    default_machine = [platform.machine()]
    parser = argparse.ArgumentParser()
    parser.add_argument("--machine", nargs='*', default=default_machine)
    args = parser.parse_args()
    for machine in args.machine:
        create_cache(machine)

        base_images, distros = manylinux_analysis(CACHE_PATH, machine)
        policy_names = sorted(
            base_images.keys(),
            key=lambda x: [int(v) for v in x.split('_')[1:]]
        )
        for policy_name in policy_names:
            distros_ = base_images[policy_name]
            print(f'{policy_name}: {distros_}')
    update_readme()
    update_details()
    update_eol()


if __name__ == '__main__':
    main()
