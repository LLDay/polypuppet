class polypuppet::install {

  if $::operatingsystem == 'windows' {
    include chocolatey

    if (versioncmp($facts['os']['release']['major'], '8') < 0) {
      $python_version = '3.8.10'
    } else {
      $python_version = 'latest'
    }

    package { 'python':
      ensure          => $python_version,
      provider        => 'chocolatey',
      install_options => [ '--install-arguments', { 'PrependPath' => '1' } ],
    }

  } else {

    case $::facts['os']['name'] {
      'ArchLinux': {
        $python_package_name = 'python'
        $pip_package_name = 'python-pip'
      }

      default: {
        $python_package_name = 'python3'
        $pip_package_name = 'python3-pip'
      }
    }

    package { $python_package_name:
      ensure =>  installed,
    }

    package { $pip_package_name:
      ensure => installed,
    }

    -> package { 'polypuppet':
      ensure   => installed,
      provider => pip3,
    }

  }

}
