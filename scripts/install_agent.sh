#!/usr/bin/env bash

SERVER_DOMAIN=$(polypuppet config server_domain)

if which apt-get; then
    ./scripts/import_puppet.sh
    apt-get -y install puppet-agent
fi

/opt/puppetlabs/bin/puppet config set --section agent server "$SERVER_DOMAIN"
