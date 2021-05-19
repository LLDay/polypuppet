#!/usr/bin/env bash

./scripts/install_puppet.sh

echo 'Installing polypuppet module'
/opt/puppetlabs/bin/puppet module install llday-polypuppet >/dev/null

echo 'Setup server:'
/opt/puppetlabs/bin/puppet apply -e 'class { "polypuppet": puppet_role => "server" }'

echo 'Deploing environment'
#r10k deploy environment -pv >/dev/null

echo 'Server is ready'
