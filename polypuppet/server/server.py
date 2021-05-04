import asyncio
import pathlib
import socket
import ssl
import warnings

from polypuppet import proto
from polypuppet import Config
from polypuppet import PuppetServer, Puppet
from polypuppet.definitions import POLYPUPPET_PEM_NAME, EOF_SIGN
from polypuppet.messages import info, error
from polypuppet.server.audience import Audience
from polypuppet.server.authentication import authenticate
from polypuppet.server.cert_list import CertList
from polypuppet.server.person import PersonType
from polypuppet.server.token import Token


class Server:
    def __init__(self):
        self.config = Config()
        self.puppet = Puppet()
        self.puppetserver = PuppetServer()
        self.certlist = CertList()
        self.token = Token()

    async def _read_message(self, reader):
        raw_message = await reader.readuntil(EOF_SIGN)
        raw_message = raw_message[:-len(EOF_SIGN)]
        message = proto.Message()
        with warnings.catch_warnings():
            try:
                message.ParseFromString(raw_message)
            except:
                pass
        return message

    async def _answer(self, writer, response):
        response.type == proto.RESPONSE
        writer.write(response.SerializeToString())
        writer.write(EOF_SIGN)
        await writer.drain()

    #
    # Agent connection handlers
    #

    async def agent_message_handler(self, reader, writer):
        message = await self._read_message(reader)
        response = proto.Message()

        if message.type == proto.LOGIN:
            response = self._handle_login(message)

        await self._answer(writer, response)

    def _handle_login(self, message):
        profile = message.profile
        if profile.username != str():
            return self._handle_user_login(profile.username, profile.password)
        elif profile.audience != 0:
            return self._handle_audience_login(profile, message.token)
        else:
            return proto.Message()

    def wait_for_certificate(self, certname):
        self.puppetserver.clear_certname(certname)
        self.certlist.append(certname)
        info.wait_for_cert(certname)

    def _handle_user_login(self, username, password):
        response = proto.Message()
        person = authenticate(username, password)
        if person.valid():
            certname = person.certname()
            print('certname', certname)
            response.certname = certname
            response.profile.flow = person.flow
            response.profile.group = person.group
            response.ok = True
            self.wait_for_certificate(certname)
        return response

    def _handle_audience_login(self, profile, token):
        response = proto.Message()
        if len(token) > 0 and token == self.token:
            audience = Audience(profile.audience, profile.platform,
                                profile.release, profile.uuid)
            certname = audience.certname()
            response.ok = True
            response.certname = certname
            response.profile.audience = profile.audience
            self.wait_for_certificate(certname)
        return response

    #
    # Control connection handlers
    #

    async def control_message_handler(self, reader, writer):
        message = await self._read_message(reader)
        response = proto.Message()

        if message.type == proto.AUTOSIGN:
            response = self._handle_autosign(message.certname)
        elif message.type == proto.TOKEN:
            response = self._handle_token(message.taction, message.token)
        elif message.type == proto.STOP:
            await self.stop()

        await self._answer(writer, response)

    def _handle_autosign(self, certname):
        response = proto.Message()
        response.ok = self.certlist.check_and_remove(certname)
        info.request_for_cert(certname, response.ok)
        return response

    def _handle_token(self, taction, token):
        response = proto.Message()
        response.ok = True
        if taction == proto.GET:
            response.token = self.token.get()
        elif taction == proto.NEW:
            response.token = self.token.new()
        elif taction == proto.CLEAR:
            response.token == self.token.clear()
        return response

    #
    # SSL setup
    #

    def get_ssl_context(self):
        ssldir = pathlib.Path(self.config['SSLDIR'])
        ssl_cert = ssldir / ('certs/' + POLYPUPPET_PEM_NAME + '.pem')
        ssl_private = ssldir / ('private_keys/' + POLYPUPPET_PEM_NAME + '.pem')
        if not ssl_cert.exists() or not ssl_private.exists():
            error.must_call_setup_server()

        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ssl_context.load_cert_chain(ssl_cert, ssl_private)
        return ssl_context

    async def _create_ssl_connection(self, ip, port, handler):
        ssl_context = self.get_ssl_context()
        try:
            sock = socket.create_server((ip, port))
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

        except Exception as e:
            error.server_cannot_bind(ip, port, e)
        wrapper = ssl_context.wrap_socket(sock, server_side=True)
        return await asyncio.start_server(handler, sock=wrapper)

    #
    # Execution control
    #

    async def run(self):
        server_ip = self.config['SERVER_DOMAIN']
        server_port = int(self.config['SERVER_PORT'])
        control_ip = 'localhost'
        control_port = int(self.config['CONTROL_PORT'])

        self.agent_connection = await self._create_ssl_connection(
            server_ip, server_port, self.agent_message_handler)
        self.control_connection = await self._create_ssl_connection(
            control_ip, control_port, self.control_message_handler)

        await asyncio.wait([self.agent_connection.serve_forever(), self.control_connection.serve_forever()])
        info.server_stopped()

    async def stop(self):
        self.agent_connection.close()
        self.control_connection.close()
        await asyncio.gather(self.agent_connection.wait_closed(), self.control_connection.wait_closed())


def main():
    server = Server()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
