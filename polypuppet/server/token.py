import hmac
import os
import secrets
from threading import Lock

from polypuppet.definitions import CONFIG_DIR
from polypuppet.definitions import TOKEN_PATH
from polypuppet.exception import PolypuppetException
from polypuppet.messages import Messages


class Token:
    def __init__(self):
        self.token = ''
        self.lock = Lock()

        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            with self.lock:
                if TOKEN_PATH.exists():
                    with open(TOKEN_PATH, 'r', encoding='UTF-8') as tokenfile:
                        self.token = tokenfile.readline()
        except Exception as exception:
            exception_message = Messages.cannot_create_config_file()
            raise PolypuppetException(exception_message) from exception

    def set(self, token):
        with self.lock:
            self.token = token
            with open(TOKEN_PATH, 'w', encoding='UTF-8') as tokenfile:
                tokenfile.write(self.token)
            os.chmod(TOKEN_PATH, 0o600)

    def get(self):
        return self.token

    def empty(self):
        return self.token == str()

    def new(self):
        token = secrets.token_hex(20)
        self.set(token)
        return token

    def clear(self):
        with self.lock:
            self.token = ''
            TOKEN_PATH.unlink()

    def __eq__(self, value):
        return isinstance(value, str) and hmac.compare_digest(self.get(), value)
