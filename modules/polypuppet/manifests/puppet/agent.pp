class polypuppet::puppet::agent (
  $autostart     = $polypuppet::agent_autostart,
  $server_domain = $polypuppet::puppet_server_domain,
) {

  if $autostart {
    $runmode = 'server'
  } else {
    $runmode = 'none'
  }

  $building = $polypuppet::building
  $audience = $polypuppet::audience

  if $audience == undef {
    $allow_puppet = true
  } elsif ! has_key($::facts, 'polypuppet') {
    $allow_puppet = true
  } elsif $::polypuppet['audience'] == '' or $::polypuppet['building'] == '' {
    $allow_puppet = true
  } elsif $audience == Integer($::polypuppet['audience']) and $building == Integer($::polypuppet['building']) {
    $allow_puppet = true
  } else {
    $allow_puppet = false
  }

  # This condition equals false when admin explicitly change audience number.
  # It's necessary because '::puppet' class restores previous certname after changing certname by polypuppet.
  if $allow_puppet {

    class { '::puppet':
      environment  => $polypuppet::environment,
      puppetmaster => $server_domain,
      runmode      => $runmode,
      server       => false,
    }

  }

}
