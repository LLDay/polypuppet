class profile::vm (
  Variant[Array[String], Undef] $names = undef,
) {

  if ! str2bool($::is_virtual) {

    package { 'vagrant':
      ensure   => installed,
      provider => $::polypuppet::defs::provider,
    }

    package { 'virtualbox':
      ensure   => installed,
      provider => $::polypuppet::defs::provider,
    }

    $polypuppet_config_dir = $::facts['polypuppet']['confdir']
    $vagrantfile = "${polypuppet_config_dir}/Vagrantfile"

    file { $vagrantfile:
      ensure => present,
      source => 'puppet:///modules/polypuppet/Vagrantfile',
    }

    if $names != undef {
      $names.each |String $vm| {

        exec { "vagrant up ${vm}":
          cwd  => $polypuppet_config_dir,
          path => $::path,
        }

        ~> exec { "vagrant halt ${vm}":
          cwd         => $polypuppet_config_dir,
          refreshonly => true,
          path        => $::path,
        }

      }
    }
  }
}
