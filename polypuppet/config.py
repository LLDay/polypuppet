import configparser

from polypuppet.definitions import CONFIG_DIR
from polypuppet.definitions import CONFIG_PATH
from polypuppet.exception import PolypuppetException
from polypuppet.messages import messages


class Config:
    def __getitem__(self, key):
        key = str(key).lower()
        if key not in self.flat:
            raise PolypuppetException(messages.no_config_key(key))
        return self.flat[key]

    def __setitem__(self, key, value):
        key = key.lower()
        for k in self.config:
            if key in self.config[k]:
                self.flat[key] = value
                self.config[k][key] = value
                break

        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            CONFIG_PATH.touch(exist_ok=True)
            with open(CONFIG_PATH, 'w') as configfile:
                self.config.write(configfile)
        except Exception as exception:
            exception_message = messages.cannot_create_config_file()
            raise PolypuppetException(exception_message) from exception

    def __contains__(self, key):
        return key in self.flat

    def restricted_set(self, key, value):
        for k in ['agent', 'server']:
            if key in self.config[k]:
                self[key] = value
                return

        if key not in self.flat:
            raise PolypuppetException(messages.no_config_key(key))
        raise PolypuppetException(messages.cannot_change_key(key))

    def load(self):
        default_config = configparser.ConfigParser()

        default_config['server'] = {
            'SERVER_DOMAIN': 'server.poly.puppet.com',
            'SERVER_PORT': 8139}
        default_config['agent'] = {
            'CONTROL_PORT': 8139,
            'CERT_WAITTIME': 90}
        default_config['profile'] = {
            'AUDIENCE': '',
            'ROLE': '',
            'STUDENT_FLOW': '',
            'STUDENT_GROUP': ''}
        default_config['cache'] = {
            'AGENT_CERTNAME': '',
            'SSLDIR': '',
            'SSL_CERT': '',
            'SSL_PRIVATE': '',
            'SSL_SERVER_CERT': '',
            'SSL_SERVER_PRIVATE': ''}

        if CONFIG_PATH.exists():
            read_config = configparser.ConfigParser()
            read_config.read(CONFIG_PATH)
            for section in default_config:
                for option in default_config[section]:
                    if read_config.has_option(section, option):
                        default_config[section][option] = read_config[section][option]

        self.config = default_config
        self.flat = {}
        for key in self.config:
            self.flat.update(self.config[key])

    def all(self):
        return self.flat

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.load()
        return cls._instance
