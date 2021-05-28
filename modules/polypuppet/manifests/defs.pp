class polypuppet::defs {

  if downcase($::os['name']) == 'windows' {
    $codedir = 'C:\ProgramData\PuppetLabs\code'
    $facter_dir = 'C:\ProgramData\PuppetLabs\facter\etc'
    $facter_path = 'C:\ProgramData\PuppetLabs\facter\etc\facter.conf'
    $polypuppet_confdir = 'C:\ProgramData\Polypuppet'
    $provider = 'chocolatey'
  } else {
    $codedir = '/etc/puppetlabs/code'
    $facter_dir = '/etc/puppetlabs/facter'
    $facter_path = '/etc/puppetlabs/facter/facter.conf'
    $polypuppet_confdir = '/etc/polypuppet'
    $provider = undef
  }

}
