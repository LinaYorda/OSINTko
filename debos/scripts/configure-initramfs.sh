#!/bin/sh
# OSINTko only ever runs as a VM (UTM/VirtualBox on macOS - see README), never
# on bare metal, but initramfs-tools' default MODULES=most bundles driver
# support for every PCI/USB/SCSI/RAID controller Debian ships, for hardware
# this image will never see. That bloats the initrd to tens of MB, which
# GRUB has to read off disk before the kernel even starts - directly adding
# to boot time. Restricting to just the storage stack a VM actually uses
# keeps the initrd small without needing a kernel rebuild.
set -eu

sed -i 's/^MODULES=.*/MODULES=list/' /etc/initramfs-tools/initramfs.conf

cat >/etc/initramfs-tools/modules <<-EOF
	virtio
	virtio_pci
	virtio_ring
	virtio_blk
	virtio_scsi
	virtio_console
	nvme
	ahci
	sd_mod
	ext4
EOF

# The kernel package's postinst already built one default (MODULES=most)
# initrd before this script ran - rebuild it now so the shipped image
# actually reflects the trimmed module list, not the stale default one.
update-initramfs -u -k all
