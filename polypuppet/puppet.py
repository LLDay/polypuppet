import subprocess


class Puppet:
    def _run(self, *args):
        full_command = 'puppet ' + ' '.join(args)
        print(full_command)
        run = subprocess.run(full_command.split(), text=True)
        return run.stdout

    def config(self, which, value=None, rm=False, section='agent'):
        if rm:
            self._run('config delete --section', section, which)
        elif value is None:
            print(self._run('config print --section', section, which))
        else:
            self._run('config set', which, value, '--section', section)

    def sync(self, noop=False):
        command = ['agent --test']
        if noop:
            command.append('--noop')
        return self._run(*command)

    def service(self, service_name, ensure=True, enable=None):
        if enable is None:
            enable = ensure

        ensure = 'running' if ensure else 'stopped'
        enable = 'true' if enable else 'false'

        command = ['resource service']
        command.append(service_name)
        command.append('ensure=' + ensure)
        command.append('enable=' + enable)
        self._run(*command)
