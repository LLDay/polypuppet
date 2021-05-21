import logging
import sched
import time
from threading import Lock

from polypuppet import Config
from polypuppet.messages import Messages


class CertList:
    def __init__(self):
        config = Config()
        self.certlist = set()
        self.timeout = int(config['CERT_WAITTIME'])
        self.scheduler = sched.scheduler(time.monotonic, time.sleep)
        self.lock = Lock()

    def remove(self, certname):
        with self.lock:
            if certname in self.certlist:
                logging.info(Messages.stop_waiting_for_cert(certname))
                self.certlist.remove(certname)
                return True
            return False

    def append(self, certname):
        self.scheduler.run(blocking=False)
        self.certlist.add(certname)
        logging.info(Messages.wait_for_cert(certname))
        self.scheduler.enter(self.timeout, 1, self.remove, [(certname)])

    def check_and_remove(self, certname):
        self.scheduler.run(blocking=False)
        had_certname = self.remove(certname)
        if had_certname:
            logging.info(Messages.cert_is_known(certname))
        else:
            logging.warning(Messages.cert_is_unknown(certname))
        return had_certname

    def __contains__(self, certname):
        self.scheduler.run(blocking=False)
        return certname in self.certlist
