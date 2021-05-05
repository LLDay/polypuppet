import configparser
import re

from polypuppet import Puppet, PuppetServer
from polypuppet import Config
from polypuppet.definitions import *
from pathlib import Path


def setup_server():
    config = Config()
    puppet = Puppet()
    server_name = config['SERVER_DOMAIN']
    certname = config['SERVER_CERTNAME']

    puppet.service('puppetserver', ensure=False)

    puppet.config('autosign', AUTOSIGN_PATH.as_posix(), section='server')
    puppet.config('certname', certname, section='main')
    puppet.config('server', server_name, section='main')
    puppet.service('puppetserver')
    config['SSLDIR'] = puppet.config('ssldir')

    puppetserver = PuppetServer()
    puppetserver.generate(POLYPUPPET_PEM_NAME)


def setup_agent():
    config = Config()
    puppet = Puppet()
    server_name = config['SERVER_DOMAIN']
    puppet.config('server', server_name, section='agent')
    puppet.service('puppet', ensure=False, enable=False)
    config['SSLDIR'] = puppet.config('ssldir')
