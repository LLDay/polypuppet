#!/usr/bin/env bash

BASEDIR=$(dirname $0)
source "$BASEDIR/../polypuppet.env"

if which apt-get; then
    apt-get update
    apt-get -y install puppet
fi

puppet config set --section agent server "$PRIMARY_SERVER_DOMAIN"
puppet resource service puppet ensure=running enable=true
puppet module install puppet-python
puppet apply /vagrant/manifests/agent.pp
