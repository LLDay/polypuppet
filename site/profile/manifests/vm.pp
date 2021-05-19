class profile::vm (
  Array[String] $vagrant_names,
) {

  package { 'vagrant':
    ensure => installed,
  }

  package { 'virtualbox':
    ensure => installed,
  }

  $polypuppet_config_dir = $::facts['polypuppet']['confdir']
  $vagrantfile = "${polypuppet_config_dir}/Vagrantfile"
  $vms = join($vagrant_names, ' ')

  file { $vagrantfile:
    ensure => present,
    source => 'puppet:///modules/polypuppet/Vagrantfile',
  }

  exec { "vagrant up ${vms}":
    cwd       => $polypuppet_config_dir,
    subscribe => File[$vagrantfile],
    path      => '/usr/bin:/usr/local/bin',
  }

  ~> exec { "vagrant halt ${vms}":
    cwd         => $polypuppet_config_dir,
    path        => '/usr/bin:/usr/local/bin',
    refreshonly => true,
  }

}
