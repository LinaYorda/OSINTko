#!/bin/sh
set -eu

apt-get clean
rm -rf /var/lib/apt/lists/*
rm -f /etc/machine-id
rm -rf /tmp/* /var/tmp/*
