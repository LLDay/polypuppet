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
            self._run('config set --section', section, which, value)

    def sync(noop=False):
        command = 'agent --test'
        if noop:
            command += ' --noop'
        self._run(command)
