import asyncio
import multiprocessing as mp
import os

from polypuppet import polypuppet_pb2 as proto
from polypuppet.config import Config
from polypuppet.puppet import Puppet
from polypuppet.daemon.api import Api


class Daemon(Api):
    def __init__(self):
        self.config = Config()
        self.puppet = Puppet()
        self.ip = self.config['AGENT_CONTROL_IP']
        self.port = self.config['AGENT_CONTROL_PORT']

    async def stop_daemon(self):
        self.server.close()
        await self.server.wait_closed()

    async def daemon_connection_handler(self, reader, writer):
        raw_message = await reader.read()
        message = proto.Message()
        message.ParseFromString(raw_message)

        output = await getattr(self, message.api_function)(*message.api_args)
        response = proto.Message()
        response.type = proto.OUT
        if output is not None:
            response.output = str(output)
        writer.write(response.SerializeToString())
        writer.write_eof()
        await writer.drain()

    async def run(self):
        if os.getuid() != 0:
            print('Daemon must run with superuser priviliges')
            return
        try:
            self.server = await asyncio.start_server(
                self.daemon_connection_handler, self.ip, self.port)
        except:
            print('Daemon has been already runned')
            return

        print('Start daemon')
        print('Listen to the local port', self.port)
        print('Forked into the process with pid', os.getpid())
        await asyncio.wait([self.server.serve_forever()])

    def forked_run(self):
        process = mp.Process(target=lambda: asyncio.run(
            self.run()), daemon=True)
        process.start()


def main():
    daemon = Daemon()
    asyncio.run(daemon.run())


if __name__ == "__main__":
    main()
