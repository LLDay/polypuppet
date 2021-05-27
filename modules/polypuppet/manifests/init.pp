class polypuppet (
  Enum['agent', 'server'] $puppet_role,

  Variant[String, Undef] $environment = undef,

  Integer $polypuppet_cert_waittime,
  Integer $polypuppet_control_port,
  Integer $polypuppet_server_port,

  Variant[Integer, Undef] $building = undef,
  Variant[Integer, Undef] $audience = undef,
  Variant[String, Undef]  $token = undef,

  Boolean $enable_foreman,
  Stdlib::HTTPUrl $repository,
  String $puppet_server_domain,

  Boolean $agent_autostart,

  String $server_jvm_min_heap_size,
  String $server_jvm_max_heap_size,
) {

  include polypuppet::check
  include polypuppet::facter
  include polypuppet::install
  include polypuppet::config
  include polypuppet::puppet::setup

}
