#!/usr/bin/env bash

./scripts/install_puppet.sh

echo 'Installing polypuppet module'
/opt/puppetlabs/bin/puppet module install llday-polypuppet >/dev/null

echo 'Setup server:'
/opt/puppetlabs/bin/puppet apply -e 'class { "polypuppet::setup::server": }'
/opt/puppetlabs/bin/puppetserver ca setup >/dev/null

echo 'Deploing environment'
r10k deploy environment -pv >/dev/null

echo 'Setup polypuppet server'
polypuppet setup server

echo 'Server is ready'
