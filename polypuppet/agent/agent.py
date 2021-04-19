import asyncio
import os
import multiprocessing as mp

from polypuppet import proto
from polypuppet.server import server
from polypuppet.config import Config
from polypuppet.puppet import Puppet
from polypuppet.messages import error


class Agent:
    def __init__(self):
        self._config = Config()

    async def _connect(self, ip, port, message):
        try:
            reader, writer = await asyncio.open_connection(ip, port)
            writer.write(message.SerializeToString())
            writer.write_eof()
            await writer.drain()

            raw_message = await reader.read()
            writer.close()
            await writer.wait_closed()

            response = proto.Message()
            response.ParseFromString(raw_message)
            return response
        except Exception as e:
            error.agent_cannot_connect_server(ip, port)

    def connect_lan(self, message):
        ip = self._config['CONTROL_IP']
        port = self._config['CONTROL_PORT']
        return asyncio.run(self._connect(ip, port, message))

    def connect_wan(self, message):
        ip = self._config['PRIMARY_SERVER_DOMAIN']
        port = self._config['SERVER_PORT']
        return asyncio.run(self._connect(ip, port, message))

    def autosign(self, certname):
        message = proto.Message()
        message.type = proto.AUTOSIGN
        message.certname = certname
        response = self.connect_lan(message)
        return response.ok

    def login(self, username, password):
        message = proto.Message()
        message.type = proto.LOGIN
        message.username = username
        message.password = password
        response = self.connect_wan(message)
        if response.ok:
            puppet = Puppet()
            puppet.certname(response.certname)
            puppet.sync(noop=True)
        return response.ok

    def stop_server(self):
        message = proto.Message()
        message.type = proto.STOP
        self.connect_lan(message)
