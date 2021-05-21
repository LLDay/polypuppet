import getpass
import logging
import sys


def _concat(*args):
    return ' '.join(str(arg) for arg in args)


class _MessagesEn:

    def help_verbose():
        return 'Provide more output'

    def help_quiet():
        return 'Supress output'

    def help_certname():
        return ''

    def help_username():
        return 'Username from CAS SPBSTU'

    def help_token():
        return "Secret server's token"

    def help_audience_number():
        return 'Audience number'

    def help_server():
        return 'Manages the server'

    def help_server_daemon():
        return 'Run the server as a daemon'

    def help_server_restart():
        return 'Restart the server if it has been ran'

    def help_server_clean():
        return "Clean server's certificate"

    def help_server_stop():
        return 'Stop the server'

    def help_password():
        return 'Password for CAS SPBSTU'

    def logged_in():
        return 'Logged in successfully'

    def not_logged_in():
        return 'Wrong credentials'

    def server_is_on(ip, port):
        return _concat('Server is listening to', ip, 'with port', port)

    def server_already_runned():
        return 'Server is already runned'

    def no_config_key(key):
        return _concat('There is no key', key)

    def cannot_change_key(key):
        return _concat('You cannot explicitly change key', key)

    def executable_not_exists(executable_name):
        return _concat('Exetuable does not exist:', executable_name + '.', 'You should install it first')

    def cannot_connect_to_server(ip, port):
        return _concat('Cannot open connection to the server on', ip, 'with port', port)

    def cannot_create_config_file():
        return 'Cannot change config file because of low permissions'

    def cannot_create_token_file():
        return 'Cannot create token file because of low permissions'

    def cannot_connect_to_cas():
        return 'Cannot connect to the CAS'

    def wait_for_cert(certname):
        return _concat('Waiting for CSR from', certname)

    def stop_waiting_for_cert(certname):
        return _concat('Stop waiting for CSR from', certname)

    def cert_is_known(certname):
        return _concat('Puppetserver requested for known certname', certname)

    def cert_is_unknown(certname):
        return _concat('Puppetserver requested for unknown certname', certname + '.', "It won't be signed")

    def server_generated_token(token):
        return _concat('Server has generated token', token)

    def server_stopped():
        return 'Server stopped successfully'

    def cannot_request_token():
        return 'Cannot request token. No server runs on local machine'

    def token_not_generated():
        return "Token has not been generated. Call 'polypuppet token --new' first"

    def cannot_generate_certificate():
        return 'Server cannot generate certificate'

    def server_sends(message):
        return 'Server sends:\n' + str(message)

    def server_receives(message):
        return 'Server receives:\n' + str(message)

    def agent_sends(message):
        return 'Agent sends:\n' + str(message)

    def agent_receives(message):
        return 'Agent receives:\n' + str(message)


Messages = _MessagesEn
