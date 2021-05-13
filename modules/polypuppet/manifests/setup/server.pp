class polypuppet::setup::server(
  Stdlib::HTTPUrl $repository,
  Boolean $enable_foreman,
  String $server_jvm_min_heap_size,
  String $server_jvm_max_heap_size,
) {

  if $enable_foreman {

    class {'::foreman':
      initial_admin_password => 'password',
      rails_cache_store      => {
        type => 'file',
      },
    }

    package { 'foreman-installer':
      ensure => installed,
    }

    ~> exec { 'setup foreman':
      command     => 'foreman-installer --skip-puppet-version-check',
      user        => 'root',
      path        => '/usr/bin:/local/usr/bin:/usr/sbin',
      refreshonly => true,
      timeout     => 0,
    }

  }

  class { '::puppet':
    server                   => true,
    server_foreman           => true,
    server_ca_allow_sans     => true,
    server_jvm_min_heap_size => $server_jvm_min_heap_size,
    server_jvm_max_heap_size => $server_jvm_max_heap_size,
  }

  $deploy_settings = {
    'purge_allowlist' => ['modules/polypuppet'],
  }

  class { '::r10k':
    provider        => 'puppet_gem',
    install_options => empty,
    configfile      => '/etc/puppetlabs/r10k/r10k.yaml',
    deploy_settings => $deploy_settings,
    sources         => {
      'puppet' => {
        'basedir' => $::settings::environmentpath,
        'remote'  => $repository,
        'prefix'  => false,
      }
    }
  }

  class { '::python':
    version => 'system',
    pip     => 'present',
  }

  if !defined('::polypuppet::setup') {
    class { 'polypuppet::setup':
      polypuppet_type => 'server'
    }
  }

}
