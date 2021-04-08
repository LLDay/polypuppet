import asyncio

from polypuppet.daemon.api import Api
from polypuppet.config import Config
from polypuppet.daemon import Daemon
import polypuppet.polypuppet_pb2 as proto


class _DaemonSender:
    def __init__(self, function):
        self.function = function
        config = Config()
        self.ip = config['AGENT_CONTROL_IP']
        self.port = config['AGENT_CONTROL_PORT']

    async def _connect_daemon(self, *args):
        try:
            reader, writer = await asyncio.open_connection(self.ip, self.port)
        except:
            return proto.Message()

        message = proto.Message()
        message.type = proto.API
        message.api_function = self.function
        for arg in args:
            message.api_args.append(str(arg))

        writer.write(message.SerializeToString())
        writer.write_eof()
        await writer.drain()

        raw_message = await reader.read()
        writer.close()
        await writer.wait_closed()

        message = proto.Message()
        message.ParseFromString(raw_message)
        return message

    def __call__(self, *args):
        return asyncio.run(self._connect_daemon(*args))


class DaemonAccessor(Api):
    def __getattribute__(self, attr):
        if attr == 'run_daemon':
            daemon = Daemon()
            return daemon.forked_run
        else:
            return _DaemonSender(attr)
