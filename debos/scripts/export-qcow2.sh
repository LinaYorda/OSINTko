#!/bin/sh
# Usage: export-qcow2.sh <imagename-without-extension>
set -eu

image="$1"

echo "INFO: Generate $image.qcow2"
qemu-img convert -O qcow2 "$image".raw "$image".qcow2
rm -f "$image".raw
