#!/bin/sh
# Usage: export-qcow2.sh <imagename-without-extension> [vdi]
set -eu

image="$1"
extra_format="${2:-}"

# $ARTIFACTDIR is only auto-chdir'd into when fakemachine is active; on
# hosts without KVM (e.g. GitHub's arm64 runners) debos falls back to
# running on the host as-is, so the cwd must be set explicitly here.
cd "$ARTIFACTDIR"

echo "INFO: Generate $image.qcow2"
qemu-img convert -O qcow2 -c "$image".raw "$image".qcow2

echo "INFO: Verify qcow2 content matches raw bytes exactly (checks whether compression corrupts data)"
if qemu-img compare "$image".raw "$image".qcow2; then
	echo "INFO: qcow2 content matches raw image - compression is not corrupting data"
else
	echo "ERROR: qcow2 content differs from raw image - compression is corrupting data"
	exit 1
fi

if [ "$extra_format" = "vdi" ]; then
	echo "INFO: Generate $image.vdi (VirtualBox, for Windows/Linux hosts - no qcow2-style compression, so expect a larger file)"
	qemu-img convert -O vdi "$image".raw "$image".vdi
	echo "INFO: Final vdi size:"
	ls -lh "$image".vdi
	sha256sum "$image".vdi >"$image".vdi.sha256
fi

rm -f "$image".raw

sha256sum "$image".qcow2 >"$image".qcow2.sha256

echo "INFO: Final qcow2 size:"
ls -lh "$image".qcow2
