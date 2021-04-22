Facter.add('polypuppet') do
  setcode do
    Facter::Core::Execution.execute('polypuppet config')
  end
end
