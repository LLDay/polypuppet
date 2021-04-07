from pathlib import Path
from polypuppet.setup import setup_environment
import dotenv
import os

_defaults = {}
_defaults['AGENT_CONTROL_PORT'] = 8668
_defaults['AGENT_CONTROL_IP'] = 'localhost'


class Config:
    env_path = Path('/etc/polypuppet/polypuppet.env')

    def __init__(self):
        if not Path.exists(self.env_path):
            try:
                setup_environment(self.env_path)
                self.load()
            except:
                return

    def __getitem__(self, env):
        value = os.getenv(env)
        if value is None:
            return _defaults.get(env)

    def load(self):
        self.presented_keys = dotenv.dotenv_values(self.env_path).keys()
        dotenv.load_dotenv(self.env_path)

    def all(self):
        all_configs = {}
        for key in self.presented_keys:
            all_configs[key] = self[key]
        return all_configs

    def __setitem__(self, key, value):
        if key in self.presented_keys:
            os.environ[key] = value
            dotenv.set_key(self.env_path, str(key), str(value))

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance
