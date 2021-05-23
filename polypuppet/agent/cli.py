#!/usr/bin/env python3
import logging
import multiprocessing as mp
import os
import sys

import click
import polypuppet.agent.output as out
from polypuppet import Config
from polypuppet.agent.agent import Agent
from polypuppet.agent.vagrant import Vagrant
from polypuppet.exception import PolypuppetException
from polypuppet.messages import Messages
from polypuppet.server.server import main as server_main
from polypuppet.server.server import Server


@click.group()
@click.option('-v', '--verbose', count=True, help=Messages.help_verbose())
def cli(verbose):
    grpc_v = 'GRPC_VERBOSITY'
    os.environ.get(grpc_v, 'NONE')

    loglevel = logging.INFO
    if verbose > 0:
        loglevel = logging.DEBUG
    if verbose > 1:
        os.environ.get(grpc_v, 'DEBUG')

    logging.root.setLevel(loglevel)


@cli.command()
@click.argument('certname')
def autosign(certname):
    agent = Agent()
    has_certname = agent.autosign(certname)
    if not has_certname:
        sys.exit(1)


@cli.group('login')
def login_group():
    pass


def check_login(response):
    if response:
        out.info(Messages.logged_in())
    else:
        out.warning(Messages.not_logged_in())
        sys.exit(1)


@login_group.command()
@click.argument('username', required=False)
@click.argument('password', required=False)
def user(username, password):
    agent = Agent()
    if username is None:
        username = click.prompt('Username')
    if password is None:
        password = click.prompt('Password', hide_input=True)
    response = agent.login(username, password)
    check_login(response)


@cli.command()
@click.argument('number', required=True, type=click.INT)
@click.argument('token', required=True, type=click.STRING)
def audience(number, token):
    agent = Agent()
    response = agent.audience(number, token)
    check_login(response)


def start_server():
    try:
        server_main()
    except PolypuppetException as pe:
        out.critical(pe.message)
        sys.exit(1)


@cli.command(help=Messages.help_server())
@click.option('-d', '--daemon', is_flag=True, help=Messages.help_server_daemon())
@click.option('-r', '--restart', is_flag=True, help=Messages.help_server_restart())
@click.option('-s', '--stop', is_flag=True, help=Messages.help_server_stop())
def server(daemon, restart, stop):
    if stop or restart:
        agent = Agent()
        is_stopped = agent.stop_server()

    if stop:
        if is_stopped:
            out.info('Server stopped')
        return

    if daemon:
        process = mp.Process(target=start_server)
        process.start()
        os._exit(0)
    else:
        start_server()


@cli.command(name='config')
@click.argument('key', required=False)
@click.argument('value', required=False)
def manage_config(key, value):
    config = Config()
    if key is None:
        for key, value in config.all().items():
            out.info(key + '=' + value)
    elif value is None:
        out.info(config[key])
    else:
        config.restricted_set(key, value)


@cli.group(name='test')
def test_group():
    pass


@test_group.command()
@click.argument('key')
@click.argument('value')
def config(key, value):
    config = Config()
    try:
        if config[key] != value:
            sys.exit(1)
    except PolypuppetException:
        sys.exit(1)


@test_group.command()
@click.argument('vm_name')
def vm(vm_name):
    vagrant = Vagrant()
    vagrant.is_created(vm_name)


@cli.command()
@click.option('--new', '-n', is_flag=True)
@click.option('--clear', '-c', is_flag=True)
def token(new, clear):
    agent = Agent()
    if clear:
        agent.clear_token()
        return

    if new:
        server_token = agent.update_token()
        out.info(server_token)
    else:
        server_token = agent.get_token()
        if server_token != str():
            out.info(server_token)
        else:
            out.warning(Messages.token_not_generated())
            sys.exit(1)


def main():
    try:
        cli()
    except PolypuppetException as pe:
        out.critical(pe.message)
        sys.exit(1)


if __name__ == "__main__":
    main()
