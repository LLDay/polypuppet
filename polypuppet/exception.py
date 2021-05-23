import logging


class PolypuppetException(Exception):
    def __init__(self, message):
        self.message = message
