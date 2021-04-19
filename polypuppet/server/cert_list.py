import asyncio
from polypuppet import Config


class CertList:
    def __init__(self):
        config = Config()
        self.certlist = []
        self.timeout = int(config['NEW_CERT_LIFETIME'])

    async def _certname_stopwatch(self, certname):
        await asyncio.sleep(self.timeout)
        self.remove(certname)

    def remove(self, certname):
        if certname in self.certlist:
            self.certlist.remove(certname)
            print('Deleted certname', certname)

    def append(self, certname):
        self.certlist.append(certname)
        print('Added certname', certname)
        asyncio.ensure_future(self._certname_stopwatch(certname))

    def check_and_remove(self, certname):
        has_certname = certname in self.certlist
        self.remove(certname)
        return has_certname

        if has_certname:
            print('Certname in server')
            self.certlist.remove(certname)

    def __contains__(self, certname):
        return certname in self.certlist
