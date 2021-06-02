from dataclasses import dataclass

from polypuppet import proto


@dataclass
class Classroom:
    building: int = -1
    classroom: int = -1
    token: str = str()
    pc: proto.PC = proto.PC()

    def deserialize(self, message):
        self.building = message.building
        self.classroom = message.classroom
        self.token = message.token
        self.pc = message.pc

    def certname(self):
        components = ['classroom', self.building, self.classroom,
                      self.pc.platform, self.pc.release, self.pc.uuid]
        return '.'.join(str(c) for c in components if c != str())
