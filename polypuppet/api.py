import asyncio

from polypuppet.agent.api import AgentApi, AgentApiImpl
from polypuppet.daemon.api import ServerApi, DaemonApi
from polypuppet.config import Config
import polypuppet.polypuppet_pb2 as proto


class _Session:
    def __init__(self, function, ip, port):
        self.function = function
        config = Config()
        self.ip = ip
        self.port = port

    async def _connect(self, *args):
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
        return asyncio.run(self._connect(*args))


class ApiAccessor(AgentApi, DaemonApi, ServerApi):
    def __init__(self):
        super(AgentApi, self).__init__()
        super(DaemonApi, self).__init__()
        super(ServerApi, self).__init__()

    def __getattribute__(self, attribute):
        config = Config()
        if hasattr(AgentApi, attribute):
            agent = AgentApiImpl()
            return getattr(agent, attribute)

        if hasattr(DaemonApi, attribute):
            ip = config['CONTROL_IP']
            port = config['CONTROL_PORT']
        elif hasattr(ServerApi, attribute):
            ip = config['PRIMARY_SERVER_DOMAIN']
            port = config['SERVER_PORT']
        else:
            message = 'Attribute ' + attribute + ' does not exist'
            raise AttributeError(message)
        return _Session(attribute, ip, port)
