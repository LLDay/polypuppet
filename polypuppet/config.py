import configparser
from polypuppet.definitions import CONFIG_PATH
from polypuppet.messages import error


class Config:
    def __getitem__(self, value):
        value = str(value).lower()
        return self.flat[value]

    def __setitem__(self, key, value):
        for k in self.config:
            if key in self.config[k]:
                self.flat[key] = value
                self.config[k][key] = value

        try:
            CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
            CONFIG_PATH.touch(exist_ok=True)
            with open(CONFIG_PATH, 'w') as configfile:
                self.config.write(configfile)
        except:
            error.cannot_create_config_file()

    def __contains__(self, key):
        return key in self.flat

    def load(self):
        default_config = configparser.ConfigParser()
        default_config['server'] = {
            'CONTROL_IP': 'localhost',
            'SSLDIR': '/etc/puppetlabs/puppet/ssl',
            'CONTROL_PORT': 8668,
            'NEW_CERT_LIFETIME': 90,
            'PRIMARY_SERVER_CERTNAME': 'server.poly.puppet.com',
            'PUPPET_MEMORY_USAGE': '256m'}
        default_config['common'] = {
            'PRIMARY_SERVER_DOMAIN': 'server.poly.puppet.com',
            'PUPPET_VERSION': 'puppet7-release',
            'SERVER_PORT': 8668}

        if not CONFIG_PATH.exists():
            self.config = default_config
        else:
            self.config = configparser.ConfigParser()
            self.config.read(CONFIG_PATH)

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
