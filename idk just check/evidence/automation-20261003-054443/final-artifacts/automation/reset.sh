#!/usr/bin/env bash
# Run as seed in evidence terminal B. Only documented administration uses sudo.
set -euo pipefail
cd /home/seed/issd-member5/lab-files
if [[ $(id -u) != 1000 || $EUID != 1000 ]]; then
    echo 'Exit any root login shell first. Reset must be launched as seed.' >&2
    exit 1
fi
set -x
id
date -Is
if pgrep -a -x 'attack_naive|attack_atomic|vulp|vulp_slow|vulp_least|su'; then
    echo 'Experiment or su process is still present. Reset stopped.' >&2
    exit 1
fi
if pgrep -af '[b]ash run_trials.sh'; then
    echo 'Trial monitor is still present. Reset stopped.' >&2
    exit 1
fi
sudo test -f /root/issd-member5-passwd.original
sudo cp -a /root/issd-member5-passwd.original /etc/passwd
sudo cmp /etc/passwd /root/issd-member5-passwd.original
echo 'Clean password-file baseline restored'
sha256sum -c ../passwd-before.sha256
if grep '^test:' /etc/passwd; then
    echo 'Unexpected test record in restored baseline. Stopping.' >&2
    exit 1
fi
echo 'No test record remains'
sudo rm -f /tmp/XYZ /tmp/ABC
id
