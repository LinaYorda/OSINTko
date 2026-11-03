#!/bin/sh
# Adds a 127.0.1.1 <hostname> line to /etc/hosts. Without it, PAM/session
# startup and various desktop components resolving the local hostname fall
# through to DNS, which times out with no reachable server - causing slow
# logins and general sluggishness. Ported from Trace Labs' finish-install.sh.
set -eu

hostname=$(cat /etc/hostname)

if grep -Eq "^127\.0\.1\.1\s+$hostname" /etc/hosts; then
	echo "INFO: hostname already present in /etc/hosts"
	exit 0
fi

if ! grep -Eq "^127\.0\.0\.1\s+localhost" /etc/hosts; then
	echo "ERROR: couldn't find localhost in /etc/hosts"
	exit 1
fi

echo "INFO: adding line '127.0.1.1 $hostname' to /etc/hosts"
sed -Ei "/^127\.0\.0\.1\s+localhost/a 127.0.1.1\t$hostname" /etc/hosts
