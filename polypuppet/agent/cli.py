#!/usr/bin/env python3

import click
import os
from polypuppet.daemon.daemon_accessor import DaemonAccessor


@click.group()
def cli():
    pass


accessor = DaemonAccessor()


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
    output = accessor.stop_daemon()
    if output is not None:
        print(output)


@cli.command()
@click.argument('name', required=False)
@click.argument('value', required=False)
def config(name, value):
    result = api.change_config(name, value)
    if isinstance(result, dict):
        for k, v in result.items():
            print(k + '=' + v)
    elif result is not None:
        print(result)


if __name__ == "__main__":
    cli()
