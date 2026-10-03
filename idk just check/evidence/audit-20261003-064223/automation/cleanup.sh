#!/usr/bin/env bash
# Final guide cleanup. User explicitly chose installed policy 1/2 in this session.
# Those values are NOT claimed to be the VM's original runtime values.
set -euo pipefail
cd /home/seed/issd-member5/lab-files
bash ../automation/reset.sh
set -x
cat ../sysctl-before.txt
echo 'Saved file is 0/0; original pre-lab runtime values are not established.'
echo 'User-selected final policy: protected_symlinks=1, protected_regular=2.'
sudo sysctl -w fs.protected_symlinks=1 fs.protected_regular=2
sudo sysctl fs.protected_symlinks fs.protected_regular
sudo chmod 0755 vulp vulp_slow vulp_least
sudo rm -f /tmp/XYZ /tmp/ABC
sudo cmp /etc/passwd /root/issd-member5-passwd.original
echo 'Original password file restored'
sha256sum -c ../passwd-before.sha256
grep '^test:' /etc/passwd || echo 'No test account'
ls -l vulp vulp_slow vulp_least
if pgrep -a -x 'attack_naive|attack_atomic|vulp|vulp_slow|vulp_least|su'; then
    echo 'Unexpected experiment/login process remains.' >&2
    exit 1
fi
if pgrep -af '[b]ash run_trials.sh'; then
    echo 'Unexpected monitor remains.' >&2
    exit 1
fi
echo 'No experiment or su processes remain'
id
