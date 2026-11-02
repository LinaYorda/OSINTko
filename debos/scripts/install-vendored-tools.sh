#!/bin/bash
# Installs OSINTko's vendored OSINT tools, fresh from their real upstream
# (PyPI if the tool has a package, otherwise a fresh git clone). Tool list
# and sourcing decisions are the result of the testing/docker/ harness run.
set +e

REPORT=/opt/install-report.txt
: > "$REPORT"

# Kali retired unmanaged `pip install` (PEP 668). The entry-point scripts
# pip generates point at /usr/bin/python3, so packages must land in system
# site-packages to be importable.
PIP="pip install --break-system-packages"
pip install --upgrade pip --break-system-packages >/dev/null 2>&1

mkdir -p /opt/new-tools

# Best-effort guess at a tool's CLI entry file, for repos with no
# setup.py/pyproject.toml (just loose scripts). Picks the first obvious
# match, or the single top-level .py file if there's exactly one.
find_entry_point() {
	local dir="$1" name="$2" candidate
	for candidate in "${name}.py" "main.py" "app.py" "__main__.py" \
		"$(tr '[:upper:]' '[:lower:]' <<<"$name").py" \
		"$name" "$(tr '[:upper:]' '[:lower:]' <<<"$name")"; do
		if [ -f "$dir/$candidate" ]; then
			echo "$candidate"
			return 0
		fi
	done
	local pyfiles=("$dir"/*.py)
	if [ "${#pyfiles[@]}" -eq 1 ] && [ -f "${pyfiles[0]}" ]; then
		basename "${pyfiles[0]}"
		return 0
	fi
	return 1
}

# install_tool <name> <pypi-package-or-empty> <git-url-or-empty> [extra pip flags]
# Tries PyPI first (if given), falls back to a fresh git clone.
install_tool() {
	local name="$1" pypi="$2" repo="$3" extra="${4:-}"
	local log="/tmp/install_${name}.log"

	if [ -n "$pypi" ] && $PIP $extra "$pypi" >"$log" 2>&1; then
		echo "INSTALL_OK   $name (pypi:$pypi)" >>"$REPORT"
		return
	fi

	if [ -z "$repo" ]; then
		echo "INSTALL_FAIL $name (no pypi package, no repo url given, see $log)" >>"$REPORT"
		return
	fi

	local dir="/opt/new-tools/$name"
	rm -rf "$dir"
	if ! git clone --depth 1 "$repo" "$dir" >"$log" 2>&1; then
		echo "INSTALL_FAIL $name (git clone failed, see $log)" >>"$REPORT"
		return
	fi

	if [ -f "$dir/pyproject.toml" ] || [ -f "$dir/setup.py" ]; then
		if $PIP "$dir" >>"$log" 2>&1; then
			echo "INSTALL_OK   $name (pip install from source: $repo)" >>"$REPORT"
			return
		fi
		echo "INSTALL_FAIL $name (pip install from source failed, see $log)" >>"$REPORT"
		return
	fi

	if [ -f "$dir/requirements.txt" ]; then
		$PIP -r "$dir/requirements.txt" >>"$log" 2>&1 \
			|| echo "INSTALL_WARN $name (requirements.txt install had errors, see $log)" >>"$REPORT"
	fi

	local entry
	entry=$(find_entry_point "$dir" "$name")
	if [ -n "$entry" ]; then
		cat >"/usr/local/bin/$name" <<-WRAPPER
			#!/bin/sh
			cd "$dir" && exec python3 "$entry" "\$@"
		WRAPPER
		chmod +x "/usr/local/bin/$name"
		echo "INSTALL_OK   $name (git clone: $repo, entry: $entry)" >>"$REPORT"
	else
		echo "INSTALL_FAIL $name (cloned $repo but no entry point found, see $log)" >>"$REPORT"
	fi
}

install_tool aliens_eye      ""              "https://github.com/arxhr007/Aliens_eye"
install_tool social-analyzer "social-analyzer" "https://github.com/qeeqbox/social-analyzer"
install_tool osgint          ""              "https://github.com/hippiiee/osgint"
install_tool holehe          "holehe"        "https://github.com/megadose/holehe"
install_tool instaloader     "instaloader"   "https://github.com/instaloader/instaloader"
install_tool socialscan      "socialscan"    "https://github.com/iojw/socialscan"
install_tool blackbird       ""              "https://github.com/antoniaci/blackbird"
install_tool xosint          ""              "https://github.com/TermuxHackz/X-osint"
install_tool maigret         "maigret"       "https://github.com/soxoj/maigret"
install_tool near            ""              "https://github.com/SamueleAmato/Near"
# Near ships no requirements.txt at all - this is a best-effort guess at
# its real dependency, inferred from the ModuleNotFoundError, not a
# declared requirement. Same undeclared-dependency pattern seen before.
$PIP textual >/tmp/install_near_textual.log 2>&1 \
	&& echo "INSTALL_OK   near (extra guessed dep: textual)" >>"$REPORT" \
	|| echo "INSTALL_FAIL near (guessed dep textual failed, see /tmp/install_near_textual.log)" >>"$REPORT"
install_tool zehef           ""              "https://github.com/N0rz3/Zehef"
install_tool mailaccess      "mailaccess"    "https://github.com/KatrielMoses/MailAccess"
install_tool linkook         "linkook"       "https://github.com/JackJuly/linkook"
# ghunt's dep chain tries to upgrade `packaging`, which was apt-installed
# (python3-packaging) and has no pip RECORD file, so pip can't uninstall it.
install_tool ghunt           "ghunt"         "https://github.com/mxrch/GHunt" "--ignore-installed packaging"

# owlculus is a full backend+frontend+Caddy docker-compose platform. Needs
# a separate `docker-compose up` based check, done manually, not here.

# Non-Python new tools: different toolchains, no PyPI/git-clone pattern ---
# cargo/go install both place binaries under $HOME of the user running them
# (root, during this chroot build) - not on the shipped image's default
# user's PATH. Copy them into /usr/local/bin so they're actually reachable.
if cargo install --locked sn0int >/tmp/install_sn0int.log 2>&1; then
	cp /root/.cargo/bin/sn0int /usr/local/bin/sn0int
	echo "INSTALL_OK   sn0int (cargo)" >>"$REPORT"
else
	echo "INSTALL_FAIL sn0int (cargo install failed, see /tmp/install_sn0int.log)" >>"$REPORT"
fi

if go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest >/tmp/install_subfinder.log 2>&1; then
	cp /root/go/bin/subfinder /usr/local/bin/subfinder
	echo "INSTALL_OK   subfinder (go install)" >>"$REPORT"
else
	echo "INSTALL_FAIL subfinder (go install failed, see /tmp/install_subfinder.log)" >>"$REPORT"
fi

cat "$REPORT"
exit 0
