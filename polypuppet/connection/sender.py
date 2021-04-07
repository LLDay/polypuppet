import asyncio
import socket
from polypuppet import polypuppet_pb2 as proto
from polypuppet import Config


class Sender(asyncio.Protocol):
    def __init__(self, message, handler=None):
        self.buffer = bytearray()
        self.message = message
        self.message_handler = handler

    def connection_made(self, transport):
        self.transport = transport
        transport.write(self.message.SerializeToString())

    def data_received(self, data):
        if self.message_handler != None:
            self.buffer.extend(data)
            message = proto.Message()
            message.ParseFromString(self.buffer)
            if self.message_handler is not None:
                self.message_handler(message, self.transport)


def _send_to(connection, ip, port):
    loop = asyncio.get_event_loop()
    try:
        coro = loop.create_connection(lambda: connection, ip, port)
        loop.run_until_complete(coro)
        return True
    except:
        return False


def send_to_daemon(message, handler=None):
    connection = Sender(message, handler)
    config = Config()
    ip = config['AGENT_CONTROL_IP']
    port = config['AGENT_CONTROL_PORT']
    return _send_to(connection, ip, port)


def send_to_server(message, handler=None):
    connection = Sender(message, handler)
    config = Config()
    ip, port = socket.gethostbyname(config['PRIMARY_SERVER_DOMAIN'])
    return _send_to(connection, ip, port)
