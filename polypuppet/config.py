import configparser
from threading import Lock

from polypuppet.definitions import CONFIG_DIR
from polypuppet.definitions import CONFIG_PATH
from polypuppet.exception import PolypuppetException
from polypuppet.messages import Messages


class Config:
    _lock = Lock()

    def __getitem__(self, key):
        key = str(key).lower()

        # Lock free accessing dict value
        value = self.flat.get(key, None)
        if value is None:
            raise PolypuppetException(Messages.no_config_key(key))
        return value

    def _save(self):
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            CONFIG_PATH.touch(exist_ok=True)
            with Config._lock:
                with open(CONFIG_PATH, 'w', encoding='UTF-8') as configfile:
                    self.config.write(configfile)
        except Exception as exception:
            exception_message = Messages.cannot_create_config_file()
            raise PolypuppetException(exception_message) from exception

    def __setitem__(self, key, value):
        key = key.lower()
        with Config._lock:
            for k in self.config:
                if key in self.config[k]:
                    self.flat[key] = value
                    self.config[k][key] = value
                    break
        self._save()

    def __contains__(self, key):
        return key in self.flat

    def restricted_set(self, key, value):
        for k in ['server']:
            if key in self.config[k]:
                self[key] = value
                return

        if key not in self.flat:
            raise PolypuppetException(Messages.no_config_key(key))
        raise PolypuppetException(Messages.cannot_change_key(key))

    def load(self):
        default_config = configparser.ConfigParser()

        default_config['server'] = {
            'SERVER_DOMAIN': 'server.poly.puppet.com',
            'SERVER_PORT': 8139,
            'CONTROL_PORT': 8139,
            'CERT_WAITTIME': 90}
        default_config['profile'] = {
            'BUILDING': '',
            'CLASSROOM': '',
            'ROLE': '',
            'STUDENT_FLOW': '',
            'STUDENT_GROUP': ''}
        default_config['cache'] = {
            'AGENT_CERTNAME': '',
            'SSLDIR': '',
            'SSL_CERT': '',
            'SSL_PRIVATE': '',
            'CONFDIR': CONFIG_DIR}

        if CONFIG_PATH.exists():
            read_config = configparser.ConfigParser()
            read_config.read(CONFIG_PATH)
            for section in default_config:
                for option in default_config[section]:
                    if read_config.has_option(section, option):
                        default_config[section][option] = read_config[section][option]

        flat_config = {}
        for key in default_config:
            flat_config.update(default_config[key])

        self.config = default_config
        self.flat = flat_config

    def all(self):
        return self.flat

    def __new__(cls):
        with Config._lock:
            if not hasattr(cls, '_instance'):
                cls._instance = super(Config, cls).__new__(cls)
                cls._instance.load()
        return cls._instance
