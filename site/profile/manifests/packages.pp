class profile::packages (
  Array[Variant[Hash, String]] $install   = [],
  Array[Variant[Hash, String]] $uninstall = [],
  Hash $default_install_params = {},
  Hash $default_uninstall_params = {},
) {

  $install.each |$package| {
    if $package =~ Hash {
        $package.map |$name, $hash| {
          $merged_hash = merge($default_install_params, $hash)
          package { $name:
            ensure          => installed,
            provider        => $merged_hash['provider'],
            install_options => $merged_hash['options'],
        }
      }
    } else {
      package { $package:
        ensure          => installed,
        provider        => $default_install_params['provider'],
        install_options => $default_install_params['options']
      }
    }
  }

  $uninstall.each |$package| {
    if $package =~ Hash {
      $package.map |$name, $hash| {
        $merged_hash = merge($default_uninstall_params, $hash)

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

      if $default_uninstall_params['purge'] {
        $action = 'purged'
      } else {
        $action = 'absent'
      }

      package { $package:
        ensure            => $action,
        provider          => $default_uninstall_params['provider'],
        uninstall_options => $default_uninstall_params['options'],
      }
    }
  }
}
