#!/bin/sh
set -eu

apt-get -y remove desktop-base tango-icon-theme xorg
apt-get -y autoremove
