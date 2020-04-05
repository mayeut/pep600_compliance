class _PackageManager:
    def __init__(self, install_prefix, update_command=None, environment=None):
        self._install_prefix = install_prefix
        self._update_command = update_command
        self._environment = environment

    def _update(self, container):
        if self._update_command is not None:
            exit_code, output = container.exec_run(
                self._update_command, environment=self._environment)
            assert exit_code == 0, output.decode('utf-8')

    def install(self, container, machine, packages):
        for packages_ in packages:
            self._update(container)
            exit_code, output = container.exec_run(self._install_prefix + packages_, environment=self._environment)
            assert exit_code == 0, output.decode('utf-8')


class APT(_PackageManager):
    def __init__(self, has_no_install_recommends=True, run_once=[], ppa_list=[]):
        install_prefix = ['apt-get', 'install', '-qq', '-y']
        if has_no_install_recommends:
            install_prefix += ['--no-install-recommends']
        update_command = ['apt-get', 'update', '-qq']
        environment = {'DEBIAN_FRONTEND': 'noninteractive'}
        self._run_once = run_once
        self._ppa_list = ppa_list
        super().__init__(install_prefix, update_command, environment)

    def install(self, container, machine, packages):
        for command in self._run_once:
            exit_code, output = container.exec_run(command, environment=self._environment)
            assert exit_code == 0, output.decode('utf-8')
        if self._ppa_list:
            super().install(container, machine, [['software-properties-common', 'python-software-properties']])
            for ppa in self._ppa_list:
                exit_code, output = container.exec_run(['add-apt-repository', ppa], environment=self._environment)
                assert exit_code == 0, output.decode('utf-8')
        super().install(container, machine, packages)


class DNF(_PackageManager):
    def __init__(self):
        super().__init__(['dnf', '-y', 'install'])


class MICRODNF(_PackageManager):
    def __init__(self):
        super().__init__(['microdnf', '-y', 'install'])


class PACMAN(_PackageManager):
    def __init__(self):
        super().__init__(['pacman', '-Sy', '--noconfirm'])


class SWUPD(_PackageManager):
    def __init__(self):
        super().__init__(['swupd', 'bundle-add'])


class TDNF(_PackageManager):
    def __init__(self):
        super().__init__(['tdnf', '-y', 'install'])


class URPM(_PackageManager):
    def __init__(self):
        super().__init__(['urpmi', '--auto', '--no-recommends'])


class YUM(_PackageManager):
    def __init__(self,  run_once=[]):
        self._run_once = run_once
        super().__init__(['yum', '-y', 'install'])

    def install(self, container, machine, packages):
        if machine == 'i686':
            exit_code, output = container.exec_run(['bash', '-c', 'echo "i386" > /etc/yum/vars/basearch'])
            assert exit_code == 0, output.decode('utf-8')
        for command in self._run_once:
            exit_code, output = container.exec_run(command, environment=self._environment)
            assert exit_code == 0, output.decode('utf-8')
        super().install(container, machine, packages)

class ZYPPER(_PackageManager):
    def __init__(self):
        super().__init__(['zypper', 'install', '-y'])

    def install(self, container, machine, packages):
        if machine == 'i686':
            exit_code, output = container.exec_run(['bash', '-c', 'echo "arch = i586" >> /etc/zypp/zypp.conf'])
            assert exit_code == 0, output.decode('utf-8')
        super().install(container, machine, packages)