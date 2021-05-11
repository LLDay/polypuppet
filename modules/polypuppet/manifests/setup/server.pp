class polypuppet::setup::server(
  Stdlib::HTTPUrl $repository,
  String $server_jvm_min_heap_size,
  String $server_jvm_max_heap_size,
  Enum['cron', 'service', 'systemd.timer', 'none', 'unmanaged'] $runmode
) {

  class { '::python':
    version => 'system',
    pip     => 'present',
  }

  if not defined('::polypuppet::setup') {
    class { 'polypuppet::setup':
      polypuppet_type => 'server'
    }
  }

  $deploy_settings = { 'purge_allowlist' => ['modules/polypuppet'],
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

  hocon_setting { 'ca.conf allow-subject-alt-names':
    ensure  => present,
    path    => '/etc/puppetlabs/puppetserver/conf.d/ca.conf',
    setting => 'certificate-authority.allow-subject-alt-names',
    value   => true,
    type    => 'boolean',
  }

  class {'::foreman':
    initial_admin_password => 'password',
    rails_cache_store      => {
      type => 'file',
    },
  }

  class { '::puppet':
    server                   => true,
    server_foreman           => true,
    server_jvm_min_heap_size => $server_jvm_min_heap_size,
    server_jvm_max_heap_size => $server_jvm_max_heap_size,
    runmode                  => $runmode,
  }

}
