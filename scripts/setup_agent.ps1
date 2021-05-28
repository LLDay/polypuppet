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
try {
    iex 'C:\Program` Files\Puppet` Labs\Puppet\bin\puppet.bat module install llday-polypuppet'
} catch {
    echo "Some errors occure during module installation"
}

echo 'Configuring puppet'
try {
    iex 'C:\Program` Files\Puppet` Labs\Puppet\bin\puppet.bat apply -e "class { `"polypuppet`": puppet_role => `"agent`", }"'
    echo 'Puppet-agent is configured'
} catch {
    echo 'Some errors happen during configuration'
}
