import os
import platform
import uuid
from dataclasses import dataclass

import distro


@dataclass(init=False)
class Pc:
    uuid: int = uuid.getnode()
    platform: str
    release: str

    def __init__(self):
        if platform.system() == 'Linux':
            self.platform = distro.id().lower()
            self.release = distro.major_version().lower()
        else:
            os_name = platform.system()
            if os_name == str():
                os_name = os.name
            self.platform = os_name.lower()
            self.release = platform.release().lower()
