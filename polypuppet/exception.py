import logging


class PolypuppetException(Exception):
    def __init__(self, message):
        self.message = message

    def print(self):
        logging.error(self.message)

    def print_with_exit(self):
        self.print()
        exit(1)
