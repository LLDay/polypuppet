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

_GRPC_V = 'GRPC_VERBOSITY'


def verbosity_option(f):
    def callback(ctx, param, value):
        if value > 0:
            root = logging.root
            root.setLevel(logging.DEBUG)
        if value > 1:
            os.environ[_GRPC_V] = 'DEBUG'
        return value

    return click.option('-v', '--verbose', count=True,
                        expose_value=False,
                        help='Enables verbosity.',
                        callback=callback)(f)


@click.group()
@verbosity_option
def cli():
    pass


@cli.command()
@click.argument('certname')
@verbosity_option
def autosign(certname):
    agent = Agent()
    has_certname = agent.autosign(certname)
    if not has_certname:
        sys.exit(1)


@cli.group('login')
@verbosity_option
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
@verbosity_option
def user(username, password):
    agent = Agent()
    if username is None:
        username = click.prompt('Username')
    if password is None:
        password = click.prompt('Password', hide_input=True)
    response = agent.login(username, password)
    check_login(response)


@login_group.command()
@click.argument('building', required=True, type=click.INT)
@click.argument('number', required=True, type=click.INT)
@click.argument('token', required=True, type=click.STRING)
@verbosity_option
def audience(building, number, token):
    agent = Agent()
    response = agent.audience(building, number, token)
    check_login(response)


def start_server():
    try:
        # This prevents error messages on operating systems that are not supported for the server
        from polypuppet.server.server import main as server_main
        agent = Agent()
        agent.stop_server()
        server_main()

    except ModuleNotFoundError:
        out.critical(Messages.unsupported_os())
        sys.exit(1)

    except PolypuppetException as pe:
        out.critical(pe.message)
        sys.exit(1)


@cli.group(name='server', invoke_without_command=True, help=Messages.help_server())
@click.pass_context
@verbosity_option
def group_server(ctx):
    if not ctx.invoked_subcommand:
        start_server()


@group_server.command(name='stop', help=Messages.help_server_stop())
@verbosity_option
def server_stop():
    agent = Agent()
    if agent.stop_server():
        out.info(Messages.server_stopped())


@group_server.command(name='daemon', help=Messages.help_server_daemon())
@verbosity_option
def server_daemon():
    process = mp.Process(target=start_server)
    process.start()
    os._exit(0)


@cli.command(name='config')
@click.argument('key', required=False)
@click.argument('value', required=False)
@verbosity_option
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
@verbosity_option
def test_group():
    pass


@test_group.command(name='audience')
@click.argument('building')
@click.argument('audience')
@verbosity_option
def test_audience(building, audience):
    config = Config()
    if config['AUDIENCE'] != audience or config['BUILDING'] != building:
        sys.exit(1)


@test_group.command(name='config')
@click.argument('key')
@click.argument('value')
@verbosity_option
def test_config(key, value):
    config = Config()
    try:
        if config[key] != value:
            sys.exit(1)
    except PolypuppetException:
        sys.exit(1)


@test_group.command()
@click.argument('vm_name')
@verbosity_option
def vm(vm_name):
    vagrant = Vagrant()
    if not vagrant.is_created(vm_name):
        exit(1)


@cli.group(name='token', invoke_without_command=True)
@click.pass_context
@verbosity_option
def token_group(ctx):
    if not ctx.invoked_subcommand:
        agent = Agent()
        server_token = agent.get_token()
        if server_token != str():
            out.info(server_token)
        else:
            out.warning(Messages.token_not_generated())
            sys.exit(1)


@token_group.command(name='new')
@verbosity_option
def token_new():
    agent = Agent()
    server_token = agent.update_token()
    out.info(server_token)


@token_group.command(name='clear')
@verbosity_option
def token_clear():
    agent = Agent()
    agent.clear_token()


@token_group.command(name='set')
@click.argument('token')
@verbosity_option
def token_set(token):
    agent = Agent()
    agent.set_token(token)


def main():
    os.environ[_GRPC_V] = 'NONE'
    log_level = logging.INFO
    log_format = '%(message)s'
    logging.basicConfig(format=log_format, level=log_level)

    try:
        cli()
    except PolypuppetException as pe:
        out.critical(pe.message)
        sys.exit(1)


if __name__ == "__main__":
    main()
