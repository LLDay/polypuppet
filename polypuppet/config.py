from pathlib import Path
from polypuppet.setup import setup_environment
import dotenv
import os


class Config:
    env_path = Path('/etc/polypuppet/polypuppet.env')

    def __getitem__(self, env):
        return os.getenv(env)

    def __setitem__(self, key, value):
        if key in self.presented_keys:
            os.environ[key] = value
            dotenv.set_key(self.env_path, str(key), str(value))

    def __contains__(self, key):
        return key in self.presented_keys

    def load(self):
        self.presented_keys = dotenv.dotenv_values(self.env_path).keys()
        dotenv.load_dotenv(self.env_path)

    def all(self):
        all_configs = {}
        for key in self.presented_keys:
            all_configs[key] = self[key]
        return all_configs

    def _init_singleton(self):
        self.presented_keys = {}
        if not Path.exists(self.env_path):
            try:
                setup_environment(self.env_path)
                self.load()
            except Exception as e:
                print(e)
                return
        else:
            self.load()

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._init_singleton()
        return cls._instance
