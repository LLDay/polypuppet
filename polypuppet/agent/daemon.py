import asyncio
import signal
from polypuppet import config
from polypuppet.agent.connection import AgentListenerProtocol
from polypuppet import polypuppet_pb2 as proto


def handle_message(message):
    if message.command == proto.Command.STOP:
        loop = asyncio.get_event_loop()
        loop.stop()


def handle_stop(sign, frame):
    loop = asyncio.get_event_loop()
    loop.call_soon_threadsafe(loop.stop)


def daemon_run():
    ip = config['AGENT_CONTROL_IP']
    port = config['AGENT_CONTROL_PORT']

    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        lambda: AgentListenerProtocol(handle_message), ip, port)
    server = loop.run_until_complete(coro)

    print('Serving on {}'.format(server.sockets[0].getsockname()))
    signal.signal(signal.SIGINT, handle_stop)
    loop.run_forever()


if __name__ == "__main__":
    daemon()
