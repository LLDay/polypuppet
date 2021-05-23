import logging
import pathlib
import subprocess
from shutil import which

import requests
import urllib3
from polypuppet.config import Config
from polypuppet.definitions import CA_PATH
from polypuppet.exception import PolypuppetException
from polypuppet.messages import Messages


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
        logging.debug(full_command)
        run = subprocess.run(full_command.split(), check=False,
                             capture_output=True, text=True)

        stdout = run.stdout.strip()
        stderr = run.stderr.strip()

        if stderr:
            logging.debug(stderr)

        if returncode:
            return run.returncode
        return stdout

    def __init__(self, executable_name):
        self.path = self._get_full_path(executable_name)
        if self.path is None:
            exception_message = Messages.executable_not_exists(executable_name)
            raise PolypuppetException(exception_message)


class Puppet(PuppetBase):
    def __init__(self):
        super().__init__('puppet')

    def config(self, key, value=None, rm=False, section='agent'):
        if rm:
            return self._run('config delete --section', section, key)
        if value is None:
            return self._run('config print --section', section, key)
        return self._run('config set', key, value, '--section', section)

    def download_ca(self):
        config = Config()
        domain = config['SERVER_DOMAIN']

        # TODO: change verify=True and remove warning disabling when get trusted CA
        url = 'https://{0}:8140/puppet-ca/v1/certificate/{0}'.format(domain)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        try:
            response = requests.get(url, verify=False)
        except Exception as exception:
            exception_message = Messages.cannot_connect_to_server(domain, 8140)
            raise PolypuppetException(exception_message) from exception

        try:
            with open(CA_PATH, 'w', encoding='UTF-8') as ca_file:
                ca_file.write(response.text)
        except Exception as exception:
            exception_message = Messages.cannot_create_ca_file()
            raise PolypuppetException(exception_message) from exception

    def get_ca(self):
        if not CA_PATH.exists():
            self.download_ca()

        with open(CA_PATH, 'rb') as ca:
            return ca.read()

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
        return self._run('ssl clean --certname', certname, returncode=True)

    def certname(self, value=None):
        if value is None:
            return self.config('certname')
        self.clean_certname()
        return self.config('certname', value, section='agent')

    def sync(self, noop=False):
        command = ['agent --test --no-daemonize']
        if noop:
            command.append('--noop')
        return self._run(*command, returncode=True) == 0

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
