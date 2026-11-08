#!/bin/sh
# Fills all free space with zeros, then deletes the fill file. Deleted/freed
# blocks still hold their old leftover bytes until something overwrites
# them, so qemu-img convert would otherwise have to store that garbage too.
# Zeroing it first lets qcow2's own zero-cluster detection skip it - a
# build-time-only trick with no effect on runtime write performance, unlike
# qcow2 compression (-c in export-qcow2.sh), which is handled separately.
set -eu

dd if=/dev/zero of=/EMPTY bs=1M 2>/dev/null || true
rm -f /EMPTY
sync
