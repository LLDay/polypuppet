import asyncio
import logging

from polypuppet import Config
from polypuppet.messages import messages


class CertList:
    def __init__(self):
        config = Config()
        self.certlist = []
        self.timeout = int(config['CERT_WAITTIME'])

    async def _certname_stopwatch(self, certname):
        await asyncio.sleep(self.timeout)
        self.remove(certname)

    def remove(self, certname):
        if certname in self.certlist:
            logging.info(messages.stop_waiting_for_cert(certname))
            self.certlist.remove(certname)

    def append(self, certname):
        self.certlist.append(certname)
        logging.info(messages.wait_for_cert(certname))
        asyncio.ensure_future(self._certname_stopwatch(certname))

    def check_and_remove(self, certname):
        has_certname = certname in self.certlist
        self.remove(certname)
        if has_certname:
            logging.info(messages.cert_is_known(certname))
        else:
            logging.warning(messages.cert_is_unknown(certname))
        return has_certname

    def __contains__(self, certname):
        return certname in self.certlist
