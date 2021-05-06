#!/usr/bin/env python3

import click
import getpass
import multiprocessing as mp
import os

from polypuppet import Config
from polypuppet.agent.agent import Agent
from polypuppet.agent.setup import setup_server, setup_agent
from polypuppet.server.server import main as server_main
from polypuppet.messages import info, error


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
        username = info.username()
    if password is None:
        password = info.password()
    response = agent.login(username, password)
    if response:
        info.logged_in()
    else:
        error.not_logged_in()


@cli.command()
@click.argument('number', required=True, type=click.INT)
@click.argument('token', required=True, type=click.STRING)
def audience(number, token):
    agent = Agent()
    response = agent.audience(number, token)
    if response:
        info.logged_in()
    else:
        error.not_logged_in()


@cli.command()
@click.option('-d', '--daemon', is_flag=True, default=False)
@click.option('-r', '--restart', is_flag=True, default=False)
def server(daemon, restart):
    if restart:
        agent = Agent()
        agent.stop_server()

    if daemon:
        process = mp.Process(target=server_main)
        process.start()
        os._exit(0)
    else:
        server_main()


@cli.command()
def stop():
    agent = Agent()
    agent.stop_server()


@cli.command()
@click.argument('key', required=False)
@click.argument('value', required=False)
@click.option('-t', '--test', is_flag=True)
def config(key, test, value):
    config = Config()
    if key is None:
        for k, v in config.all().items():
            print(k + '=' + v)
    elif value is None:
        print(config[key])
    else:
        if not test:
            config.restricted_set(key, value)
        elif config[key] != value:
            exit(1)


@cli.command()
@click.argument('what', type=click.Choice(['agent', 'server']), required=True)
def setup(what):
    if what == 'server':
        setup_server()
    elif what == 'agent':
        setup_agent()


@cli.command()
@click.option('--new', '-n', is_flag=True)
@click.option('--clear', '-c', is_flag=True)
def token(new, clear):
    agent = Agent()
    config = Config()
    if clear:
        token = agent.clear_token()
    elif new:
        token = agent.update_token()
        print(token)
    else:
        token = agent.get_token()
        if token == str():
            error.token_not_generated()
        print(token)


if __name__ == "__main__":
    cli()
