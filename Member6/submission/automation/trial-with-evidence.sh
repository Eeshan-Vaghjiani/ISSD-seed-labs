#!/usr/bin/env bash
# Add metadata/transcript capture around the UNCHANGED supplied trial helper.
# Usage (in the verified guest): bash ../automation/trial-with-evidence.sh dummy 30 task1-run1
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")" && pwd -P)
source "$HERE/guest-guard.sh"
m6_require_guest
cd /home/seed/issd-member6/lab-files
m6_require_workspace
m6_no_attacker
mode=${1:?Use dummy or passwd}
seconds=${2:?Supply a positive runtime limit}
label=${3:?Supply a fresh trial label}
[[ $seconds =~ ^[1-9][0-9]*$ && $label =~ ^[A-Za-z0-9_-]+$ ]] || exit 1
case "$mode" in
    dummy)
        target=/zzz
        cmp -s /zzz <(printf '111111222222333333\n') || {
            echo 'STOP: /zzz does not match the exact normal baseline.' >&2; exit 1;
        } ;;
    passwd)
        target=/etc/passwd
        sha256sum -c ../provenance/passwd-normal.sha256
        # The trusted root backup and the normal login are established at S08.
        ;;
    *) echo 'Mode must be dummy or passwd.' >&2; exit 1 ;;
esac
[[ -f $target && ! -L $target && ! -w $target ]] || exit 1
[[ $(stat -c '%u:%g:%a' "$target") == 0:0:644 ]] || {
    echo 'STOP: target must retain root:root mode 0644.' >&2; exit 1;
}
sha256sum -c SOURCE_SHA256SUMS
for binary in cow_attack cow_control; do
    if [[ ! -f $binary || -L $binary || ! -x $binary ||
          $(stat -c '%u:%a' "$binary") != "$(id -u):755" ]]; then
        echo "STOP: $binary must be a seed-owned regular 0755 executable from the guest build." >&2
        exit 1
    fi
done
mkdir -p logs
prefix=logs/$label
if compgen -G "${prefix}-*" >/dev/null; then
    echo 'STOP: this label already has artifacts. Preserve them and choose a new label.' >&2
    exit 1
fi

record_trial() {
    local status=0
    printf '+ id\n'
    id
    printf '+ stat -c %%u:%%g:%%a:%%s %s\n' "$target"
    stat -c '%u:%g:%a:%s' "$target" | tee "${prefix}-metadata-before.txt"
    printf '+ bash run_trial.sh %s %s %s\n' "$mode" "$seconds" "$label"
    bash run_trial.sh "$mode" "$seconds" "$label" || status=$?
    printf 'Supplied wrapper exit: %s\n' "$status"
    m6_no_attacker
    stat -c '%u:%g:%a:%s' "$target" | tee "${prefix}-metadata-after.txt"
    if (( status != 0 )); then
        # Interrupted wrappers may omit their after copy. Preserve a separately
        # named recovery observation; do not invent a completed trial summary.
        cp -- "$target" "${prefix}-interrupted-current.txt"
        echo 'INCOMPLETE TRIAL: saved current state; inspect before resetting.'
        return "$status"
    fi
    python "$HERE/verify-trial.py" "$mode" "$prefix" --live
}
record_trial 2>&1 | tee "${prefix}-session.txt"
