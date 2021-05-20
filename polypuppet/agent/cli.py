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

    coloredlogs.install(level=loglevel)


@cli.command()
@click.argument('certname')
def autosign(certname):
    agent = Agent()
    has_certname = agent.autosign(certname)
    if not has_certname:
        sys.exit(1)


def check_login(response):
    if response:
        print(Messages.logged_in())
    else:
        print(Messages.not_logged_in())
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
@click.option('-c', '--clean', is_flag=True, help=Messages.help_server_clean())
@click.option('-s', '--stop', is_flag=True, help=Messages.help_server_stop())
def server(daemon, restart, clean, stop):
    if restart or stop:
        try:
            agent = Agent()
            agent.stop_server()
        except PolypuppetException:
            pass

    if stop:
        return

    if clean:
        server_instance = Server()
        server_instance.clean_certificate()

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
            print(key + '=' + value)
    elif value is None:
        print(global_config[key])
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
        print(server_token)
    else:
        server_token = agent.get_token()
        if server_token != str():
            print(server_token)
        else:
            print(Messages.token_not_generated())
            sys.exit(1)


def main():
    try:
        cli()
    except PolypuppetException as exception:
        exception.print_with_exit()


if __name__ == "__main__":
    main()
