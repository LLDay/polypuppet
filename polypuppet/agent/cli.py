#!/usr/bin/env python3

import click
import os
import getpass
from polypuppet import Config
from polypuppet.agent.agent import Agent
from polypuppet.setup import setup_server, setup_agent


@click.group()
def cli():
    pass


@cli.command()
@click.argument('certname')
def autosign(certname):
    agent = Agent()
    has_certname = agent.autosign(certname)
    if not has_certname:
        exit(1)


@cli.command()
@click.argument('username', required=False)
@click.argument('password', required=False)
def login(username, password):
    agent = Agent()
    if username is None:
        username = input('Username: ')
    if password is None:
        password = getpass.getpass('Password: ')
    response = agent.login(username, password)
    if response:
        print('Logged in successfully')
    else:
        exit(1)


@cli.command()
@click.option('-d', '--daemon', is_flag=True, default=False)
def server(daemon):
    agent = Agent()
    if daemon:
        agent.fork_server()
        os._exit(0)
    else:
        agent.run_server()


@cli.command()
def stop():
    agent = Agent()
    agent.stop_server()


@cli.command()
@click.argument('key', required=False)
@click.argument('value', required=False)
@click.option('-k', '--keys-only', is_flag=True)
@click.option('-g', '--generate', is_flag=True)
def config(key, value, keys_only, generate):
    if generate:
        setup_config()
        return

    agent = Agent()
    result = agent.config(key, value)
    if keys_only:
        for k in result:
            print(k)
    elif isinstance(result, dict):
        for k, v in result.items():
            print(k + '=' + v)
    elif result is False:
        print('There is no key', key)
        exit(1)
    elif result is True:
        pass
    elif result is not None:
        print(result)


@cli.command()
@click.argument('what', type=click.Choice(['config', 'agent', 'server']), required=True)
def setup(what):
    if what == 'server':
        setup_server()
    elif what == 'agent':
        setup_agent()
    elif what == 'config':
        config = Config()
        config.setup(force=True)


if __name__ == "__main__":
    cli()
