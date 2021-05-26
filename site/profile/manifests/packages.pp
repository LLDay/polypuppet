class profile::packages {

  $install = lookup('install', Tuple, 'unique', [])
  $uninstall = lookup('uninstall', Tuple, 'unique', [])
  $install_defaults = lookup('install_defaults', Hash, 'hash', {})
  $uninstall_defaults = lookup('uninstall_defaults', Hash, 'hash', {})

  $default_puppet_params = {
    'provider' => $::polypuppet::defs::provider,
  }

  $install_params = merge($default_puppet_params, $install_defaults)
  $uninstall_params = merge($default_puppet_params, $uninstall_defaults)

  $install.each |$package| {
    if $package =~ Hash {
      $package.map |$name, $hash| {
        $merged_hash = merge($install_params, $hash)
        package { $name:
          ensure          => installed,
          provider        => $merged_hash['provider'],
          install_options => $merged_hash['options'],
        }
      }
    } else {
      package { $package:
        ensure          => installed,
        provider        => $install_params['provider'],
        install_options => $install_params['options']
      }
    }
  }

  $uninstall.each |$package| {
    if $package =~ Hash {
      $package.map |$name, $hash| {
        $merged_hash = merge($uninstall_params, $hash)

        if $merged_hash['purge'] {
          $action = 'purged'
        } else {
          $action = 'absent'
        }

        package { $name:
          ensure            => $action,
          provider          => $merged_hash['provider'],
          uninstall_options => $merged_hash['options'],
        }
      }
    } else {

      if $uninstall_params['purge'] {
        $action = 'purged'
      } else {
        $action = 'absent'
      }

      package { $package:
        ensure            => $action,
        provider          => $uninstall_params['provider'],
        uninstall_options => $uninstall_params['options'],
      }
    }
  }
}
