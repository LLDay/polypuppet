import asyncio
import os
import pathlib
import platform
import socket
import ssl
import uuid

from polypuppet import proto
from polypuppet.definitions import EOF_SIGN
from polypuppet.config import Config
from polypuppet.puppet import Puppet
from polypuppet.messages import error


class Agent:
    def __init__(self):
        self.config = Config()

    #
    # Server connection
    #

    async def _connect(self, ip, port, message):
        ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.VerifyMode.CERT_NONE

        try:
            sock = socket.create_connection((ip, port))
        except Exception as e:
            error.agent_cannot_connect_server(ip, port)

        wrapper = ssl_context.wrap_socket(sock)
        reader, writer = await asyncio.open_connection(sock=wrapper)
        writer.write(message.SerializeToString())
        writer.write(EOF_SIGN)
        await writer.drain()

        raw_message = await reader.readuntil(EOF_SIGN)
        raw_message = raw_message[:-len(EOF_SIGN)]
        writer.close()
        await writer.wait_closed()

        response = proto.Message()
        response.ParseFromString(raw_message)
        return response

    def connect_lan(self, message):
        ip = 'localhost'
        port = self.config['CONTROL_PORT']
        return asyncio.run(self._connect(ip, port, message))

    def connect_wan(self, message):
        ip = self.config['SERVER_DOMAIN']
        port = self.config['SERVER_PORT']
        return asyncio.run(self._connect(ip, port, message))

    def set_token(self, token=None):
        message = proto.Message()
        message.type = proto.TOKEN
        if token is not None:
            message.taction = proto.SET
            message.token = token
        else:
            message.taction = proto.NEW
        response = self.connect_lan(message)
        return response.token

    def autosign(self, certname):
        message = proto.Message()
        message.type = proto.AUTOSIGN
        message.certname = certname
        response = self.connect_lan(message)
        return response.ok

    #
    # Login
    #

    def on_login(self, response):
        certname = response.certname
        ssldir = pathlib.Path(self.config['SSLDIR'])
        ssl_cert = ssldir / ('certs/' + certname + '.pem')
        ssl_private = ssldir / ('private_keys/' + certname + '.pem')

        self.config['AUDIENCE'] = str(response.profile.audience)
        self.config['STUDENT_FLOW'] = response.profile.flow
        self.config['STUDENT_GROUP'] = response.profile.group
        self.config['AGENT_CERTNAME'] = certname
        self.config['SSL_CERT'] = ssl_cert.as_posix()
        self.config['SSL_PRIVATE'] = ssl_private.as_posix()

        puppet = Puppet()
        puppet.certname(response.certname)
        puppet.sync(noop=True)

    def audience(self, number, token):
        os_name = platform.system()
        release = platform.release()
        if os_name == str():
            os_name = os.name()

        message = proto.Message()
        message.type = proto.LOGIN
        message.token = token
        message.profile.audience = number
        message.profile.uuid = uuid.getnode()
        message.profile.platform = os_name
        message.profile.release = release

        response = self.connect_wan(message)
        if response.ok:
            self.on_login(response)
        return response.ok

    def login(self, username, password):
        message = proto.Message()
        message.type = proto.LOGIN
        message.profile.username = username
        message.profile.password = password
        response = self.connect_wan(message)
        if response.ok:
            self.on_login(response)
        return response.ok

    def stop_server(self):
        message = proto.Message()
        message.type = proto.STOP
        self.connect_lan(message)
