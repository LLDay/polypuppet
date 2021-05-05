class polypuppet::setup (
  Enum['server', 'agent'] $polypuppet_type = $polypuppet::params::polypuppet_type
) {

  package { 'polypuppet':
    ensure   => installed,
    provider => 'pip3',
  }

  exec { "polypuppet setup ${polypuppet_type}":
    path        => '/bin:/usr/bin/:/usr/local/bin',
    refreshonly => true,
    subscribe   => Package['polypuppet'],
    user        => 'root',
  }

}
