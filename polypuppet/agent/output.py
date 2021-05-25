import sys

import colorama

colorama.init()


def info(*args):
    print(*args, flush=True)


def _set_color(color):
    print(color, sep='', end='', flush=True)


def _reset_color(output=sys.stdout):
    print(colorama.Style.RESET_ALL, sep='', end='', flush=True, file=output)


def warning(*args):
    _set_color(colorama.Fore.YELLOW)
    print(*args, flush=True)
    _reset_color()


def critical(*args):
    _set_color(colorama.Fore.RED)
    print(*args, flush=True, file=sys.stderr)
    _reset_color(output=sys.stderr)
