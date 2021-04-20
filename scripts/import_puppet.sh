#!/usr/bin/env bash

PUPPET_VERSION=$(polypuppet config puppet_version)
UBUNTU_VERSION=$(lsb_release -sc)
FILENAME="$PUPPET_VERSION-$UBUNTU_VERSION.deb"

apt-get update
apt-get -y install wget
wget -q "https://apt.puppet.com/$FILENAME"
sudo dpkg -i "$FILENAME"
rm "$FILENAME"
apt-get update
