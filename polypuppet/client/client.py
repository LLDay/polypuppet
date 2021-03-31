from polypuppet.request import request
from polypuppet.puppet import Puppet
import argparse


def login(namespace):
    print(namespace)
    r = request(username=namespace.username,
                password=namespace.password, path='/login')
    json = r.json()
    certname = json['certname']
    puppet = Puppet()
    puppet.config('certname', certname)


def _dummy(*args):
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.set_defaults(handler=_dummy)
    subparsers = parser.add_subparsers()

    login_parser = subparsers.add_parser('login')
    login_parser.set_defaults(handler=login)
    login_parser.add_argument('username', nargs=1)
    login_parser.add_argument('password', nargs=1)

    parsed = parser.parse_args()
    parsed.handler(parsed)


if __name__ == "__main__":
    main()
