#!/usr/bin/env bash
# Documented reset and experiment setup, visibly invoked by seed in terminal B.
set -euo pipefail
cd /home/seed/issd-member5/lab-files
bash ../automation/reset.sh
set -x
sudo sysctl -w fs.protected_symlinks=0
sudo sysctl -w fs.protected_regular=0
# These /proc/sys entries are mode 0600 in this VM, so reading needs sudo too.
sudo sysctl fs.protected_symlinks fs.protected_regular
ls -ld /tmp
ls -l vulp vulp_slow vulp_least attack_naive attack_atomic
findmnt -T . -o TARGET,FSTYPE,OPTIONS
cat input.txt
nm -D vulp | grep -E 'access|fopen|sleep' || true
if nm -D vulp | grep -w sleep; then
    echo 'Unexpected delay symbol in the no-delay victim. Stopping.' >&2
    exit 1
fi
echo 'vulp has access/fopen and no imported sleep symbol.'
nm -D vulp_least | grep -E 'getuid|seteuid|access|fopen'
sha256sum vulp vulp_least attack_naive attack_atomic
id
