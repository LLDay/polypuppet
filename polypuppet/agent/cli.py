#!/usr/bin/env python3
import logging
import multiprocessing as mp
import os
import sys

import click
import coloredlogs
from polypuppet import Config
from polypuppet.agent.agent import Agent
from polypuppet.exception import PolypuppetException
from polypuppet.log_format import set_clear_logs
from polypuppet.messages import Messages
from polypuppet.server.server import main as server_main
from polypuppet.server.server import Server


@click.group()
@click.option('-v', '--verbose', is_flag=True, help=Messages.help_verbose())
@click.option('-q', '--quiet', is_flag=True, help=Messages.help_quiet())
def cli(verbose, quiet):
    loglevel = logging.INFO
    if quiet:
        loglevel = logging.CRITICAL
    elif verbose:
        loglevel = logging.DEBUG
    set_clear_logs(loglevel)


@cli.command()
@click.argument('certname')
def autosign(certname):
    agent = Agent()
    has_certname = agent.autosign(certname)
    if not has_certname:
        sys.exit(1)


def check_login(response):
    if response:
        logging.info(Messages.logged_in())
    else:
        logging.warning(Messages.not_logged_in())
        sys.exit(1)


@cli.command()
@click.option('-u', '--username', prompt=True, help=Messages.help_username())
@click.password_option('-p', '--password', confirmation_prompt=False, help=Messages.help_password())
def login(username, password):
    agent = Agent()
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
        pe.print_with_exit()


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
            logging.info('Server stopped')
        return

    if daemon:
        process = mp.Process(target=start_server)
        process.start()
        os._exit(0)
    else:
        start_server()


@cli.command()
@click.argument('key', required=False)
@click.argument('value', required=False)
@click.option('-t', '--test', is_flag=True)
def config(key, test, value):
    global_config = Config()
    if key is None:
        for key, value in global_config.all().items():
            logging.info(key + '=' + value)
    elif value is None:
        logging.info(global_config[key])
    else:
        if not test:
            global_config.restricted_set(key, value)
        elif global_config[key] != value:
            sys.exit(1)


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
        logging.info(server_token)
    else:
        server_token = agent.get_token()
        if server_token != str():
            logging.info(server_token)
        else:
            logging.warning(Messages.token_not_generated())
            sys.exit(1)


def main():
    try:
        cli()
    except PolypuppetException as exception:
        exception.print_with_exit()


if __name__ == "__main__":
    main()
