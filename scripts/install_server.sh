#!/usr/bin/env bash

BASEDIR=$(dirname $0)
source "$BASEDIR/../polypuppet.env"

if [ ! -f /opt/puppetlabs/server/bin/puppetserver ]; then
    if which apt-get; then
        UBUNTU_VERSION=$(lsb_release -sc)
        FILENAME="$PUPPET_VERSION-$UBUNTU_VERSION.deb"
        apt-get update
        apt-get -y install wget
        wget "https://apt.puppet.com/$FILENAME"
        sudo dpkg -i "$FILENAME"
        rm "$FILENAME"
        apt-get update
        apt-get -y install puppetserver

    elif which yum; then
        CENTOS_VER=$(rpm --eval "%{centos_ver}")
        rpm -Uvh https://yum.puppet.com/$PUPPET_VERSION-el-$CENTOS_VER.noarch.rpm
        yum install -y puppetserver
    fi
fi

/opt/puppetlabs/bin/puppet config set --section main server "$PRIMARY_SERVER_DOMAIN"
/opt/puppetlabs/bin/puppet config set --section main certname "$PRIMARY_SERVER_CERTNAME"
/opt/puppetlabs/bin/puppet resource package perl ensure=installed
/opt/puppetlabs/bin/puppet module install puppetlabs-puppetdb

if [ -f /etc/default/puppetserver ]; then
    PUPPET_RUN_CONFIG_PATH=/etc/default/puppetserver
elif [ -f /etc/sysconfig/puppet  ]; then
    PUPPET_RUN_CONFIG_PATH=/etc/sysconfig/puppetserver
fi

perl -pi -e "s#(?<=-Xm[sx])\d+.#$PUPPET_MEMORY_USAGE#g" "$PUPPET_RUN_CONFIG_PATH"
/opt/puppetlabs/bin/puppet apply /vagrant/manifests/server.pp
