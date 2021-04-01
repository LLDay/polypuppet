from dotenv import load_dotenv
from pathlib import Path
import os


class _Config:
    def __init__(self):
        env_path = Path('polypuppet.env')
        load_dotenv(dotenv_path=env_path)

    def __getitem__(self, env):
        return os.getenv(env)


config = _Config()
