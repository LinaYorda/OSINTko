#!/bin/sh
set -eu

apt-get clean
rm -rf /var/lib/apt/lists/*
rm -f /etc/machine-id
# Not clearing /tmp: debos mounts the currently-running script at
# /tmp/script, so rm -rf /tmp/* fails with "Device or resource busy".
rm -rf /var/tmp/*
