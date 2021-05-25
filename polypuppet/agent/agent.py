import logging
import os
import platform
import ssl
import uuid

import grpc
from google.protobuf.empty_pb2 import Empty
from polypuppet import proto
from polypuppet.agent.pc import Pc
from polypuppet.config import Config
from polypuppet.exception import PolypuppetException
from polypuppet.messages import Messages
from polypuppet.polypuppet_pb2_grpc import LocalConnectionStub
from polypuppet.polypuppet_pb2_grpc import RemoteConnectionStub
from polypuppet.puppet import Puppet


class Agent:
    def __init__(self):
        self.config = Config()
        self.connectin_timeout = 0.5
        self.puppet = Puppet()

    #
    # Server connection
    #

    def check_connection(self, channel, domain, port):
        try:
            grpc.channel_ready_future(channel).result(self.connectin_timeout)
        except grpc.FutureTimeoutError as error:
            error_message = Messages.cannot_connect_to_server(domain, port)
            raise PolypuppetException(error_message) from error

    def get_local_stub(self):
        domain = 'localhost'
        port = self.config['CONTROL_PORT']
        channel = grpc.insecure_channel(domain + ':' + str(port))
        self.check_connection(channel, domain, port)
        return LocalConnectionStub(channel)

    def get_secure_channel(self, domain, port):
        server_cert = self.puppet.get_ca()
        credentials = grpc.ssl_channel_credentials(server_cert)
        return grpc.secure_channel(domain + ':' + str(port), credentials)

    def get_remote_stub(self):
        domain = self.config['SERVER_DOMAIN']
        port = self.config['SERVER_PORT']
        channel = self.get_secure_channel(domain, port)

        try:
            self.check_connection(channel, domain, port)
        except PolypuppetException:
            logging.warning(Messages.try_to_update_certificate_from(domain))
            self.puppet.download_ca()
            channel.close()
            channel = self.get_secure_channel(domain, port)
            self.check_connection(channel, domain, port)

        return RemoteConnectionStub(channel)

    def _token_action(self, action):
        message = proto.Token()
        message.taction = action
        local_stub = self.get_local_stub()
        response = local_stub.manage_token(message)
        return response.token

    def get_token(self):
        return self._token_action(proto.GET)

    def clear_token(self):
        return self._token_action(proto.CLEAR)

    def update_token(self):
        return self._token_action(proto.NEW)

    def autosign(self, certname):
        message = proto.Certname()
        message.certname = certname
        local_stub = self.get_local_stub()
        response = local_stub.autosign(message)
        return response.ok

    #
    # Login
    #

    def on_login(self, response):
        certname = response.certname

        ssldir = self.puppet.ssldir()
        ssl_cert = ssldir / ('certs/' + certname + '.pem')
        ssl_private = ssldir / ('private_keys/' + certname + '.pem')

        self.config['AGENT_CERTNAME'] = certname
        self.config['AUDIENCE'] = str(response.audience)
        self.config['BUILDING'] = str(response.building)
        self.config['ROLE'] = proto.Role.Name(response.role).lower()
        self.config['SSL_CERT'] = ssl_cert.as_posix()
        self.config['SSL_PRIVATE'] = ssl_private.as_posix()
        self.config['STUDENT_FLOW'] = response.flow
        self.config['STUDENT_GROUP'] = response.group

        self.puppet.certname(response.certname)
        return self.puppet.sync(noop=True)

    def audience(self, building, number, token):
        message = proto.Audience()
        message.token = token
        message.building = building
        message.audience = number

        pc = Pc()
        message.pc.uuid = pc.uuid
        message.pc.platform = pc.platform
        message.pc.release = pc.release

        remote_stub = self.get_remote_stub()
        response = remote_stub.login_audience(message)
        if response.ok:
            self.on_login(response)
        return response.ok

    def login(self, username, password):
        message = proto.User()
        message.username = username
        message.password = password

        remote_stub = self.get_remote_stub()
        response = remote_stub.login_user(message)
        if response.ok:
            if not self.on_login(response):
                raise PolypuppetException(Messages.agent_login_error())
        return response.ok

    def stop_server(self):
        try:
            local_stub = self.get_local_stub()
            local_stub.stop(Empty())
            return True
        except PolypuppetException:
            return False
