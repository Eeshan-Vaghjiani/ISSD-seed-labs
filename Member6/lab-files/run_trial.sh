#!/usr/bin/env bash
# Usage: bash run_trial.sh dummy 30 task1-run1
#        bash run_trial.sh passwd 30 task2-run1
# Runtime limit is seconds; this helper never changes target permissions.
set -euo pipefail
cd -- "$(dirname -- "$0")"
mode=${1:-dummy}
seconds=${2:-30}
label=${3:-trial}
if [[ $(id -u) == 0 ]]; then
    echo 'Run as seed without sudo.' >&2; exit 1
fi
if [[ ! $seconds =~ ^[1-9][0-9]*$ || ! $label =~ ^[a-zA-Z0-9_-]+$ ]]; then
    echo 'Use positive integer seconds and a label containing letters/numbers/_/-.' >&2
    exit 1
fi
args=("$mode")
case "$mode" in
    dummy) target=/zzz ;;
    passwd)
        target=/etc/passwd
        uid=$(awk -F: '$1=="charlie" {print $3}' /etc/passwd)
        if [[ ! $uid =~ ^[0-9]+$ || $uid =~ ^0+$ ]]; then
            echo 'Create charlie or restore its normal nonzero UID first.' >&2; exit 1
        fi
        args+=("$uid") ;;
    *) echo 'Mode must be dummy or passwd.' >&2; exit 1 ;;
esac
if [[ ! -x ./cow_attack || -u ./cow_attack ]]; then
    echo 'Run bash build.sh; cow_attack must not be Set-UID.' >&2; exit 1
fi
command -v timeout >/dev/null
mkdir -p logs
prefix="logs/$label"
if [[ -e ${prefix}-summary.txt ]]; then
    echo 'Choose a fresh run label to preserve existing evidence.' >&2; exit 1
fi
cp -- "$target" "${prefix}-before.txt"
before=$(sha256sum "$target")
printf 'Date: %s\nKernel: %s\nIdentity: %s\nTarget: %s\nLimit: %ss\nBefore: %s\n' \
    "$(date -Iseconds)" "$(uname -r)" "$(id)" "$target" "$seconds" "$before" \
    | tee "${prefix}-summary.txt"
start=$SECONDS
child=''
stop_child() {
    if [[ -n $child ]]; then
        # GNU timeout forwards TERM to its managed process group.
        kill -TERM "$child" 2>/dev/null || true
        wait "$child" 2>/dev/null || true
        child=''
    fi
}
trap stop_child EXIT
trap 'echo "Interrupted; inspect target and reset before retrying."; exit 130' INT TERM
timeout --signal=TERM --kill-after=2s "${seconds}s" ./cow_attack "${args[@]}" \
    > "${prefix}-program.txt" 2>&1 &
child=$!
changed=no
while kill -0 "$child" 2>/dev/null; do
    if [[ $(sha256sum "$target") != "$before" ]]; then
        changed=yes
        stop_child
        break
    fi
    sleep 0.2
done
status=0
if [[ -n $child ]]; then
    wait "$child" || status=$?
    child=''
fi
cp -- "$target" "${prefix}-after.txt"
after=$(sha256sum "$target")
[[ $before == "$after" ]] || changed=yes
printf 'Elapsed: %ss\nChange detected: %s\nAfter: %s\n' \
    "$((SECONDS - start))" "$changed" "$after" | tee -a "${prefix}-summary.txt"
if [[ $changed == yes ]]; then
    echo 'Stopped after content change; inspect the full diff and verify exact outcome.' \
        | tee -a "${prefix}-summary.txt"
else
    printf 'No target change. Process exit=%s (124 means timeout). Review program output.\n' \
        "$status" | tee -a "${prefix}-summary.txt"
fi
cat "${prefix}-program.txt"
diff -u "${prefix}-before.txt" "${prefix}-after.txt" || true
echo 'A content change alone is not proof of UID 0; follow the guide verification steps.'
