class profile::vm {

  $names = lookup('virtual_machines', Variant[Array[String], Undef], 'unique', undef)

  if ! str2bool($::is_virtual) and $names != undef {

    package { 'vagrant':
      ensure   => installed,
      provider => $::polypuppet::defs::provider,
    }

    package { 'virtualbox':
      ensure   => installed,
      provider => $::polypuppet::defs::provider,
    }

    $polypuppet_confdir = $::polypuppet::defs::polypuppet_confdir
    $vagrantfile = "${polypuppet_confdir}/Vagrantfile"

    file { $vagrantfile:
      ensure => present,
      source => 'puppet:///modules/polypuppet/Vagrantfile',
    }

    $names.each |String $vm| {

      exec { "vagrant up ${vm}":
        cwd     => $polypuppet_confdir,
        path    => $::path,
        unless  => "polypuppet test vm ${vm}",
        timeout => 0,
      }

      ~> exec { "vagrant halt ${vm}":
        cwd         => $polypuppet_confdir,
        refreshonly => true,
        path        => $::path,
      }

    }
  }
}
