import argparse
import json
import logging
import os
import platform
import subprocess
import sys
from pep600_compliance.images import get_images
from pep600_compliance.make_policies import manylinux_analysis


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HERE = os.path.abspath(os.path.dirname(__file__))


def create_cache(path, machine):
    cache_path = os.path.join(path, machine)
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)

    subprocess.check_call([
        sys.executable, '-m', 'pip', 'download', '--no-deps', '--no-binary', ':all:',
        '-d', os.path.join(HERE, 'tools'),
        'pyelftools==0.26'
    ])

    for image in get_images(machine):
        cache_name = f'{image.name}-{image.version}'
        cache_file = os.path.join(cache_path, cache_name + '.json')
        if not os.path.exists(cache_file):
            symbols = image.run_check(machine)
            with open(cache_file, 'wt') as f:
                json.dump(symbols, f, sort_keys=True)


def update_readme(path, machine, base_images, distros):
    with open(path, 'rt') as f:
        content = f.read()
    lines = content.splitlines()

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
        distros_ = ', '.join([d for d in sorted(base_images[policy_name])])
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
        distros_ = ', '.join([d for d in sorted(distros[policy_name])])
        line = f'   "{policy_name}", "{distros_}"'
        new_lines.append(line)
    lines = lines[:start + 1] + new_lines + lines[end:]

    content = '\n'.join(lines) + '\n'

    with open(path, 'wt') as f:
        f.write(content)


def main():
    default_machine = [platform.machine()]
    parser = argparse.ArgumentParser()
    parser.add_argument("--machine", nargs='*', default=default_machine)
    parser.add_argument("--cache-folder", required=True, help="Path of the cache folder")
    parser.add_argument("--readme", required=False, help="Path of the readme file to update")
    args = parser.parse_args()

    for machine in args.machine:
        create_cache(args.cache_folder, machine)
        base_images, distros = manylinux_analysis(args.cache_folder, machine)
        for policy_name in sorted(base_images.keys()):
            print(f'{policy_name}: {base_images[policy_name]}')
        if args.readme:
            update_readme(args.readme, machine, base_images, distros)


if __name__ == '__main__':
    main()


