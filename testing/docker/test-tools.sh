#!/bin/bash
# Tries to start every vendored OSINTko tool and classifies the result.
# This proves a tool starts without crashing - it does NOT prove it still
# does useful OSINT work against live third-party sites/APIs.
set -u

REPORT=/opt/test-tools-report.txt
: > "$REPORT"

test_tool() {
	local name="$1"
	local bin_path
	bin_path=$(command -v "$name" 2>/dev/null)
	if [ -z "$bin_path" ]; then
		echo "MISSING     $name (not found on PATH / file absent)" >>"$REPORT"
		return
	fi

	local out rc
	out=$(timeout 15 "$name" --help 2>&1)
	rc=$?
	if [ $rc -eq 124 ]; then
		echo "TIMEOUT     $name" >>"$REPORT"
	elif echo "$out" | grep -qiE "exec format error|cannot execute binary"; then
		echo "ARCH_FAIL   $name (wrong architecture)" >>"$REPORT"
	elif echo "$out" | grep -qiE "ModuleNotFoundError|ImportError|DistributionNotFound|PackageNotFoundError"; then
		local err
		err=$(echo "$out" | grep -iE "ModuleNotFoundError|ImportError|DistributionNotFound|PackageNotFoundError" | head -1)
		echo "IMPORT_FAIL $name ($err)" >>"$REPORT"
	elif echo "$out" | grep -qiE "EOFError: EOF when reading a line"; then
		echo "INTERACTIVE $name (ignores --help, blocks on stdin menu - needs manual test)" >>"$REPORT"
	elif echo "$out" | grep -qi "Traceback"; then
		echo "FAIL        $name (unhandled exception, see above)" >>"$REPORT"
	elif [ $rc -eq 0 ] || echo "$out" | grep -qiE "usage|options|argument"; then
		echo "PASS        $name" >>"$REPORT"
	else
		echo "FAIL        $name (exit $rc)" >>"$REPORT"
	fi
}

TOOLS=(
	aliens_eye social-analyzer osgint holehe instaloader socialscan
	blackbird xosint
	maigret near zehef mailaccess linkook ghunt
	sn0int subfinder
)

for t in "${TOOLS[@]}"; do
	test_tool "$t"
done

echo "=== TEST-TOOLS REPORT ($(uname -m)) ==="
sort "$REPORT"