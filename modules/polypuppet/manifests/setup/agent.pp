class polypuppet::setup::agent (
  Enum['cron', 'service', 'systemd.timer', 'none', 'unmanaged'] $runmode,
) {

  class { '::puppet':
    server  => false,
    runmode => $runmode,
  }

  include 'polypuppet::setup'

}
