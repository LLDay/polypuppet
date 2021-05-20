#!/usr/bin/env bash

./scripts/install_puppet.sh

PUPPET_PATH=$(which puppet)
if [ -z $PUPPET_PATH ]; then
    POSSIBLE_PATH="/opt/puppetlabs/bin/puppet"
    if [ -f "$POSSIBLE_PATH" ]; then
        PUPPET_PATH="$POSSIBLE_PATH"
    else
        echo 'Cannot find puppet executable'
        exit 1
    fi
fi

echo 'Installing polypuppet module'
$PUPPET_PATH module install llday-polypuppet >/dev/null

echo 'Setup agent:'
$PUPPET_PATH apply -e 'class { "polypuppet": puppet_role => "agent", }'

echo 'Agent is ready'
