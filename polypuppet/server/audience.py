from dataclasses import dataclass

from polypuppet import proto


@dataclass
class Audience:
    building: int = -1
    audience: int = -1
    token: str = str()
    pc: proto.PC = proto.PC()

    def deserialize(self, message):
        self.building = message.building
        self.audience = message.audience
        self.token = message.token
        self.pc = message.pc

    def certname(self):
        components = ['audience', self.building, self.audience,
                      self.pc.platform, self.pc.release, self.pc.uuid]
        return '.'.join(str(c) for c in components if c != str())
