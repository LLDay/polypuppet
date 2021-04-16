import dotenv
from pathlib import Path


def setup_environment(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    path.touch()

    config_params = {}
    config_params['PRIMARY_SERVER_CERTNAME'] = 'server.poly.puppet.com'
    config_params['PRIMARY_SERVER_DOMAIN'] = 'server.poly.puppet.com'
    config_params['PUPPET_MEMORY_USAGE'] = '256m'
    config_params['PUPPET_VERSION'] = 'puppet7-release'
    config_params['SERVER_PORT'] = 8668
    config_params['CONTROL_PORT'] = 8668
    config_params['CONTROL_IP'] = 'localhost'

    for key, value in config_params.items():
        dotenv.set_key(path, str(key), str(value))
