class polypuppet::defs {

  if $::operatingsystem == 'windows' {
    $provider = 'chocolatey'
    $facter_dir = 'C:\ProgramData\PuppetLabs\facter\etc'
    $facter_path = 'C:\ProgramData\PuppetLabs\facter\etc\facter.conf'
    $polypuppet_confdir = 'C:\ProgramData\Polypuppet'
  } else {
    $provider = undef
    $facter_dir = '/etc/puppetlabs/facter'
    $facter_path = '/etc/puppetlabs/facter/facter.conf'
    $polypuppet_confdir = '/etc/polypuppet'
  }

}