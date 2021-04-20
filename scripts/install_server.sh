#!/usr/bin/env bash

PRIMARY_SERVER_DOMAIN=$(polypuppet config primary_server_domain)
PRIMARY_SERVER_CERTNAME=$(polypuppet config primary_server_certname)
PUPPET_MEMORY_USAGE=$(polypuppet config puppet_memory_usage)

if [ ! -f /opt/puppetlabs/server/bin/puppetserver ]; then
    if which apt-get; then
        ./scripts/import_puppet.sh
        apt-get -y install puppetserver
    elif which yum; then
        CENTOS_VER=$(rpm --eval "%{centos_ver}")
        rpm -Uvh https://yum.puppet.com/$PUPPET_VERSION-el-$CENTOS_VER.noarch.rpm
        yum install -y puppetserver
    fi
fi

/opt/puppetlabs/bin/puppet module install puppet-r10k
/opt/puppetlabs/bin/puppet apply manifests/r10k.pp
r10k deploy environment -pv
