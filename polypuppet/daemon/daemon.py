import asyncio
import multiprocessing as mp
import os

from inspect import iscoroutinefunction
from polypuppet import polypuppet_pb2 as proto
from polypuppet.person import PersonType
from polypuppet.daemon.api import ServerApi, DaemonApi
from polypuppet.daemon.authentication import authenticate
from polypuppet.daemon.cert_list import CertList
from polypuppet.config import Config


class Daemon(DaemonApi, ServerApi):
    def __init__(self):
        self.cert_list = CertList()
        self.config = Config()

        self.daemon_ip = self.config['CONTROL_IP']
        self.daemon_port = self.config['CONTROL_PORT']

        self.server_ip = self.config['PRIMARY_SERVER_DOMAIN']
        self.server_port = self.config['SERVER_PORT']

    #
    # Handlers
    #

    async def common_handler(self, reader, writer, api):
        raw_message = await reader.read()
        message = proto.Message()
        message.ParseFromString(raw_message)

        if hasattr(api, message.api_function):
            function = getattr(self, message.api_function)
            if iscoroutinefunction(function):
                output = await function(*message.api_args)
            else:
                output = function(*message.api_args)
        else:
            output = "Wrong api method"

        response = proto.Message()
        response.type = proto.OUT
        if output is not None:
            response.output = str(output)
        writer.write(response.SerializeToString())
        writer.write_eof()
        await writer.drain()

    async def server_handler(self, reader, writer):
        await self.common_handler(reader, writer, ServerApi)

    async def daemon_handler(self, reader, writer):
        await self.common_handler(reader, writer, DaemonApi)

    #
    # DaemonApi
    #

    async def stop_daemon(self):
        print('Stop')
        self.daemon_connection.close()
        self.server_connection.close()
        await self.daemon_connection.wait_closed()
        await self.server_connection.wait_closed()

    async def autoconf(self, certname):
        has_certname = certname in self.cert_list
        if has_certname:
            self.cert_list.remove(certname)
        return has_certname

    #
    # ServerApi
    #

    async def login(self, username, password):
        print(username, password)
        person = authenticate(username, password)
        if not person.valid():
            return
        certname = ''
        if person.type == PersonType.STUDENT:
            certname += 'student.'
            certname += person.group.replace('/', '.') + '.'
        certname += username.split('@')[0]
        self.cert_list.add(certname)
        return certname

    #
    # Methods
    #

    async def _run(self):
        if os.getuid() != 0:
            print('Daemon must run with superuser priviliges')
            return
        try:
            self.daemon_connection = await asyncio.start_server(self.daemon_handler, self.daemon_ip, self.daemon_port)
        except:
            print('Daemon has been already runned')
            return

        self.server_connection = await asyncio.start_server(self.server_handler, self.server_ip, self.server_port)
        print('Start daemon')
        print('Listen to the local port', self.daemon_port)
        print('Listen to the wan port', self.server_port)
        await asyncio.wait([self.daemon_connection.serve_forever(), self.server_connection.serve_forever()])

    def run(self):
        asyncio.run(self._run())

    def _fork(self):
        print('Forked into the process with pid', os.getpid())
        self.run()

    def fork(self):
        process = mp.Process(target=self._fork, daemon=True)
        process.start()


def main():
    daemon = Daemon()
    daemon.run()


if __name__ == "__main__":
    main()
