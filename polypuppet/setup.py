import dotenv
from pathlib import Path


def setup_environment(path):
    path.mkdir()
    path.touch(mode=0o644, exist_ok=True)
    config_params = {}
    config_params['PRIMARY_SERVER_CERTNAME'] = 'server.poly.puppet.com'
    config_params['PRIMARY_SERVER_DOMAIN'] = 'server.poly.puppet.com'
    config_params['PUPPET_MEMORY_USAGE'] = '256m'
    config_params['PUPPET_VERSION'] = 'puppet7-release'
    config_params['AGENT_CONTROL_PORT'] = 8668
    config_params['AGENT_CONTROL_IP'] = 'localhost'

    for key, value in config_params.items():
        dotenv.set_key(path, str(key), str(value))
