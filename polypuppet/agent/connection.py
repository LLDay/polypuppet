import asyncio
import socket
from polypuppet import config
from polypuppet import polypuppet_pb2 as proto


class ClientConnection(asyncio.Protocol):
    def __init__(self, message, handler=None):
        self.buffer = bytearray()
        self.message = message
        self.message_handler = handler

    def connection_made(self, transport):
        self.transport = transport
        transport.write(self.message.SerializeToString())

    def data_received(self, data):
        if handler != None:
            self.buffer.extend(data)
            message = proto.Message()
            message.ParseFromString(self.buffer)
            if self.message_handler is not None:
                self.message_handler(message, self.transport)


class ServerConnection(asyncio.Protocol):
    def __init__(self, message_handler):
        self.buffer = bytearray()
        self.message_handler = message_handler

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self.buffer.extend(data)
        message = proto.Message()
        message.ParseFromString(self.buffer)
        self.message_handler(message, self.transport)


def send_to_server(message, handler=None):
    loop = asyncio.get_event_loop()
    ip, port = socket.gethostbyname(config['PRIMARY_SERVER_DOMAIN'])
    coro = loop.create_connection(
        lambda: ClientConnection(message, handler), ip, port)
    try:
        client = loop.run_until_complete(coro)
    except:
        print('Cannot connect to the server')
