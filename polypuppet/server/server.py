import asyncio

from polypuppet import proto
from polypuppet import Config
from polypuppet import PuppetServer
from polypuppet.person import PersonType
from polypuppet.server.cert_list import CertList
from polypuppet.server.authentication import authenticate


class Server:
    def __init__(self):
        config = Config()
        self.puppetserver = PuppetServer()
        self.certlist = CertList()
        self.server_ip = config['PRIMARY_SERVER_DOMAIN']
        self.server_port = config['SERVER_PORT']
        self.control_ip = config['CONTROL_IP']
        self.control_port = config['CONTROL_PORT']

    async def _read_message(self, reader):
        raw_message = await reader.read()
        message = proto.Message()
        message.ParseFromString(raw_message)
        return message

    async def _answer(self, writer, response):
        writer.write(response.SerializeToString())
        writer.write_eof()
        await writer.drain()

    async def agent_message_handler(self, reader, writer):
        message = await self._read_message(reader)
        response = proto.Message()
        response.type = proto.RESPONSE

        if message.type == proto.LOGIN:
            certname = await self.login(message.username, message.password)
            if certname is not None:
                response.certname = certname
                response.ok = True
        await self._answer(writer, response)

    async def control_message_handler(self, reader, writer):
        message = await self._read_message(reader)
        response = proto.Message()
        response.type = proto.RESPONSE

        if message.type == proto.AUTOSIGN:
            response.ok = self.certlist.check_and_remove(message.certname)
            print('Autosign request')
            print('Result', response.ok)
        elif message.type == proto.STOP:
            await self.stop()
        await self._answer(writer, response)

    async def login(self, username, password):
        person = authenticate(username, password)
        if not person.valid():
            return
        certname = ''
        if person.type == PersonType.STUDENT:
            certname += 'student.'
            certname += person.group.replace('/', '.') + '.'
        certname += username.split('@')[0]
        self.puppetserver.clear_certname(certname)
        self.certlist.append(certname)
        return certname

    async def run(self):
        try:
            self.agent_connection = await asyncio.start_server(self.agent_message_handler, self.server_ip, self.server_port)
            self.control_connection = await asyncio.start_server(self.control_message_handler, self.control_ip, self.control_port)
        except Exception as e:
            print(e)
            return
        await asyncio.wait([self.agent_connection.serve_forever(), self.control_connection.serve_forever()])
        print('Server stopped successfully')

    async def stop(self):
        self.agent_connection.close()
        self.control_connection.close()
        await asyncio.gather(self.agent_connection.wait_closed(), self.control_connection.wait_closed())


def main():
    server = Server()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
