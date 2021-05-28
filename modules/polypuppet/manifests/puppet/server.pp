class polypuppet::puppet::server(
  $repository = $polypuppet::repository,
  $enable_foreman = $polypuppet::enable_foreman,
  $server_jvm_min_heap_size = $polypuppet::server_jvm_min_heap_size,
  $server_jvm_max_heap_size = $polypuppet::server_jvm_max_heap_size,
) {

  if $enable_foreman {

    class { '::puppet':
      autosign                   => '/usr/local/bin/polypuppet-autosign',
      autosign_mode              => '755',
      client_certname            => $polypuppet::puppet_server_domain,
      codedir                    => $polypuppet::defs::codedir,
      environment                => $polypuppet::environment,
      server                     => true,
      server_ca_allow_sans       => true,
      server_certname            => $polypuppet::puppet_server_domain,
      server_common_modules_path => '',
      server_foreman             => true,
      server_jvm_max_heap_size   => $server_jvm_max_heap_size,
      server_jvm_min_heap_size   => $server_jvm_min_heap_size,
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
      autosign                   => '/usr/local/bin/polypuppet-autosign',
      autosign_mode              => '755',
      client_certname            => $polypuppet::puppet_server_domain,
      codedir                    => $polypuppet::defs::codedir,
      environment                => $polypuppet::environment,
      report                     => false,
      server                     => true,
      server_ca_allow_sans       => true,
      server_certname            => $polypuppet::puppet_server_domain,
      server_common_modules_path => '',
      server_external_nodes      => '',
      server_foreman             => false,
      server_jvm_max_heap_size   => $server_jvm_max_heap_size,
      server_jvm_min_heap_size   => $server_jvm_min_heap_size,
      server_reports             => '',
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

  $github_token = lookup('github_api_token', Variant[String, Undef], 'first', undef)

  if $github_token != undef {

    class {'r10k::webhook::config':
      use_mcollective => false,
    }

    -> class {'r10k::webhook':
      use_mcollective => false,
      user            => 'root',
      group           => '0',
    }

    git_webhook { 'web_post_receive_webhook' :
      ensure             => present,
      webhook_url        => "https://${polypuppet::server_domain}:8088/payload",
      token              =>  $github_token,
      project_name       => 'organization/control',
      server_url         => 'https://api.github.com',
      disable_ssl_verify => true,
      provider           => 'github',
    }

  }

  package { 'hiera-eyaml':
    ensure   => installed,
    provider => gem,
  }

  exec { 'eyaml createkeys':
    command => 'eyaml createkeys --pkcs7-private-key=/etc/puppetlabs/puppet/keys/private_key.pkcs7.pem\
                                 --pkcs7-public-key=/etc/puppetlabs/puppet/keys/public_key.pkcs7.pem',
    creates => '/etc/puppetlabs/puppet/keys/private_key.pkcs7.pem',
    path    => $::path,
  }

  $service_path = '/etc/systemd/system/polypuppet.service'

  file { $service_path:
    source => 'puppet:///modules/polypuppet/polypuppet.service',
  }

  service { 'polypuppet':
    ensure    => running,
    enable    => true,
    hasstatus => true,
    require   => Class['::puppet'],
  }

  File[$service_path] ~> Service['polypuppet']
  Package['polypuppet'] ~> Service['polypuppet']
}
