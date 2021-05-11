#!/usr/bin/env bash

./scripts/install_puppet.sh

echo 'Installing module polypuppet'
/opt/puppetlabs/bin/puppet module install llday-polypuppet >/dev/null

echo 'Setup agent:'
/opt/puppetlabs/bin/puppet apply -e 'class { "polypuppet::setup::server": }'
/opt/puppetlabs/bin/puppetserver ca setup >/dev/null

echo 'Deploing environment'
r10k deploy environment -pv >/dev/null

echo 'Server is ready'
