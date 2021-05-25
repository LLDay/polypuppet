class polypuppet (
  Enum['agent', 'server'] $puppet_role,

  Integer $polypuppet_cert_waittime,
  Integer $polypuppet_control_port,
  Integer $polypuppet_server_port,

  Variant[Integer, Undef] $audience = undef,
  Variant[String, Undef]  $token = undef,

  Boolean $enable_foreman,
  Stdlib::HTTPUrl $repository,
  String $puppet_server_domain,

  Boolean $agent_autostart,

  String $server_jvm_min_heap_size,
  String $server_jvm_max_heap_size,
) {

  include polypuppet::facter
  contain polypuppet::install
  contain polypuppet::config::ini
  contain polypuppet::puppet::setup
  contain polypuppet::config::role

}
