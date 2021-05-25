class polypuppet::config (
  $cert_waittime = $polypuppet::polypuppet_cert_waittime,
  $control_port  = $polypuppet::polypuppet_control_port,
  $server_domain = $polypuppet::puppet_server_domain,
  $server_port   = $polypuppet::polypuppet_server_port,
) inherits polypuppet::defs {

  include polypuppet::config::role

  if $cert_waittime != undef {
    polypuppet::config::set { 'cert_waittime':
      value => $cert_waittime
    }
  }

  if $control_port != undef {
    polypuppet::config::set { 'control_port':
      value => $control_port
    }
  }

  if $server_domain != undef {
    polypuppet::config::set { 'server_domain':
      value => $server_domain
    }
  }

  if $server_port != undef {
    polypuppet::config::set { 'server_port':
      value => $server_port
    }
  }

}
