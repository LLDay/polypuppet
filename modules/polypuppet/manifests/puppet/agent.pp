class polypuppet::puppet::agent (
  $autostart     = $polypuppet::agent_autostart,
  $confdir       = $polypuppet::puppet_confdir,
  $server_domain = $polypuppet::puppet_server_domain,
) {

  $codedir = "${confdir}/code"

  if ($autostart) {
    $runmode = 'server'
  } else {
    $runmode = 'none'
  }

  class { '::puppet':
    server       => false,
    runmode      => $runmode,
    codedir      => $codedir,
    puppetmaster => $server_domain,
  }

}
