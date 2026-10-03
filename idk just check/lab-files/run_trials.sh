#!/usr/bin/env bash
# Usage: bash run_trials.sh ./vulp 300 task2b
# Starts the VICTIM repeatedly. Start an attacker separately in terminal A.
set -euo pipefail
cd -- "$(dirname -- "$0")"
victim=${1:-./vulp}
duration=${2:-300}
label=${3:-trial}
if [[ $(id -u) == 0 ]]; then
    echo "Run as seed, without sudo." >&2; exit 1
fi
case "$victim" in
    ./vulp|./vulp_least) ;;
    *) echo "Choose ./vulp or ./vulp_least (not the slow demo)." >&2; exit 1 ;;
esac
if [[ ! $duration =~ ^[1-9][0-9]*$ || ! $label =~ ^[a-zA-Z0-9_-]+$ ]]; then
    echo "Duration must be positive seconds; label uses letters/numbers/_/-." >&2
    exit 1
fi
if [[ ! -x $victim || ! -u $victim || $(stat -c %u "$victim") != 0 ]]; then
    echo "Victim must be executable, root-owned and Set-UID. Run bash build.sh." >&2
    exit 1
fi
if [[ ! -f input.txt ]]; then
    echo "Create input.txt as described in the guide first." >&2; exit 1
fi
input=$(cat input.txt)
if [[ -z $input || ${#input} -gt 50 || $input == *[[:space:]]* || $input != test:* ]]; then
    echo "input.txt must contain one test: record, <=50 characters, no whitespace." >&2
    exit 1
fi
if grep -q '^test:' /etc/passwd; then
    echo "test already exists. Stop attackers and restore the clean baseline first." >&2
    exit 1
fi
mkdir -p logs
summary="logs/${label}-summary.txt"
last="logs/${label}-last-output.txt"
if [[ -e $summary || -e $last ]]; then
    echo "Label already has logs; choose a unique label to preserve evidence." >&2
    exit 1
fi
before=$(sha256sum /etc/passwd)
start=$SECONDS
attempts=0
interrupted=0
printf 'Start: %s\nVictim: %s\nLimit: %s seconds\nBefore: %s\n' \
    "$(date -Is)" "$victim" "$duration" "$before" | tee "$summary"
# Finish and count the in-flight invocation before reporting an interruption.
# The visible runner sends TERM to this monitor, then waits before any reset.
trap 'interrupted=130' INT
trap 'interrupted=143' TERM
while (( interrupted == 0 && SECONDS - start < duration )); do
    status=0
    attempts=$((attempts + 1))
    "$victim" < input.txt > "$last" 2>&1 || status=$?
    after=$(sha256sum /etc/passwd)
    if [[ $before != "$after" ]]; then
        printf 'CHANGE detected after %s attempts and %s seconds.\nAfter: %s\n' \
            "$attempts" "$((SECONDS - start))" "$after" | tee -a "$summary"
        if grep -Fxq -- "$input" /etc/passwd; then
            echo 'Exact input record found. Stop attacker; verify login and id manually.' | tee -a "$summary"
        else
            echo 'File changed, but exact record is absent. Inspect; do not claim success.' | tee -a "$summary"
        fi
        exit 0
    fi
    if (( status == 126 || status == 127 )); then
        cat "$last"; exit "$status"
    fi
    if (( attempts % 1000 == 0 )); then
        printf 'Attempts=%s elapsed=%ss last_exit=%s\n' \
            "$attempts" "$((SECONDS - start))" "$status" | tee -a "$summary"
    fi
done
if (( interrupted != 0 )); then
    printf 'INTERRUPTED after %s attempts and %s seconds; signal_exit=%s.\n' \
        "$attempts" "$((SECONDS - start))" "$interrupted" | tee -a "$summary"
    printf 'After: %s\n' "$(sha256sum /etc/passwd)" | tee -a "$summary"
    echo 'Stop the attacker in terminal A as well.' | tee -a "$summary"
    exit "$interrupted"
fi
printf 'NO CHANGE within %ss; attempts=%s. This is an observation, not proof of impossibility.\n' \
    "$((SECONDS - start))" "$attempts" | tee -a "$summary"
echo 'Stop the attacker in terminal A. Last victim output:' | tee -a "$summary"
cat "$last" | tee -a "$summary"
