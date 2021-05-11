class polypuppet::setup::agent {

  class { '::python':
    version => 'system',
    pip     => 'present',
  }

  if not defined('::polypuppet::setup') {
    class { 'polypuppet::setup':
      polypuppet_type => 'agent'
    }
  }

  class { '::puppet':
    server => false,
  }

}
