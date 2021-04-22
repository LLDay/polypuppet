class polypuppet (
  $audience        = undef,
  $student_flow    = undef,
  $student_group   = undef,

  $cert_waittime   = $polypuppet::params::cert_waittime,
  $confdir         = $polypuppet::params::confdir,
  $control_port    = $polypuppet::params::control_port,
  $enabled         = $polypuppet::params::enabled,
  $server_certname = $polypuppet::params::server_certname,
  $server_domain   = $polypuppet::params::server_domain,
  $server_port     = $polypuppet::params::control_port,
) inherits polypuppet::params {

  $polypuppet_config_dir = '/etc/polypuppet/'
  $polypuppet_config_name = 'polypuppet.ini'
  $polypuppet_config_path = "${polypuppet_config_dir}${polypuppet_config_name}"

  exec { 'create config file':
    command => "mkdir -p ${polypuppet_config_dir} && touch ${polypuppet_config_path}",
    creates => $polypuppet_config_path,
    path    => '/usr/bin:/usr/local/bin:/usr/sbin:/bin',
    user    => 'root',
  }

  $ini_content = {
    'server'  => {
      'server_domain'   => $server_domain,
      'server_certname' => $server_certname,
      'server_port'     => $server_port,
    },
    'agent'   => {
      'cert_waittime' => $cert_waittime,
      'control_port'  => $control_port,
      'enabled'       => $enabled,
    },
    'profile' => {
      'audience'      => $audience,
      'student_flow'  => $student_flow,
      'student_group' => $student_group,
    },
  }

  $ini_path = { 'path' => $confdir }
  ::inifile::create_ini_settings($ini_content, $ini_path)
}
