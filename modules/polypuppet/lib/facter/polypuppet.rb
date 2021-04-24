require('facter')

Facter.add('polypuppet') do
  confine {Facter::Core::Execution.which('polypuppet')}
  setcode do
    Facter::Core::Execution.execute('polypuppet config')
  end
end
