#!/usr/bin/env bash
# VM-only build/compatibility checks around the unchanged supplied build.sh.
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")" && pwd -P)
source "$HERE/guest-guard.sh"
m6_require_guest
cd /home/seed/issd-member6/lab-files
m6_require_workspace
m6_no_attacker
label=${1:?Supply a unique build label}
[[ $label =~ ^[A-Za-z0-9_-]+$ ]] || exit 1
manifest="../provenance/$label-binaries.sha256"
[[ ! -e $manifest ]] || { echo 'Preserve the existing build record; use a new label.' >&2; exit 1; }
set -x
id
pwd
df -T .
sha256sum -c SOURCE_SHA256SUMS
bash build.sh
file cow_attack cow_control
stat -c '%n uid=%u gid=%g mode=%a bytes=%s' cow_attack cow_control
python --version
python -c 'compile(open("../automation/verify-trial.py").read(), "verify-trial.py", "exec"); print("Guest verifier syntax OK")'
status=0
timeout --signal=TERM --kill-after=2s 1s /bin/sleep 2 || status=$?
printf 'Timeout compatibility check exit=%s (expected 124)\n' "$status"
[[ $status == 124 ]]
sha256sum cow_attack cow_control | tee "$manifest"
echo 'Build and prerequisite runtime checks passed. No Dirty COW experiment was run by this helper.'
