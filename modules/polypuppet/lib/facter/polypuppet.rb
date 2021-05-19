Facter.add('polypuppet') do
  confine {Facter::Core::Execution.which('polypuppet')}
  setcode do
    configs = Facter::Core::Execution.execute('polypuppet config')

    result = {}
    configs.each_line do |line|
      key, value = line.split('=')

      if value.nil?
        value = ''
      end

      result[key] = value.strip()
    end

    result
  end

end
