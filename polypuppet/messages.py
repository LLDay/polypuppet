import getpass


class _InfoEn:
    def username(self):
        return input('Username: ')

    def password(self):
        return getpass.getpass('Password: ')

    def logged_in(self):
        print('Logged in successfully')

    def not_logged_in(self):
        print('Wrong credentials')

    def no_config_key(self, key):
        print('There is no key', key)

    def puppet_exec_no_exit(self, executable_name):
        print('Exetuable does not exist:', executable_name)
        print('You should install it first')

    def agent_cannot_connect_server(self, ip, port):
        print('Cannot open connection to the server on', ip, 'with port', port)

    def cannot_create_config_file(self):
        print('Cannot change config file because of low permissions')

    def cannot_connect_to_cas(self):
        print('Cannot connect to the CAS')

    def server_cannot_bind(self, ip, port, why):
        print('Server cannot bind', ip, 'with port', port)
        print(why)


class _Error(_InfoEn):
    def __getattribute__(self, attr):
        function = getattr(_InfoEn(), attr)

        def run_and_exit(*args, **kwargs):
            function(*args, **kwargs)
            exit(1)
        return run_and_exit


info = _InfoEn()
error = _Error()
