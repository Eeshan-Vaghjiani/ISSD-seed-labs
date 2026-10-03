#!/usr/bin/env bash
# Guide section 12 stable seed-owned symlink check, after the concurrent trial.
set -euo pipefail
cd /home/seed/issd-member5/lab-files
[[ $(id -u) == 1000 && $EUID == 1000 ]] || exit 1
if pgrep -a -x 'attack_naive|attack_atomic|vulp|vulp_slow|vulp_least|su'; then
    echo 'Stop the experiment and exit login shells before the static control.' >&2
    exit 1
fi
if pgrep -af '[b]ash run_trials.sh'; then
    echo 'Monitor still running.' >&2
    exit 1
fi
set -x
id
ls -l vulp
ln -sfn /dev/null /tmp/XYZ
ls -ld /tmp /tmp/XYZ
status=0
./vulp < input.txt || status=$?
printf 'Static symlink-follow exit=%s\n' "$status"
sha256sum /etc/passwd
sha256sum -c ../passwd-before.sha256
grep '^test:' /etc/passwd || echo 'No test account'
