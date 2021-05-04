import os
import secrets

from polypuppet import config
from polypuppet.messages import error
from polypuppet.definitions import TOKEN_PATH, CONFIG_DIR


class Token:
    def __init__(self):
        self.token = ''
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            if TOKEN_PATH.exists():
                with open(TOKEN_PATH, 'r') as tokenfile:
                    self.token = tokenfile.readline()
        except:
            error.cannot_create_token_file()

    def _set(self, token):
        self.token = token
        with open(TOKEN_PATH, 'w') as tokenfile:
            tokenfile.write(self.token)
        os.chmod(TOKEN_PATH, 0o600)

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
