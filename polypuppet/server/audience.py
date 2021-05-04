class Audience:
    def __init__(self, number, platform, release, uuid):
        self.number = str(number)
        self.platform = platform
        self.release = release
        self.uuid = hex(uuid)[2:]

    def certname(self):
        components = ['audience', self.number,
                      self.platform, self.release, self.uuid]
        components = [c.lower() for c in components if len(c) > 0]
        return '.'.join(components)
