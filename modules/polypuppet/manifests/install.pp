class polypuppet::install inherits polypuppet::defs {

  if downcase($::os['name']) == 'windows' {
    include chocolatey

    if (versioncmp($::os['release']['major'], '8') < 0) {
      $python_version = '3.8.10'
    } else {
      $python_version = 'latest'
    }

    package { 'python':
      ensure          => $python_version,
      provider        => $polypuppet::defs::provider,
      install_options => [ '--install-arguments', { 'PrependPath' => '1' } ],
    }

  } else {

    case $::os['name'] {
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
      ensure   => installed,
      provider => $polypuppet::defs::provider,
    }

    package { $pip_package_name:
      ensure   => installed,
      provider => $polypuppet::defs::provider,
    }

  }

  package { 'polypuppet':
    ensure   => installed,
    provider => pip3,
  }

}
