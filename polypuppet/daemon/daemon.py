import asyncio
import multiprocessing as mp
import os

from polypuppet import polypuppet_pb2 as proto
from polypuppet.config import Config
from polypuppet.connection import Receiver, send_to_server
from polypuppet.puppet import Puppet


class Daemon:
    def __init__(self):
        self.config = Config()
        self.puppet = Puppet()
        self.ip = self.config['AGENT_CONTROL_IP']
        self.port = self.config['AGENT_CONTROL_PORT']
        self.loop = asyncio.new_event_loop()

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
        return send_to_server(message, handler=self._login_response)

    def sync(self):
        self.puppet.sync(noop=True)

    def accept(self):
        puppet_info = self.puppet.sync(noop=False)

    def stop_daemon(self):
        self.loop.call_soon(self.loop.stop)

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
        elif message.type == proto.API:
            output = getattr(self, message.api_function)(*message.api_args)
            answer = proto.Message()
            answer.type = proto.OUT
            if output is not None:
                answer.output = str(output)
            transport.write(answer.SerializeToString())

    def _run_new_process(self):
        coro = self.loop.create_server(
            lambda: Receiver(self.control_message_handler), self.ip, self.port)
        try:
            self.loop.run_until_complete(coro)
            print('Start daemon')
            print('Listen to the local port', self.port)
            print('Forked into the process with pid', os.getpid())
            self.loop.run_forever()
        except:
            print('Daemon has been already runned')
        finally:
            self.loop.close()

    def run(self):
        if os.getuid() != 0:
            print('Daemon must run with superuser priviliges')
            return
        process = mp.Process(target=self._run_new_process, daemon=True)
        process.start()


def main():
    daemon = Daemon()
    daemon.run()


if __name__ == "__main__":
    main()
