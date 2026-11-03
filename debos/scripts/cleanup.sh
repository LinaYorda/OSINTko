#!/bin/sh
set -eu

apt-get autoremove -y --purge
rc_packages=$(dpkg --list | grep "^rc" | tr -s " " | cut -d " " -f 2)
if [ -n "$rc_packages" ]; then
	apt-get purge -y "$rc_packages"
fi
apt-get clean
rm -rf /var/lib/apt/lists/*
rm -f /etc/machine-id
# Not clearing /tmp: debos mounts the currently-running script at
# /tmp/script, so rm -rf /tmp/* fails with "Device or resource busy".
rm -rf /var/tmp/*
