import getpass
import logging
import sys


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

    def help_classroom_number():
        return 'Classroom number'

    def help_server():
        return 'Manages the server'

    def help_server_daemon():
        return 'Run the server as a daemon'

    def help_server_restart():
        return 'Restart the server if it has been ran'

    def help_server_stop():
        return 'Stop the server'

    def help_password():
        return 'Password for CAS SPBSTU'

    def logged_in():
        return 'Logged in successfully'

    def not_logged_in():
        return 'Wrong credentials'

    def server_is_on(ip, port):
        return 'Server is listening to {0} with port {1}'.format(ip, port)

    def server_may_already_runned():
        return 'Cannot bind address. Server may be already runned'

    def no_config_key(key):
        return 'There is no key {0}'.format(key)

    def no_vm_named(vm_name):
        return "Virtual machine with name '{0}' does not exist".format(vm_name)

    def cannot_change_key(key):
        return 'You cannot explicitly change key {0}'.format(key)

    def executable_not_exists(executable_name):
        return "Executable '{0}' does not exist".format(executable_name)

    def cannot_connect_to_server(ip, port):
        return 'Cannot open connection to the server on {0} with port {1}'.format(ip, port)

    def cannot_create_config_file():
        return 'Cannot change config file because of low permissions'

    def cannot_create_token_file():
        return 'Cannot create token file because of low permissions'

    def cannot_create_ca_file():
        return 'Cannot create ca.pem file because of low permissions'

    def cannot_read_ssl():
        return 'Cannot read ssl files because of low permissions'

    def cannot_connect_to_cas():
        return 'Cannot connect to the CAS'

    def unsupported_os():
        return 'Server must be runned on machine with systemd'

    def try_to_update_certificate_from(domain):
        return '''Cannot establish secure connection with server.
        It may happen because of invalid CA. Downloading ca certificate from {0}'''.format(domain)

    def wait_for_cert(certname):
        return 'Waiting for CSR from {0}'.format(certname)

    def stop_waiting_for_cert(certname):
        return 'Stop waiting for CSR from {0}'.format(certname)

    def cert_is_known(certname):
        return 'Puppetserver requested for known certname {0}'.format(certname)

    def cert_is_unknown(certname):
        return "Puppetserver requested for unknown certname {0}. It won't be signed".format(certname)

    def server_stopped():
        return 'Server stopped successfully'

    def cannot_request_token():
        return 'Cannot request token. No server runs on local machine'

    def token_not_generated():
        return "Token has not been generated. Call 'polypuppet token new' or 'polypuppet token set' first"

    def cannot_generate_certificate():
        return 'Server cannot generate certificate'

    def agent_login_error():
        return 'Agent cannot setup puppet for work with server'

    def server_sends(message):
        return 'Server sends:\n' + str(message)

    def server_receives(message):
        return 'Server receives:\n' + str(message)

    def agent_sends(message):
        return 'Agent sends:\n' + str(message)

    def agent_receives(message):
        return 'Agent receives:\n' + str(message)


Messages = _MessagesEn
