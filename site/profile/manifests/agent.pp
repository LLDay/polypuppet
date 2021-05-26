class profile::agent {
  if !defined(Class['::polypuppet']) {
    class { '::polypuppet':
      puppet_role => 'agent',
    }
  }
}
