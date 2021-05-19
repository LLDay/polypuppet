#!/usr/bin/env bash

PUPPET_VERSION='puppet7-release'

if ! which lsb_release >/dev/null; then
    if which yum >/dev/null; then
        echo 'Installing lsb_release'
        yum install -y redhat-lsb-core >/dev/null
    fi
fi

if which pacman >/dev/null; then
    if ! which puppet >/dev/null; then
        echo 'Installing puppet-agent'
        pacman --noconfirm -Sy puppet >/dev/null
    fi

elif which apt-get >/dev/null; then
    echo 'Updating apt-get'
    apt-get update -y >/dev/null
    echo 'Installing necessary packages'
    apt-get install -y wget ca-certificates gpg >/dev/null

    echo 'Importing puppet repository'
    VERSION=$(lsb_release -sc | tr '[:upper:]' '[:lower:]')
    FILENAME="$PUPPET_VERSION-$VERSION.deb"
    wget -q "https://apt.puppet.com/$FILENAME"
    dpkg -i "$FILENAME" >/dev/null
    rm "$FILENAME"
    apt-get update >/dev/null

    echo 'Installing puppet-agent'
    apt-get install -y -o Dpkg::Options::="--force-confold" puppet-agent >/dev/null 2>&1

    case $(lsb_release -is) in
        Debian)
            FOREMAN_NAME=buster;;
        *)
            FOREMAN_NAME=bionic;;
    esac

    echo 'Importing foreman repository'
    echo "deb http://deb.theforeman.org/ $FOREMAN_NAME nightly" > /etc/apt/sources.list.d/foreman.list
    echo "deb http://deb.theforeman.org/ plugins nightly" >> /etc/apt/sources.list.d/foreman.list
    wget -q https://deb.theforeman.org/pubkey.gpg -O- > /etc/apt/trusted.gpg.d/foreman.asc
    apt-get update >/dev/null

elif which yum >/dev/null; then
    DIST=$(lsb_release -is | tr '[:upper:]' '[:lower:]')
    VERSION=$(lsb_release -rs)

    if [ $DIST != 'fedora' ]; then
        DIST='el'
        VERSION=$(echo $VERSION | cut -c1)
        echo 'Importing foreman repository'
        yum -y install http://dl.fedoraproject.org/pub/epel/epel-release-latest-${VERSION}.noarch.rpm >/dev/null
        yum -y install https://yum.theforeman.org/releases/nightly/el${VERSION}/x86_64/foreman-release.rpm >/dev/null
    fi

    rpm -Uvh "https://yum.puppet.com/$PUPPET_VERSION-$DIST-$VERSION.noarch.rpm"
    echo 'Installing puppet-agent'
    yum install -y puppet-agent >/dev/null

elif which brew >/dev/null; then
    echo 'Installing puppet-agent'
    brew install puppetlabs/puppet/puppet-agent >/dev/null
fi
