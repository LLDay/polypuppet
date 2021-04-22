import configparser
import re

from polypuppet import Puppet, PuppetServer
from polypuppet import Config
from polypuppet.definitions import *
from pathlib import Path


def setup_server():
    config = Config()
    puppet = Puppet()
    server_name = config['PRIMARY_SERVER_DOMAIN']
    certname = config['PRIMARY_SERVER_CERTNAME']

    puppet.service('puppetserver', ensure=False)
    puppet.config('server', server_name, section='server')
    puppet.config('certname', certname, section='server')
    puppet.config('autosign', AUTOSIGN_PATH.as_posix(), section='server')

    if PUPPET_SETTINGS_PATH is not None:
        with open(PUPPET_SETTINGS_PATH, 'r') as settings:
            data = settings.read()
            regex = '(?<=-Xm[sx])[^ ]+'
            data = re.sub(regex, config['PUPPET_MEMORY_USAGE'], data, 2)

        with open(PUPPET_SETTINGS_PATH, 'w') as settings:
            settings.write(data)

    puppetserver = PuppetServer()
    puppetserver.setup()
    puppet.service('puppetserver')
    puppetserver.generate(POLYPUPPET_PEM_NAME)
    config['SSLDIR'] = puppet.config('ssldir')


def setup_agent():
    config = Config()
    puppet = Puppet()
    server_name = config['PRIMARY_SERVER_DOMAIN']
    puppet.config('server', server_name, section='agent')
    puppet.service('puppet', ensure=False, enable=False)
