import asyncio
import multiprocessing as mp
import os

from polypuppet import config
from polypuppet import polypuppet_pb2 as proto
from polypuppet.agent.connection import send_to_server, ServerConnection
from polypuppet.puppet import Puppet


class Daemon:
    def __init__(self):
        self.ip = config['AGENT_CONTROL_IP']
        self.port = config['AGENT_CONTROL_PORT']
        self.loop = asyncio.new_event_loop()
        self.puppet = Puppet()

    def _login_response(self, message, transport):
        if message.type != proto.LOGIN:
            return
        certname = message.certname
        self.puppet.config('certname', certname, section='agent')

    def login(self, username, password):
        message = proto.Message()
        message.type = proto.LOGIN
        message.username = username
        message.password = password
        send_to_server(message, handler=self._login_response)

    def sync(self):
        self.puppet.sync(noop=True)

    def accept(self):
        puppet_info = self.puppet.sync(noop=False)

    def control_message_handler(self, message, transport):
        if message.type == proto.UNKNOWN:
            print('Undefined command')
        elif message.type == proto.STOP:
            self.stop()
        elif message.type == proto.LOGIN:
            self.login(message.username, message.password)
        elif message.type == proto.SYNC:
            self.sync()
        elif message.type == proto.ACCEPT:
            self.accept()

    def _new_process(self):
        self.loop.run_forever()

    def run(self):
        if os.getuid() != 0:
            print('Daemon must run with superuser priviliges')
            return

        print('Start daemon')
        coro = self.loop.create_server(
            lambda: ServerConnection(self.control_message_handler), self.ip, self.port)
        print('Listen to the local port', self.port)

        self.loop.run_until_complete(coro)
        process = mp.Process(target=self._new_process, daemon=True)
        process.start()
        print('Forked into the process with pid', process.pid)

    def _threadsafe_stop(self):
        self.loop.stop()
        print('Daemon is successfully stopped')

    def stop(self):
        self.loop.call_soon_threadsafe(self._threadsafe_stop)


def main():
    daemon = Daemon()
    daemon.run()


if __name__ == "__main__":
    main()
