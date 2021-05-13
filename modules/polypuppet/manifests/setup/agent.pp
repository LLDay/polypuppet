class polypuppet::setup::agent {
  Enum['cron', 'service', 'systemd.timer', 'none', 'unmanaged'] $runmode
) {

  class { '::puppet':
    server  => false,
    runmode => $runmode,
  }

  class { '::python':
    version => 'system',
    pip     => 'present',
  }

  if not defined('::polypuppet::setup') {
    class { 'polypuppet::setup':
      polypuppet_type => 'agent'
    }
  }

}
