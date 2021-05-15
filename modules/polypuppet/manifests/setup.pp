class polypuppet::setup {

  class { '::python':
    ensure => 'present',
    pip    => 'present',
  }

  package { 'polypuppet':
    ensure   => installed,
    provider => 'pip3',
  }

}
