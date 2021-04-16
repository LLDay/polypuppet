#
# Interfaces of the daemon
#

class DaemonApi:
    def stop_daemon(self):
        pass

    def autoconf(self, certname):
        pass


class ServerApi:
    def login(self, username, password):
        pass
