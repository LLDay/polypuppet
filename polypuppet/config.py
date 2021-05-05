import configparser

from polypuppet.definitions import CONFIG_DIR, CONFIG_PATH, POLYPUPPET_PEM_NAME
from polypuppet.messages import error


class Config:
    def __getitem__(self, key):
        key = str(key).lower()
        if key not in self.flat:
            error.no_config_key(key)
        return self.flat[key]

    def __setitem__(self, key, value):
        for k in self.config:
            if key in self.config[k]:
                self.flat[key] = value
                self.config[k][key] = value

        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            CONFIG_PATH.touch(exist_ok=True)
            with open(CONFIG_PATH, 'w') as configfile:
                self.config.write(configfile)
        except:
            error.cannot_create_config_file()

    def __contains__(self, key):
        return key in self.flat

    def restricted_set(self, key, value):
        for k in ['agent', 'server']:
            if key in self.config[k]:
                self[key] = value
                return

        if key not in self.flat:
            error.no_config_key(key)
        else:
            error.cannot_change_key(key)

    def load(self):
        default_config = configparser.ConfigParser()

        default_config['server'] = {
            'SERVER_DOMAIN': 'server.poly.puppet.com',
            'SERVER_PORT': 8139}
        default_config['agent'] = {
            'CONTROL_PORT': 8139,
            'CERT_WAITTIME': 90,
            'ENABLED': False}
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
            'CONFDIR': CONFIG_DIR}

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
