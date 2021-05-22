import logging

from polypuppet.definitions import CONFIG_DIR
from polypuppet.exception import PolypuppetException
from polypuppet.messages import Messages


_level = logging.root.level
logging.root.setLevel(logging.CRITICAL)
# Suppress output to the log from this module
import vagrant  # noqa
logging.root.setLevel(_level)


class Vagrant:

    def __init__(self):
        self._vagrant = vagrant.Vagrant(CONFIG_DIR)
        try:
            self._vagrant.version()
        except Exception as exception:
            exception_message = Messages.executable_not_exists('vagrant')
            raise PolypuppetException(exception_message) from exception

    def is_created(self, vm):
        try:
            return self._vagrant.status(vm)[0].state != self._vagrant.NOT_CREATED
        except Exception as exception:
            raise PolypuppetException(Messages.no_vm_named(vm)) from exception
