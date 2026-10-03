#!/usr/bin/env bash
# Re-enable only the guide's documented lab setup for follow-up evidence capture.
set -euo pipefail
cd /home/seed/issd-member5/lab-files
[[ $(id -u) == 1000 && $EUID == 1000 ]] || exit 1
if pgrep -a -x 'attack_naive|attack_atomic|vulp|vulp_slow|vulp_least|su'; then
    echo 'Stop experiments and exit root login shells first.' >&2
    exit 1
fi
set -x
id
pwd
sudo cmp /etc/passwd /root/issd-member5-passwd.original
sha256sum -c ../passwd-before.sha256
sudo chmod 4755 vulp vulp_slow vulp_least
sudo sysctl -w fs.protected_symlinks=0 fs.protected_regular=0
sudo sysctl fs.protected_symlinks fs.protected_regular
ls -ld /tmp
ls -l vulp vulp_slow vulp_least attack_naive attack_atomic
