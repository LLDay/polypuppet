#!/usr/bin/env bash

PRIMARY_SERVER_DOMAIN=$(polypuppet config primary_server_domain)

if which apt-get; then
    ./scripts/import_puppet.sh
    apt-get -y install puppet-agent
fi

/opt/puppetlabs/bin/puppet config set --section agent server "$PRIMARY_SERVER_DOMAIN"
