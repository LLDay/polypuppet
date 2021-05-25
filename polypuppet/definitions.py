import os
import platform
from pathlib import Path

AUTOSIGN_PATH = Path('/usr/local/bin/polypuppet-autosign')

if platform.system() == 'Windows':
    CONFIG_DIR = os.path.expandvars('%PROGRAMDATA%\\Polypuppet\\')
else:
    CONFIG_DIR = '/etc/polypuppet/'

CONFIG_DIR = Path(CONFIG_DIR)
CONFIG_PATH = Path(CONFIG_DIR / 'config.ini')

TOKEN_PATH = Path(CONFIG_DIR / 'token')
CA_PATH = Path(CONFIG_DIR / 'ca.pem')
