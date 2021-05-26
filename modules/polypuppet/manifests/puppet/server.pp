class polypuppet::puppet::server(
  $repository = $polypuppet::repository,
  $enable_foreman = $polypuppet::enable_foreman,
  $server_jvm_min_heap_size = $polypuppet::server_jvm_min_heap_size,
  $server_jvm_max_heap_size = $polypuppet::server_jvm_max_heap_size,
) {

  if $enable_foreman {

    class { '::puppet':
      autosign                 => '/usr/local/bin/polypuppet-autosign',
      autosign_mode            => '755',
      environment              => $polypuppet::environment,
      server                   => true,
      server_ca_allow_sans     => true,
      server_foreman           => true,
      server_jvm_max_heap_size => $server_jvm_max_heap_size,
      server_jvm_min_heap_size => $server_jvm_min_heap_size,
    }

    class {'::foreman':
      dynflow_manage_services => false,
      initial_admin_username  => 'admin',
      initial_admin_password  => 'password',
      rails_cache_store       => {
        type => 'file',
      },
    }

    class {'::foreman_proxy':
      puppet   => true,
      puppetca => true,
      tftp     => false,
      dhcp     => false,
      dns      => false,
      bmc      => false,
      realm    => false,
    }

  } else {

    class { '::puppet':
      autosign                 => '/usr/local/bin/polypuppet-autosign',
      autosign_mode            => '755',
      environment              => $polypuppet::environment,
      report                   => false,
      server                   => true,
      server_ca_allow_sans     => true,
      server_external_nodes    => '',
      server_foreman           => false,
      server_jvm_max_heap_size => $server_jvm_max_heap_size,
      server_jvm_min_heap_size => $server_jvm_min_heap_size,
      server_reports           => '',
    }

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

  service { 'polypuppet':
    ensure    => running,
    enable    => true,
    hasstatus => true,
  }

  Package['polypuppet'] ~> Service['polypuppet']

}
