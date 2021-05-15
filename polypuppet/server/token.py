import os
import secrets

from polypuppet.definitions import CONFIG_DIR
from polypuppet.definitions import TOKEN_PATH
from polypuppet.exception import PolypuppetException
from polypuppet.messages import messages


class Token:
    def __init__(self):
        self.token = ''
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            if TOKEN_PATH.exists():
                with open(TOKEN_PATH, 'r') as tokenfile:
                    self.token = tokenfile.readline()
        except Exception as exception:
            exception_message = messages.cannot_create_config_file()
            raise PolypuppetException(exception_message) from exception

    def _set(self, token):
        self.token = token
        with open(TOKEN_PATH, 'w') as tokenfile:
            tokenfile.write(self.token)
        os.chmod(TOKEN_PATH, 0o600)

    def empty(self):
        return self.token == str()

    def get(self):
        return self.token

    def new(self):
        token = secrets.token_hex(20)
        self._set(token)
        return token

    def clear(self):
        self.token = ''
        TOKEN_PATH.unlink()

    def __eq__(self, value):
        return isinstance(value, str) and self.token == value
