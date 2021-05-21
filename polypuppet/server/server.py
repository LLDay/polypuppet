import logging
import os
import ssl
from concurrent import futures
from pathlib import Path

import grpc
from google.protobuf.empty_pb2 import Empty
from polypuppet import Config
from polypuppet import proto
from polypuppet import Puppet
from polypuppet import PuppetServer
from polypuppet.exception import PolypuppetException
from polypuppet.messages import Messages
from polypuppet.polypuppet_pb2_grpc import add_LocalConnectionServicer_to_server
from polypuppet.polypuppet_pb2_grpc import add_RemoteConnectionServicer_to_server
from polypuppet.polypuppet_pb2_grpc import LocalConnection
from polypuppet.polypuppet_pb2_grpc import RemoteConnection
from polypuppet.server.audience import Audience
from polypuppet.server.authentication import authenticate
from polypuppet.server.cert_list import CertList
from polypuppet.server.person import PersonType
from polypuppet.server.token import Token


class Server(LocalConnection, RemoteConnection):
    def __init__(self):
        self.config = Config()
        self.puppet = Puppet()
        self.puppetserver = PuppetServer()
        self.certlist = CertList()
        self.token = Token()
        os.environ['GRPC_VERBOSITY'] = 'NONE'

        thread_pool = futures.ThreadPoolExecutor(max_workers=2)
        options = [('grpc.so_reuseport', 0)]
        self.local_server = grpc.server(thread_pool, options=options)
        self.remote_server = grpc.server(thread_pool, options=options)

    #
    # Agent connection handlers
    #

    def wait_for_certificate(self, certname):
        self.puppetserver.clean_certname(certname)
        self.certlist.append(certname)

    def login_user(self, credentials, context):
        username = credentials.username
        password = credentials.password

        profile = proto.Profile()
        person = authenticate(username, password)
        if person.valid():
            certname = person.certname()
            profile.ok = True
            profile.certname = certname
            profile.flow = person.flow
            profile.group = person.group

            if person.type == PersonType.STUDENT:
                profile.role = proto.STUDENT
            else:
                profile.role = proto.OTHER

            self.wait_for_certificate(certname)
        return profile

    def login_audience(self, credentials, context):
        profile = proto.Profile()
        token = self.token
        if not token.empty() and credentials.token == token:
            audience = Audience(credentials.audience, credentials.platform,
                                credentials.release, credentials.uuid)

            certname = audience.certname()
            profile.ok = True
            profile.role = proto.AUDIENCE
            profile.certname = certname
            profile.audience = credentials.audience
            self.wait_for_certificate(certname)
        return profile

    #
    # Control connection handlers
    #

    def autosign(self, request, context):
        response = proto.Autosign()
        response.ok = self.certlist.check_and_remove(request.certname)
        return response

    def manage_token(self, request, context):
        response = proto.Token()
        taction = request.taction
        if taction == proto.GET:
            response.token = self.token.get()
        elif taction == proto.NEW:
            response.token = self.token.new()
        elif taction == proto.CLEAR:
            self.token.clear()
        return response

    def stop(self, request, context):
        self.local_server.stop(5)
        self.remote_server.stop(5)
        return Empty()

    #
    # Certificates
    #

    def ensure_has_certificate(self):
        ssl_cert = self.config['SSL_CERT']
        ssl_private = self.config['SSL_PRIVATE']

        if not ssl_cert or not ssl_private:
            certname = self.puppet.certname()
            ssl_cert = 'certs/' + certname + '.pem'
            ssl_private = 'private_keys/' + certname + '.pem'

            ssldir = self.puppet.ssldir()
            ssl_cert = ssldir / ssl_cert
            ssl_private = ssldir / ssl_private

            self.config['SSL_CERT'] = ssl_cert.as_posix()
            self.config['SSL_PRIVATE'] = ssl_private.as_posix()

    #
    # Execution
    #

    def run(self):
        self.ensure_has_certificate()
        add_LocalConnectionServicer_to_server(self, self.local_server)
        add_RemoteConnectionServicer_to_server(self, self.remote_server)

        server_ip = self.config['SERVER_DOMAIN']
        server_port = self.config['SERVER_PORT']
        server_address = server_ip + ':' + server_port

        control_ip = 'localhost'
        control_port = self.config['CONTROL_PORT']
        control_address = control_ip + ':' + control_port

        ssl_cert = Path(self.config['SSL_CERT'])
        with open(ssl_cert, 'rb') as cert:
            ssl_cert = cert.read()

        ssl_private = Path(self.config['SSL_PRIVATE'])
        with open(ssl_private, 'rb') as private:
            ssl_private = private.read()

        credentials = grpc.ssl_server_credentials([(ssl_private, ssl_cert)])

        try:
            self.local_server.add_insecure_port(control_address)
            self.remote_server.add_secure_port(server_address, credentials)
        except Exception as exception:
            exception_message = Messages.server_already_runned()
            raise PolypuppetException(exception_message) from exception

        self.local_server.start()
        self.remote_server.start()

        logging.info(Messages.server_is_on(control_ip, control_port))
        logging.info(Messages.server_is_on(server_ip, server_port))

        self.local_server.wait_for_termination()
        self.remote_server.wait_for_termination()
        logging.info(Messages.server_stopped())


def main():
    server = Server()
    server.run()


if __name__ == "__main__":
    main()
