import asyncio

from polypuppet import config
from polypuppet import polypuppet_pb2 as proto
from polypuppet.agent.connection import AgentControllerProtocol
from polypuppet.agent.daemon import daemon_run


def _connect_daemon(message):
    loop = asyncio.get_event_loop()
    ip = config['AGENT_CONTROL_IP']
    port = config['AGENT_CONTROL_PORT']
    coro = loop.create_connection(
        lambda: AgentControllerProtocol(message), ip, port)
    client = loop.run_until_complete(coro)


def login(username='', password='', **kwargs):
    message = proto.Message()
    message.command = proto.Command.LOGIN
    message.username = kwargs.get('username', username)
    message.password = kwargs.get('password', password)
    _connect_daemon(message)


def daemon(**kwargs):
    if kwargs.get('stop', False):
        message = proto.Message()
        message.command = proto.Command.STOP
        _connect_daemon(message)
    else:
        daemon_run()
