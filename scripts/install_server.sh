#!/usr/bin/env bash

SERVER_DOMAIN=$(polypuppet config server_domain)
PUPPET_MEMORY_USAGE=256m

if [ ! -f /opt/puppetlabs/server/bin/puppetserver ]; then
    if which apt-get; then
        ./scripts/import_puppet.sh
        apt-get -y install puppetserver
    elif which yum; then
        CENTOS_VER=$(rpm --eval "%{centos_ver}")
        rpm -Uvh "https://yum.puppet.com/$PUPPET_VERSION-el-$CENTOS_VER.noarch.rpm"
        yum install -y puppetserver
    fi
fi

/opt/puppetlabs/bin/puppet resource package perl ensure=installed
if [ -f /etc/default/puppetserver ]; then
    PUPPET_RUN_CONFIG_PATH=/etc/default/puppetserver
elif [ -f /etc/sysconfig/puppet  ]; then
    PUPPET_RUN_CONFIG_PATH=/etc/sysconfig/puppetserver
fi

perl -pi -e "s#(?<=-Xm[sx])[^ ]+#$PUPPET_MEMORY_USAGE#g" "$PUPPET_RUN_CONFIG_PATH"
/opt/puppetlabs/bin/puppetserver ca setup

/opt/puppetlabs/bin/puppet module install puppet-r10k
/opt/puppetlabs/bin/puppet module install puppetlabs-hocon
/opt/puppetlabs/bin/puppet module install puppet-python
/opt/puppetlabs/bin/puppet apply ./scripts/manifests/setup_server.pp
r10k deploy environment -pv
