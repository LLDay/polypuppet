import asyncio
import logging
import socket
import ssl
import warnings
from pathlib import Path

from polypuppet import Config
from polypuppet import proto
from polypuppet import Puppet
from polypuppet import PuppetServer
from polypuppet.definitions import EOF_SIGN
from polypuppet.definitions import POLYPUPPET_PEM_NAME
from polypuppet.exception import PolypuppetException
from polypuppet.messages import Messages
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
        self.agent_connection = None
        self.control_connection = None

    async def _read_message(self, reader):
        raw_message = await reader.readuntil(EOF_SIGN)
        raw_message = raw_message[:-len(EOF_SIGN)]
        message = proto.Message()
        with warnings.catch_warnings():
            try:
                message.ParseFromString(raw_message)
                logging.debug(Messages.server_receives(message))
            except Exception:
                address = reader._transport.get_extra_info('peername')
                logging.exception(Messages.wrong_message_from(address))
        return message

    async def _answer(self, writer, response):
        response.type = proto.RESPONSE
        logging.debug(Messages.server_sends(response))
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
        if profile.audience != 0:
            return self._handle_audience_login(profile, message.token)
        return proto.Message()

    def wait_for_certificate(self, certname):
        self.puppetserver.clean_certname(certname)
        self.certlist.append(certname)

    def _handle_user_login(self, username, password):
        response = proto.Message()
        person = authenticate(username, password)
        if person.valid():
            certname = person.certname()
            response.ok = True
            response.certname = certname
            response.profile.flow = person.flow
            response.profile.group = person.group

            if person.type == PersonType.STUDENT:
                response.profile.role = proto.STUDENT
            else:
                response.profile.role = proto.OTHER

            self.wait_for_certificate(certname)
        return response

    def _handle_audience_login(self, profile, token):
        response = proto.Message()
        if not self.token.empty() and token == self.token:
            audience = Audience(profile.audience, profile.platform,
                                profile.release, profile.uuid)
            certname = audience.certname()
            response.ok = True
            response.certname = certname
            response.profile.role = proto.AUDIENCE
            response.profile.audience = profile.audience
            self.wait_for_certificate(certname)
        return response

    #
    # Control connection handlers
    #

    async def control_message_handler(self, reader, writer):
        message = await self._read_message(reader)
        response = proto.Message()

        if message.type == proto.STOP:
            await self.stop()
        if message.type == proto.AUTOSIGN:
            response = self._handle_autosign(message.certname)
        elif message.type == proto.TOKEN:
            response = self._handle_token(message.taction)

        await self._answer(writer, response)

    def _handle_autosign(self, certname):
        response = proto.Message()
        response.ok = self.certlist.check_and_remove(certname)
        return response

    def _handle_token(self, taction):
        response = proto.Message()
        response.ok = True
        if taction == proto.GET:
            response.token = self.token.get()
        elif taction == proto.NEW:
            response.token = self.token.new()
        elif taction == proto.CLEAR:
            self.token.clear()
        return response

    #
    # SSL setup
    #

    def get_ssl_context(self):
        self.ensure_has_certificate()
        ssl_cert = Path(self.config['SSL_SERVER_CERT'])
        ssl_private = Path(self.config['SSL_SERVER_PRIVATE'])

        print(self.config['SSL_SERVER_CERT'],
              self.config['SSL_SERVER_PRIVATE'])
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ssl_context.load_cert_chain(ssl_cert, ssl_private)
        return ssl_context

    async def _create_ssl_connection(self, ip, port, handler):
        ssl_context = self.get_ssl_context()
        try:
            sock = socket.create_server((ip, port))
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

        except OSError as os_error:
            raise PolypuppetException(os_error.strerror) from os_error
        except Exception as exception:
            raise PolypuppetException(str(exception)) from exception

        wrapper = ssl_context.wrap_socket(sock, server_side=True)
        return await asyncio.start_server(handler, sock=wrapper)

    def clean_certificate(self):
        self.puppetserver.clean_certname(POLYPUPPET_PEM_NAME)
        self.puppet.clean_certname(POLYPUPPET_PEM_NAME)
        self.config['SSL_SERVER_CERT'] = ''
        self.config['SSL_SERVER_PRIVATE'] = ''

    def ensure_has_certificate(self):
        ssl_cert = self.config['SSL_SERVER_CERT']
        ssl_private = self.config['SSL_SERVER_PRIVATE']

        if not ssl_cert or not ssl_private:
            ssl_cert = 'certs/' + POLYPUPPET_PEM_NAME + '.pem'
            ssl_private = 'private_keys/' + POLYPUPPET_PEM_NAME + '.pem'

            ssldir = self.puppet.ssldir()
            ssl_cert = ssldir / ssl_cert
            ssl_private = ssldir / ssl_private

            self.config['SSL_SERVER_CERT'] = ssl_cert.as_posix()
            self.config['SSL_SERVER_PRIVATE'] = ssl_private.as_posix()

        if not Path(ssl_cert).exists() or not Path(ssl_private).exists():
            logging.warning(Messages.certificate_is_not_presented())
            generated = self.puppetserver.generate(POLYPUPPET_PEM_NAME)
            if not generated:
                logging.warning(Messages.trying_to_regenerate_certificate())
                self.clean_certificate()
                generated = self.puppetserver.generate(POLYPUPPET_PEM_NAME)

            # Recheck after second generation
            if not generated:
                exception_message = Messages.cannot_generate_certificate()
                raise PolypuppetException(exception_message)

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
        logging.info(Messages.server_is_on(control_ip, control_port))

        self.control_connection = await self._create_ssl_connection(
            control_ip, control_port, self.control_message_handler)
        logging.info(Messages.server_is_on(control_ip, control_port))

        await asyncio.wait([self.agent_connection.serve_forever(), self.control_connection.serve_forever()])
        logging.info(Messages.server_stopped())

    async def stop(self):
        self.agent_connection.close()
        self.control_connection.close()
        await asyncio.gather(self.agent_connection.wait_closed(), self.control_connection.wait_closed())


def main():
    server = Server()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
