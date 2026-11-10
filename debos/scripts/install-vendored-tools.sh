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
# --ignore-installed: several tools' dep chains want to upgrade a package
# that's already present via apt (packaging, networkx, python-dotenv, yarl,
# ...). Those apt-installed copies have no pip RECORD file, so pip refuses
# to uninstall/upgrade them and aborts the whole install. This is a
# single-use build chroot, so shadowing them with pip's copy is safe.
PIP="pip install --break-system-packages --ignore-installed"
pip install --upgrade pip --break-system-packages >/dev/null 2>&1

mkdir -p /opt/new-tools

# Appends a FAIL/WARN line plus the tail of its log to $REPORT. Without this,
# the actual pip/cargo error only ever lands in an ephemeral /tmp file inside
# the CI container - gone the moment the job ends, leaving only a one-line
# summary with no way to diagnose what actually went wrong.
log_outcome() {
	local status="$1" msg="$2" log="$3"
	echo "$status $msg" >>"$REPORT"
	if [ -f "$log" ]; then
		echo "  --- tail of $log ---" >>"$REPORT"
		tail -n 20 "$log" >>"$REPORT"
		echo "  --- end log ---" >>"$REPORT"
	fi
}

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
		log_outcome "INSTALL_FAIL" "$name (no pypi package, no repo url given)" "$log"
		return
	fi

	local dir="/opt/new-tools/$name"
	rm -rf "$dir"
	if ! git clone --depth 1 "$repo" "$dir" >"$log" 2>&1; then
		log_outcome "INSTALL_FAIL" "$name (git clone failed)" "$log"
		return
	fi
	# Tools without a pypi package run in place via a wrapper that cd's
	# into $dir (set below), as the desktop user, not root. Several write
	# relative paths like logs/ or output/ at runtime, which fails against
	# root-owned files from this clone (e.g. blackbird's os.makedirs("logs/")).
	chmod -R a+rwX "$dir"

	if [ -f "$dir/pyproject.toml" ] || [ -f "$dir/setup.py" ]; then
		if $PIP "$dir" >>"$log" 2>&1; then
			echo "INSTALL_OK   $name (pip install from source: $repo)" >>"$REPORT"
			return
		fi
		log_outcome "INSTALL_FAIL" "$name (pip install from source failed)" "$log"
		return
	fi

	if [ -f "$dir/requirements.txt" ]; then
		$PIP -r "$dir/requirements.txt" >>"$log" 2>&1 \
			|| log_outcome "INSTALL_WARN" "$name (requirements.txt install had errors)" "$log"
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
		log_outcome "INSTALL_FAIL" "$name (cloned $repo but no entry point found)" "$log"
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
# Pinned below 6.0.0: Near's code reads Label.renderable, which Textual
# 6.0.0 renamed to .content (confirmed in textual's own changelog) -
# unpinned pip grabs latest and near.py crashes with AttributeError on
# every list selection.
if $PIP "textual==5.0.0" >/tmp/install_near_textual.log 2>&1; then
	echo "INSTALL_OK   near (extra guessed dep: textual==5.0.0)" >>"$REPORT"
else
	log_outcome "INSTALL_FAIL" "near (guessed dep textual failed)" "/tmp/install_near_textual.log"
fi
install_tool zehef           ""              "https://github.com/N0rz3/Zehef"
# zehef's ~15 account-check modules all do r.json()['status'] with zero
# error handling, including its own Requests.py fallback (a bodyless
# httpx.Response(status_code=500) on transport errors - .json() on that
# raises too). Any single blocked/rate-limited/non-JSON response crashes
# the entire run. Patch httpx.Response.json globally at the one place
# zehef imports httpx, instead of touching all ~15 modules individually.
if [ -f /opt/new-tools/zehef/lib/Requests.py ]; then
	python3 - <<-'PATCH'
		path = "/opt/new-tools/zehef/lib/Requests.py"
		src = open(path).read()
		old = "import httpx\nimport requests\n"
		patch = (
		    "import httpx\n"
		    "import requests\n"
		    "\n"
		    "_original_response_json = httpx.Response.json\n"
		    "class _SafeDict(dict):\n"
		    "    def __missing__(self, key):\n"
		    "        return None\n"
		    "def _safe_response_json(self, *args, **kwargs):\n"
		    "    try:\n"
		    "        return _original_response_json(self, *args, **kwargs)\n"
		    "    except Exception:\n"
		    "        return _SafeDict()\n"
		    "httpx.Response.json = _safe_response_json\n"
		)
		if old in src and "_SafeDict" not in src:
		    open(path, "w").write(src.replace(old, patch, 1))
	PATCH
fi
install_tool mailaccess      "mailaccess"    "https://github.com/KatrielMoses/MailAccess"
install_tool linkook         "linkook"       "https://github.com/JackJuly/linkook"
install_tool ghunt           "ghunt"         "https://github.com/mxrch/GHunt"

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
	log_outcome "INSTALL_FAIL" "sn0int (cargo install failed)" "/tmp/install_sn0int.log"
fi

if go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest >/tmp/install_subfinder.log 2>&1; then
	cp /root/go/bin/subfinder /usr/local/bin/subfinder
	echo "INSTALL_OK   subfinder (go install)" >>"$REPORT"
else
	log_outcome "INSTALL_FAIL" "subfinder (go install failed)" "/tmp/install_subfinder.log"
fi

# cargo/golang-go are only needed to build sn0int/subfinder above - end
# users don't need a Rust/Go toolchain on an OSINT distro. Drop them and
# their caches now that the binaries are in /usr/local/bin.
apt-get -y purge cargo golang-go
apt-get -y autoremove
rm -rf /root/.cargo /root/go

cat "$REPORT"
exit 0
