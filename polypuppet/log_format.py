import logging

import coloredlogs


def _setup_log(level=None, fmt=coloredlogs.DEFAULT_LOG_FORMAT):
    formatter = coloredlogs.ColoredFormatter(fmt)

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = root.handlers[0]
    handler.setFormatter(formatter)


def set_clear_logs(level=None):
    _setup_log(level, fmt='%(message)s')


def set_extended_logs(level=None):
    _setup_log(level)
