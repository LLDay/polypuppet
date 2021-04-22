class { 'r10k':
  provider        => 'puppet_gem',
  install_options => empty,
  configfile      => '/etc/puppetlabs/r10k/r10k.yaml',
  sources         => {
    'puppet' => {
      'basedir' => "${::settings::environmentpath}",
      'remote'  => 'https://github.com/LLDay/polypuppet',
      'prefix'  => false,
    }
  }
}