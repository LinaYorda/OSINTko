#!/bin/sh
# Usage: export-qcow2.sh <imagename-without-extension>
set -eu

image="$1"

# $ARTIFACTDIR is only auto-chdir'd into when fakemachine is active; on
# hosts without KVM (e.g. GitHub's arm64 runners) debos falls back to
# running on the host as-is, so the cwd must be set explicitly here.
cd "$ARTIFACTDIR"

echo "INFO: Generate $image.qcow2"
qemu-img convert -O qcow2 "$image".raw "$image".qcow2
rm -f "$image".raw
