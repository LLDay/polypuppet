class polypuppet::puppet::agent (
  $autostart     = $polypuppet::agent_autostart,
  $server_domain = $polypuppet::puppet_server_domain,
) {

  if $autostart {
    $runmode = 'service'
  } else {
    $runmode = 'none'
  }

  $building  = $polypuppet::building
  $classroom = $polypuppet::classroom

  if $classroom == undef {
    $allow_puppet = true
  } elsif ! has_key($::facts, 'polypuppet') {
    $allow_puppet = true
  } elsif $::polypuppet['role'] != 'classroom' {
    $allow_puppet = true
  } elsif $::polypuppet['classroom'] == '' or $::polypuppet['building'] == '' {
    $allow_puppet = true
  } elsif $classroom == Integer($::polypuppet['classroom']) and $building == Integer($::polypuppet['building']) {
    $allow_puppet = true
  } else {
    $allow_puppet = false
  }

  # This condition equals false when admin explicitly change classroom number.
  # It's necessary because '::puppet' class restores previous certname after changing certname by polypuppet.
  if $allow_puppet {

    class { '::puppet':
      codedir      => $polypuppet::defs::codedir,
      environment  => $polypuppet::environment,
      puppetmaster => $server_domain,
      runinterval  => '1h',
      runmode      => $runmode,
      server       => false,
      splay        => true,
      splaylimit   => '20m',
    }

  }

}
