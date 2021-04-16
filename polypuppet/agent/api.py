from polypuppet.config import Config
from polypuppet.puppet import Puppet
from polypuppet.daemon import Daemon


class AgentApi:
    def config(self, name=None, value=None):
        pass

    def apply(self):
        pass

    def run_daemon(self):
        pass


class AgentApiImpl(AgentApi):
    def __init__(self):
        self._config = Config()
        self._puppet = Puppet()

    def config(self, key=None, value=None):
        if key is None and value is None:
            return self._config.all()

        if key not in self._config:
            return False
        elif value is None:
            return self._config[key]
        else:
            self._config[key] = value
            return True

    def apply(self):
        self._puppet.sync()

    def run_daemon(self):
        daemon = Daemon()
        daemon.fork()
