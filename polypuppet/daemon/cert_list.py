import asyncio


class CertList:
    def __init__(self):
        self.certlist = []
        self.timeout = 20

    async def _timeout(self, certname):
        await asyncio.sleep(self.timeout)
        if certname in self.certlist:
            self.certlist.remove(certname)
            print('Deleted certname', certname)

    def add(self, certname):
        self.certlist.append(certname)
        print('Added certname', certname)
        asyncio.ensure_future(self._timeout(certname))

    def has(self, certname):
        has_certname = certname in self.certlist
        if has_certname:
            self.certlist.remove(certname)
        return has_certname
