class polypuppet::config::ini (
  $cert_waittime = $polypuppet::polypuppet_cert_waittime,
  $control_port  = $polypuppet::polypuppet_control_port,
  $server_domain = $polypuppet::puppet_server_domain,
  $server_port   = $polypuppet::polypuppet_server_port,
) inherits polypuppet::defs {

  $ini_content = {
    'server'  => {
      'server_domain' => $server_domain,
      'server_port'   => $server_port,
    },
    'agent'   => {
      'cert_waittime' => $cert_waittime,
      'control_port'  => $control_port,
    },
  }

  $confdir = $polypuppet::defs::polypuppet_confdir
  $polypuppet_config_name = 'config.ini'
  $polypuppet_config_path = "${confdir}/${polypuppet_config_name}"

  file { $confdir:
    ensure => directory,
  }

  file { $polypuppet_config_path:
    ensure  => file,
    require => File[$confdir],
  }

  $ini_path = { 'path' => $polypuppet_config_path }
  ::inifile::create_ini_settings($ini_content, $ini_path)

}
