import asyncio
import socket
import sys
import os
import time

import polypuppet.agent.daemon as daemon
from collections.abc import Iterable
from polypuppet import config
from polypuppet import polypuppet_pb2 as proto
from polypuppet.agent.connection import ClientConnection


def send_to_daemon(message, handler=None):
    connection = ClientConnection(message, handler)
    ip = config['AGENT_CONTROL_IP']
    port = config['AGENT_CONTROL_PORT']
    loop = asyncio.get_event_loop()
    try:
        coro = loop.create_connection(lambda: connection, ip, port)
        loop.run_until_complete(coro)
    except:
        print('Daemon is not running')


def start_daemon(**kwargs):
    daemon.main()
    os._exit(0)


def stop_daemon(**kwargs):
    message = proto.Message()
    message.type = proto.STOP
    send_to_daemon(message)


def login(username='', password='', **kwargs):
    username = kwargs.get('username', username)
    password = kwargs.get('password', password)

    message = proto.Message()
    message.type = proto.LOGIN
    message.username = username
    message.password = password
    send_to_daemon(message)
