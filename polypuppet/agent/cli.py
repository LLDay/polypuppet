#!/usr/bin/env python3

import click
import os
from polypuppet.api import ApiAccessor


@click.group()
def cli():
    pass


accessor = ApiAccessor()


@cli.command()
@click.argument('username')
@click.argument('password')
def login(username, password):
    accessor.login(username, password)


@cli.command()
def daemon():
    accessor.run_daemon()
    os._exit(0)


@cli.command()
def stop():
    message = accessor.stop_daemon()
    if message.success:
        print('Server stopped successfully')
    if message.output:
        print(message.output)


@cli.command()
@click.argument('key', required=False)
@click.argument('value', required=False)
def config(key, value):
    result = accessor.config(key, value)
    if isinstance(result, dict):
        for k, v in result.items():
            print(k + '=' + v)
    elif result is False:
        print('There is no key', key)
        exit(1)
    elif result is True:
        pass
    elif result is not None:
        print(result)


if __name__ == "__main__":
    cli()
