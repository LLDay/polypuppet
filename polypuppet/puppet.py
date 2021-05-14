import subprocess
import pathlib

from shutil import which
from polypuppet.messages import info, error
from polypuppet.config import Config


class PuppetBase:
    def _get_full_path(self, executable_name):
        puppetlabs_path_x = '/opt/puppetlabs/bin/'
        puppetlabs_path_w = 'C:\\Program Files\\PuppetLabs\\bin\\'

        unix_path = which(executable_name, path=puppetlabs_path_x)
        windows_path = which(executable_name, path=puppetlabs_path_w)
        env_path = which(executable_name)

        return unix_path or windows_path or env_path

    def _run(self, *args, returncode=False):
        full_command = ' '.join([self.path, *args])
        print(full_command)
        run = subprocess.run(full_command.split(),
                             capture_output=True, text=True)
        if returncode:
            return run.returncode
        else:
            return run.stdout.strip()

    def __init__(self, executable_name):
        self.path = self._get_full_path(executable_name)
        if self.path is None:
            error.puppet_exec_no_exit(executable_name)


class Puppet(PuppetBase):
    def __init__(self):
        super().__init__('puppet')

    def config(self, which, value=None, rm=False, section='agent'):
        if rm:
            return self._run('config delete --section', section, which)
        elif value is None:
            return self._run('config print --section', section, which)
        else:
            return self._run('config set', which, value, '--section', section)

    def ssldir(self):
        config = Config()
        ssldir = config['SSLDIR']
        if not ssldir:
            ssldir = self.config('ssldir')
            config['SSLDIR'] = ssldir
        return pathlib.Path(ssldir)

    def clean_certname(self, certname=None):
        if certname is None:
            return self._run('ssl clean', returncode=True)
        else:
            return self._run('ssl clean --certname', certname, returncode=True)

    def certname(self, value=None):
        if value is None:
            return self.config('certname')
        else:
            self.clean_certname()
            self.config('certname', value, section='agent')

    def sync(self, noop=False):
        command = ['agent --test --no-daemonize']
        if noop:
            command.append('--noop')
        return self._run(*command)

    def service(self, service_name, ensure=True, enable=None):
        if enable is None:
            enable = ensure

        ensure = 'running' if ensure else 'stopped'
        enable = 'true' if enable else 'false'

        command = ['resource service']
        command.append(service_name)
        command.append('ensure=' + ensure)
        command.append('enable=' + enable)
        self._run(*command)


class PuppetServer(PuppetBase):
    def __init__(self):
        super().__init__('puppetserver')

    def generate(self, certname):
        return self._run('ca generate --certname', certname, returncode=False)

    def clean_certname(self, certname):
        return self._run('ca clean --certname', certname, returncode=False)
