class polypuppet::setup::agent (
  Enum['cron', 'service', 'systemd.timer', 'none', 'unmanaged'] $runmode
) {

  class { '::puppet':
    server  => false,
    runmode => $runmode,
  }

  if !defined(Class['polypuppet::setup']) {
    class { 'polypuppet::setup':
      polypuppet_type => 'agent'
    }
  }

}
