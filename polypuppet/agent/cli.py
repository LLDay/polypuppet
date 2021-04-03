import argparse
import polypuppet.agent.api as api
from polypuppet.request import request
from polypuppet.puppet import Puppet


def _dummy(*args, **kwargs):
    pass


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.set_defaults(handler=_dummy)
    subparsers = parser.add_subparsers()

    login_parser = subparsers.add_parser('login')
    login_parser.set_defaults(handler=api.login)
    login_parser.add_argument('username')
    login_parser.add_argument('password')

    daemon_parser = subparsers.add_parser('daemon')
    daemon_parser.set_defaults(handler=api.start_daemon)

    stop_parser = subparsers.add_parser('stop')
    stop_parser.set_defaults(handler=api.stop_daemon)

    parsed = parser.parse_args()
    parsed.handler(**vars(parsed))


if __name__ == "__main__":
    parse_arguments()
