class polypuppet::setup::server(
  Stdlib::HTTPUrl $repository,
  Boolean $enable_foreman,
  String $server_jvm_min_heap_size,
  String $server_jvm_max_heap_size,
) {

  class { '::puppet':
    server                   => true,
    server_foreman           => true,
    server_ca_allow_sans     => true,
    server_jvm_min_heap_size => $server_jvm_min_heap_size,
    server_jvm_max_heap_size => $server_jvm_max_heap_size,
    autosign                 => '/usr/local/bin/polypuppet-config',
  }

  if $enable_foreman {

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

    #-> package { 'foreman-installer':
      #ensure => installed,
    #}

    #~> exec { 'setup foreman':
      #command     => 'foreman-installer --skip-puppet-version-check --no-enable-foreman -l INFO',
      #user        => 'root',
      #path        => '/usr/bin:/local/usr/bin:/usr/sbin',
      #logoutput   => 'on_failure',
      #refreshonly => true,
      #timeout     => 0,
    #}

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

  if !defined(Class['polypuppet::setup']) {
    class { 'polypuppet::setup':
      polypuppet_type => 'server'
    }
  }

}
