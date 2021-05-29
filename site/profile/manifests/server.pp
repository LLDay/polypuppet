class profile::server {
  if !defined(Class['::polypuppet']) {
    class { '::polypuppet':
      puppet_role => 'server',
    }
  }
}
