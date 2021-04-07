import asyncio
import socket
from polypuppet import polypuppet_pb2 as proto


class Receiver(asyncio.Protocol):
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
