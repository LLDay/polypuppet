class polypuppet::puppet::agent (
  $autostart     = $polypuppet::agent_autostart,
  $confdir       = $polypuppet::puppet_confdir,
  $server_domain = $polypuppet::puppet_server_domain,
) {

  $codedir = "${confdir}/code"

  if $autostart {
    $runmode = 'server'
  } else {
    $runmode = 'none'
  }

  $audience = $polypuppet::audience

  # This condition equals false when admin explicitly change audience number.
  # It's necessary because '::puppet' class restores previous certname after changing certname by polypuppet.
  if $audience == undef or $audience == Integer($::polypuppet['audience']) {

    class { '::puppet':
      server       => false,
      runmode      => $runmode,
      codedir      => $codedir,
      puppetmaster => $server_domain,
    }

  }

}
