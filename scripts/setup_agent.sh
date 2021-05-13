#!/usr/bin/env bash

./scripts/install_puppet.sh

echo 'Installing polypuppet module'
/opt/puppetlabs/bin/puppet module install llday-polypuppet >/dev/null

echo 'Setup agent:'
/opt/puppetlabs/bin/puppet apply -e 'class { "polypuppet::setup::agent": }'

echo 'Setup polypuppet agent'
polypuppet setup agent

echo 'Agent is ready'
