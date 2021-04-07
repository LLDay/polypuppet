import asyncio

from polypuppet.daemon.api import Api
from polypuppet.connection import send_to_daemon
import polypuppet.polypuppet_pb2 as proto
import polypuppet.daemon.daemon as daemon


class _DaemonSender:
    def __init__(self, function):
        self.function = function
        self.loop = asyncio.get_event_loop()
        self.fut = self.loop.create_future()

    def _handler(self, message, transport):
        if message.type == proto.OUT:
            self.fut.set_result(message.output)

    def __call__(self, *args):
        message = proto.Message()
        message.type = proto.API
        message.api_function = self.function
        for arg in args:
            message.api_args.append(str(arg))

        if send_to_daemon(message, self._handler):
            self.loop.run_until_complete(asyncio.wait([self.fut]))
            return self.fut.result()


class DaemonAccessor(Api):
    def __getattribute__(self, attr):
        if attr == 'run_daemon':
            return daemon.main
        else:
            return _DaemonSender(attr)
