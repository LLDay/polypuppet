$choco_exists = choco -v

if (-not($choco_exists)) {
    echo 'Installing chocolatey'
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
    Set-ExecutionPolicy Default -Scope Process -Force
}

$puppet_agent_exists = choco list -lo | Where-object { $_.ToLower().StartsWith("puppet-agent") }

if (-not($puppet_agent_exists)) {
    echo 'Installing puppet-agent'
    choco install -y puppet-agent --no-progress
}

echo 'Installing polypuppet module'
$result = (Start-Process -FilePath "C:\Program Files\Puppet Labs\Puppet\bin\puppet.bat" -ArgumentList "module install llday-polypuppet" -Wait -Passthru).ExitCode

if ($result -ne 0) {
    echo "Some errors occure during module installation"
}

echo 'Configuring puppet'
$result = (Start-Process -FilePath "C:\Program Files\Puppet Labs\Puppet\bin\puppet.bat" -ArgumentList "apply -e 'class { `"polypuppet`": puppet_role => `"agent`", '}" -Wait -Passthru).ExitCode

if ($result -eq 0) {
    echo 'Puppet-agent is configured'
} else {
    echo 'Some errors happen during configuration'
}
