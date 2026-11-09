#!/bin/sh
# Sets the OSINTko wallpaper on every xfce4-desktop monitor/workspace.
#
# A static xfconf XML can't do this reliably: the real property path is
# /backdrop/screen0/monitor<NAME>/workspace<N>/last-image, where <NAME> is
# whatever the display driver reports at runtime (e.g. "Virtual-1" under
# UTM/QEMU), not a predictable "monitor0" - confirmed via `xrandr --query`
# on a live image, where xfdesktop never registered monitor0 at all; it was
# only ever this script's own fallback guess, which xfdesktop never read.
# Deriving the name directly from xrandr is deterministic and doesn't
# depend on racing xfdesktop's own (possibly nonexistent) property init.
# This also has to run after login, not at build time, since
# kali-desktop-xfce seeds its own per-user xfconf defaults via /etc/skel,
# which would otherwise take priority over anything set globally.
set -eu

WALLPAPER=/usr/share/backgrounds/osintko-images/kali_osintko_16x9.png
CHANNEL=xfce4-desktop

monitors=$(xrandr --query 2>/dev/null | awk '/ connected/ {print $1}')
[ -z "$monitors" ] && monitors="monitor0"

for monitor in $monitors; do
	for workspace in 0 1 2 3; do
		prop="/backdrop/screen0/monitor${monitor}/workspace${workspace}/last-image"
		xfconf-query --channel "$CHANNEL" --property "$prop" --create \
			--type string --set "$WALLPAPER"
		style_prop="/backdrop/screen0/monitor${monitor}/workspace${workspace}/image-style"
		xfconf-query --channel "$CHANNEL" --property "$style_prop" --create \
			--type int --set 5
	done
done
