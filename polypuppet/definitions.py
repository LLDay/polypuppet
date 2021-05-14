import platform
from pathlib import Path

EOF_SIGN = b'__EOF__'

AUTOSIGN_PATH = Path('/usr/local/bin/polypuppet-autosign')

if platform.system() == 'Windows':
    CONFIG_DIR = os.path.expandvars('%PROGRAMDATA%\\polypuppet\\')
else:
    CONFIG_DIR = '/etc/polypuppet/'

CONFIG_DIR = Path(CONFIG_DIR)
CONFIG_PATH = Path(CONFIG_DIR / 'config.ini')
TOKEN_PATH = Path(CONFIG_DIR / 'token')

PUPPET_SETTINGS_PATH_U = Path('/etc/default/puppetserver')
PUPPET_SETTINGS_PATH_C = Path('/etc/sysconfig/puppetserver')
if PUPPET_SETTINGS_PATH_U.exists():
    PUPPET_SETTINGS_PATH = PUPPET_SETTINGS_PATH_U
elif PUPPET_SETTINGS_PATH_C.exists():
    PUPPET_SETTINGS_PATH = PUPPET_SETTINGS_PATH_C
else:
    PUPPET_SETTINGS_PATH = None

POLYPUPPET_PEM_NAME = 'polypuppet'
