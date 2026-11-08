#!/bin/sh
# Sets the OSINTko wallpaper on every xfce4-desktop monitor/workspace.
#
# A static xfconf XML can't do this reliably: the real property path is
# /backdrop/screen0/monitor<NAME>/workspace<N>/last-image, where <NAME> is
# whatever the virtual display driver reports at runtime (varies by VM/host),
# not a predictable "monitor0". It also has to run after login, not at build
# time, since kali-desktop-xfce seeds its own per-user xfconf defaults via
# /etc/skel, which would otherwise take priority over anything set globally.
set -eu

WALLPAPER=/usr/share/backgrounds/osintko-images/kali_osintko_16x9.png
CHANNEL=xfce4-desktop

# xfdesktop populates its own monitor/workspace property tree on first
# start, which can race this autostart script - retry briefly rather than
# silently doing nothing if the tree isn't there yet.
props=""
i=0
while [ "$i" -lt 10 ]; do
	props=$(xfconf-query --channel "$CHANNEL" --property /backdrop --list 2>/dev/null \
		| grep -E '/workspace[0-9]+/last-image$' || true)
	[ -n "$props" ] && break
	i=$((i + 1))
	sleep 1
done

# Nothing registered yet even after retrying (e.g. xfdesktop never ran) -
# fall back to the one property xfdesktop always honors on a fresh config.
: "${props:=/backdrop/screen0/monitor0/workspace0/last-image}"

echo "$props" | while read -r prop; do
	[ -z "$prop" ] && continue
	xfconf-query --channel "$CHANNEL" --property "$prop" --create \
		--type string --set "$WALLPAPER"
	style_prop=$(dirname "$prop")/image-style
	xfconf-query --channel "$CHANNEL" --property "$style_prop" --create \
		--type int --set 5 2>/dev/null || true
done
