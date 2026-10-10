#!/usr/bin/env bash
# Read-only guest inventory. Its output is actual command output, not a fixture.
set -uo pipefail
HERE=$(cd -- "$(dirname -- "$0")" && pwd -P)
source "$HERE/guest-guard.sh"

# Reject the Arch host before inspecting guest-specific files or creating logs.
m6_require_guest || exit 1
failed=0
run() {
    local status=0
    printf '\n+ '
    printf '%q ' "$@"
    printf '\n'
    "$@" || status=$?
    if (( status != 0 )); then
        printf 'Command exit status: %s\n' "$status"
        failed=1
    fi
}
run date -u +%Y-%m-%dT%H:%M:%SZ
run whoami
run id
run lsb_release -a
run uname -r
run uname -m
run gcc --version
for tool in gcc bash timeout unzip wget nano python script sha256sum pgrep; do
    run command -v "$tool"
done
run dpkg-query -W "linux-image-$(uname -r)"
run cat /sys/class/dmi/id/product_name
run getconf LONG_BIT
run timeout --version
run pgrep -V

if (( failed != 0 )); then
    echo 'STOP: a required environment/tool check failed. Preserve the error.' >&2
    exit 1
fi
echo 'Prescribed guest identity/release/kernel/architecture checks passed.'
echo 'Review the actual kernel package against the cited SEED manual/vendor information before trials.'
echo 'No experiment has been executed by this checker.'
