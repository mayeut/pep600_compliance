import argparse
import datetime
import json
import logging
import os
import platform
import subprocess
import sys
import urllib.parse
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


def get_start_end(lines, start_tag, end_tag):
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


def create_cache(machine, force_rolling, continue_on_error):
    exit_code = 0
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
        run = (not os.path.exists(cache_file)) or \
              (force_rolling and image.eol == 'rolling')
        if run:
            try:
                symbols = image.run_check(machine)
                with open(cache_file, 'wt') as f:
                    json.dump(symbols, f, sort_keys=True)
            except BaseException as e:
                if continue_on_error:
                    exit_code |= 1
                    logger.exception('Exception occurred while creating cache '
                                     f'for {cache_name}')
                else:
                    raise e
    return exit_code


def replace_badges(lines):
    start, end = get_start_end(
        lines, '.. begin distro_badges', '.. end distro_badges'
    )
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
        'manylinux': 'python',
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
                free_eol_date = datetime.date.fromisoformat(
                    image.eol[-2].split(':')[1]
                )
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
        line = f'.. |{key}| image:: https://img.shields.io/static/v1?' \
               f'label={urllib.parse.quote(shortname)}&' \
               f'message={urllib.parse.quote(image.version)}%20' \
               f'({urllib.parse.quote(eol)})&' \
               f'color={color}{logo}'
        new_lines.append(line)
    lines = lines[:start + 1] + new_lines + lines[end:]
    return lines


def update_details():
    with open(DETAILS_PATH, 'rt') as f:
        content = f.read()
    lines = content.splitlines()

    lines = replace_badges(lines)

    for machine in MACHINES:
        base_images, distros, _ = manylinux_analysis(CACHE_PATH, machine)
        start, end = get_start_end(
            lines,
            f'.. begin base_images_{machine}',
            f'.. end base_images_{machine}'
        )
        new_lines = [
            f'.. csv-table:: {machine}', '   :header: "policy", "distros"', ''
        ]
        for policy_name in base_images.keys():
            distros_ = ' '.join([
                f'|{d.replace(" ", "-")}|' for d in base_images[policy_name]
            ])
            line = f'   "{policy_name}", "{distros_}"'
            new_lines.append(line)
        lines = lines[:start + 1] + new_lines + lines[end:]

        start, end = get_start_end(
            lines,
            f'.. begin compatibility_{machine}',
            f'.. end compatibility_{machine}'
        )
        new_lines = [
            f'.. csv-table:: {machine}', '   :header: "policy", "distros"', ''
        ]
        for policy_name in distros.keys():
            distros_ = ' '.join([
                f'|{d.replace(" ", "-")}|' for d in distros[policy_name]
            ])
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

    base_images, distros, incompatibilities = manylinux_analysis(
        CACHE_PATH, None
    )

    start, end = get_start_end(
        lines, '.. begin base_images', '.. end base_images'
    )
    new_lines = [
        f'.. csv-table:: base images', '   :header: "policy", "distros"', ''
    ]
    for policy_name in base_images.keys():
        if base_images[policy_name]:
            distros_ = ' '.join([
                f'|{d.replace(" ", "-")}|' for d in base_images[policy_name]
            ])
            line = f'   "{policy_name}", "{distros_}"'
            new_lines.append(line)
    lines = lines[:start + 1] + new_lines + lines[end:]

    start, end = get_start_end(
        lines, '.. begin compatibility', '.. end compatibility'
    )
    new_lines = [
        f'.. csv-table:: compatibility', '   :header: "policy", "distros"', ''
    ]
    for policy_name in distros.keys():
        distros_ = ' '.join([
            f'|{d.replace(" ", "-")}|' for d in distros[policy_name]
        ])
        line = f'   "{policy_name}", "{distros_}"'
        new_lines.append(line)
    lines = lines[:start + 1] + new_lines + lines[end:]

    start, end = get_start_end(
        lines, '.. begin compatibility_issues', '.. end compatibility_issues'
    )
    new_lines = [
        f'.. csv-table:: Compatibility Issues',
        '   :header: "distro", "incompatible policy", "unavailable libraries"',
        '',
    ]
    for distro in incompatibilities.keys():
        name = f'|{distro.replace(" ", "-")}|'
        policy = ''
        libraries = ''
        if 'policy' in incompatibilities[distro].keys():
            policy = incompatibilities[distro]['policy']
        if 'lib' in incompatibilities[distro].keys():
            libraries = ', '.join(sorted(incompatibilities[distro]['lib']))
        line = f'   "{name}", "{policy}", "{libraries}"'
        new_lines.append(line)
    lines = lines[:start + 1] + new_lines + lines[end:]

    content = '\n'.join(lines) + '\n'
    with open(README_PATH, 'wt') as f:
        f.write(content)


def update_eol():
    with open(EOL_PATH, 'rt') as f:
        content = f.read()
    lines = content.splitlines()
    start, end = get_start_end(
        lines, '.. begin eol_information', '.. end eol_information'
    )
    old_name = ''
    new_lines = []
    done = set()
    for image in get_images(None):
        shortname = image.name.replace("-slim", "")
        if shortname != old_name:
            old_name = shortname
            new_lines.extend([
                f'.. csv-table:: {shortname}',
                '   :header: "distro", "EOL", "LTS", "ELTS"',
                '',
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
        line = f'   "{distro_version}",' \
               f' "{dates["EOL"]}", "{dates["LTS"]}", "{dates["ELTS"]}"'
        new_lines.append(line)
    lines = lines[:start + 1] + new_lines + lines[end:]

    content = '\n'.join(lines) + '\n'
    with open(EOL_PATH, 'wt') as f:
        f.write(content)


def main():
    default_machine = [platform.machine()]
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--force-rolling", action='store_true')
    parser.add_argument("-c", "--continue-on-error", action='store_true')
    parser.add_argument("--machine", nargs='*', default=default_machine)
    args = parser.parse_args()
    exit_code = 0
    for machine in args.machine:
        exit_code |= create_cache(machine, args.force_rolling,
                                  args.continue_on_error)
        base_images, _, _ = manylinux_analysis(CACHE_PATH, machine)
        for policy_name in base_images.keys():
            distros_ = base_images[policy_name]
            print(f'{policy_name}: {distros_}')
    update_readme()
    update_details()
    update_eol()
    exit(exit_code)


if __name__ == '__main__':
    main()
