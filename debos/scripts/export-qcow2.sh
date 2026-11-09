#!/bin/sh
# Usage: export-qcow2.sh <imagename-without-extension>
set -eu

image="$1"

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

rm -f "$image".raw

echo "INFO: Final qcow2 size:"
ls -lh "$image".qcow2
