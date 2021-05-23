class polypuppet::facter inherits polypuppet::defs {

  file { $polypuppet::defs::facter_dir:
    ensure => directory,
  }

  -> file { $polypuppet::defs::facter_path:
    ensure => present,
    source => 'puppet:///modules/polypuppet/facter.conf',
  }

}
