#!/usr/bin/env bash
# Guide section 11 controls, after the concurrent trial and attacker have ended.
set -euo pipefail
cd /home/seed/issd-member5/lab-files
label=${1:?Provide the completed trial label}
[[ $label =~ ^[a-zA-Z0-9_-]+$ ]] || exit 1
[[ $(id -u) == 1000 && $EUID == 1000 ]] || exit 1
if pgrep -a -x 'attack_naive|attack_atomic|vulp|vulp_slow|vulp_least|su'; then
    echo 'Stop the experiment and exit login shells before the static controls.' >&2
    exit 1
fi
if pgrep -af '[b]ash run_trials.sh'; then
    echo 'Monitor still running.' >&2
    exit 1
fi
set -x
id
ls -l vulp_least
ln -sfn /etc/passwd /tmp/XYZ
ls -l /tmp/XYZ
status=0
./vulp_least < input.txt || status=$?
printf 'Static protected-target exit=%s\n' "$status"
sha256sum /etc/passwd
sha256sum -c ../passwd-before.sha256
grep '^test:' /etc/passwd || echo 'No test account'
if [[ -e ../allowed.txt ]]; then
    cp -p ../allowed.txt "logs/${label}-allowed-before.txt"
fi
printf 'ordinary writable file\n' > ../allowed.txt
ln -sfn "$HOME/issd-member5/allowed.txt" /tmp/XYZ
printf 'normal-operation\n' | ./vulp_least
cat ../allowed.txt
printf '\n'
cp -p ../allowed.txt "logs/${label}-allowed-after.txt"
sha256sum -c ../passwd-before.sha256
