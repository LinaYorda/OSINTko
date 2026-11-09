#!/bin/sh
set -eu

apt-get autoremove -y --purge
rc_packages=$(dpkg --list | grep "^rc" | tr -s " " | cut -d " " -f 2)
if [ -n "$rc_packages" ]; then
	apt-get purge -y "$rc_packages"
fi
apt-get clean
rm -rf /var/lib/apt/lists/*
# Empty, not delete: systemd regenerates a fresh machine-id at first boot
# when this file exists but is empty. A fully missing file instead makes
# accounts-daemon abort on startup (confirmed: "Failed to read machine-id:
# ... No such file or directory", crash-looping every ~25s D-Bus activation
# timeout) - that's what was causing the long pre-login/password-field
# delays, not boot-time I/O.
: > /etc/machine-id
# Not clearing /tmp: debos mounts the currently-running script at
# /tmp/script, so rm -rf /tmp/* fails with "Device or resource busy".
rm -rf /var/tmp/*
