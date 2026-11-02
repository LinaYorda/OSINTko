#!/bin/sh
# Usage: create-user.sh <username> <password>
set -eu

username="$1"
password="$2"

useradd -m -s /bin/bash -G sudo,netdev,plugdev "$username"
echo "$username:$password" | chpasswd
