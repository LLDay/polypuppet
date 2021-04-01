import asyncio
import logging
from polypuppet import config
from polypuppet import polypuppet_pb2 as proto


class AgentControllerProtocol(asyncio.Protocol):
    def __init__(self, message):
        self.message = message

    def connection_made(self, transport):
        transport.write(b'' + self.message.SerializeToString())
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data))

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()


class AgentListenerProtocol(asyncio.Protocol):
    def __init__(self, message_handler):
        self.buffer = bytearray()
        self.message_handler = message_handler

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        logging.info('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        self.buffer.extend(data)
        message = proto.Message()
        message.ParseFromString(self.buffer)
        self.message_handler(message)
