class polypuppet (
  Integer $cert_waittime,
  Integer $control_port,
  Integer $server_port,
  String  $confdir,
  String  $server_domain,

  Variant[Integer, Undef] $audience = undef,
  Variant[String, Undef]  $token    = undef,
) {
  $polypuppet_config_name = 'polypuppet.ini'
  $polypuppet_config_path = "${$confdir}/${polypuppet_config_name}"

  exec { 'create config file':
    command => "mkdir -p ${confdir} && touch ${polypuppet_config_path}",
    creates => $polypuppet_config_path,
    path    => '/usr/bin:/usr/local/bin:/usr/sbin:/bin',
    user    => 'root',
  }

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

  $ini_path = { 'path' => $polypuppet_config_path }
  ::inifile::create_ini_settings($ini_content, $ini_path)

  if $audience != undef and $token != undef {
    $hidden_command = Sensitive("polypuppet audience ${audience} ${token}")
    exec { 'setup audience number':
      command => $hidden_command,
      path    => '/usr/bin:/usr/local/bin:/usr/sbin:/bin',
      user    => 'root',
      unless  => "polypuppet has audience ${audience}"
    }
  }
}
