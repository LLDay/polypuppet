import getpass
import logging
import sys


class _MessagesEn:
    def _concat(self, *args):
        return ' '.join(str(arg) for arg in args)

    def logged_in(self):
        return 'Logged in successfully'

    def not_logged_in(self):
        return 'Wrong credentials'

    def server_is_on(self, ip, port):
        return self._concat('Server is listening on', ip, 'with port', port)

    def wrong_message_from(self, ip):
        return self._concat('Wrong message from host', ip)

    def wrong_message_from_server(self):
        return self._concat('Wrong message from server')

    def no_config_key(self, key):
        return self._concat('There is no key', key)

    def cannot_change_key(self, key):
        return self._concat('You cannot explicitly change key', key)

    def executable_not_exists(self, executable_name):
        return self._concat('Exetuable does not exist:', executable_name + '.', 'You should install it first')

    def cannot_connect_to_server(self, ip, port):
        return self._concat('Cannot open connection to the server on', ip, 'with port', port)

    def cannot_create_config_file(self):
        return 'Cannot change config file because of low permissions'

    def cannot_create_token_file(self):
        return 'Cannot create token file because of low permissions'

    def cannot_connect_to_cas(self):
        return 'Cannot connect to the CAS'

    def wait_for_cert(self, certname):
        return self._concat('Waiting for CSR from', certname)

    def stop_waiting_for_cert(self, certname):
        return self._concat('Stop waiting for CSR from', certname)

    def cert_is_known(self, certname):
        return self._concat('Puppetserver requested for known certname', certname)

    def cert_is_unknown(self, certname):
        return self._concat('Puppetserver requested for unknown certname', certname + '.', "It won't be signed")

    def server_generated_token(token):
        return self._concat('Server has generated token', token)

    def server_stopped(self):
        return 'Server stopped successfully'

    def must_call_setup_server(self):
        return 'You must call "polypuppet setup server" first'

    def cannot_request_token(self):
        return 'Cannot request token. No server runs on local machine'

    def token_not_generated(self):
        return "Token has not been generated. Call 'polypuppet token --new' first"

    def cannot_generate_certificate(self):
        return 'Server cannot generate certificate'

    def trying_to_regenerate_certificate(self):
        return 'Server cannot generate certificate. Trying to clean the certificate and generate again'

    def certificate_is_not_presented(self):
        return 'Server cannot find certificate. Generating a new one'

    def server_sends(self, message):
        return 'Server sends:\n' + str(message)

    def server_receives(self, message):
        return 'Server receives:\n' + str(message)

    def agent_sends(self, message):
        return 'Agent sends:\n' + str(message)

    def agent_receives(self, message):
        return 'Agent receives:\n' + str(message)


messages = _MessagesEn()
