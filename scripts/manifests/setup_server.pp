class { 'python':
  version => 'system',
  pip     => 'present',
}

$deploy_settings = {
  'purge_allowlist' => ['modules/polypuppet'],
}

class { 'r10k':
  provider        => 'puppet_gem',
  install_options => empty,
  configfile      => '/etc/puppetlabs/r10k/r10k.yaml',
  deploy_settings => $deploy_settings,
  sources         => {
    'puppet' => {
      'basedir' => $::settings::environmentpath,
      'remote'  => 'https://github.com/LLDay/polypuppet',
      'prefix'  => false,
    }
  }
}

hocon_setting { 'ca.conf allow-subject-alt-names':
  ensure  => present,
  path    => '/etc/puppetlabs/puppetserver/conf.d/ca.conf',
  setting => 'certificate-authority.allow-subject-alt-names',
  value   => true,
  type    => 'boolean',
}
