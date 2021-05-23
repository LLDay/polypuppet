import colorama

colorama.init()


def info(*args):
    print(*args, flush=True)


def warning(*args):
    print(colorama.Fore.YELLOW, *args, colorama.Style.RESET_ALL, flush=True)


def critical(*args):
    print(colorama.Fore.RED, *args, colorama.Style.RESET_ALL, flush=True)
