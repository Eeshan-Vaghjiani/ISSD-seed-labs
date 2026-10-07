#!/usr/bin/env bash
# Read-only verification AFTER the guide's manual restoration and shell exits.
# sudo is used only to compare the root-held normal-account backup.
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")" && pwd -P)
source "$HERE/guest-guard.sh"
m6_require_guest
cd /home/seed/issd-member6/lab-files
m6_require_workspace
m6_no_attacker
m6_no_process cow_control
m6_no_process su
id
sudo cmp /etc/passwd /root/issd-member6-passwd.normal
sha256sum -c ../provenance/passwd-normal.sha256
grep '^charlie:' /etc/passwd
cmp <(grep '^charlie:' /etc/passwd) ../provenance/charlie-normal.txt
uid=$(awk -F: '$1 == "charlie" {print $3}' /etc/passwd)
[[ $uid =~ ^[0-9]+$ && ! $uid =~ ^0+$ ]] || exit 1
id charlie
if [[ -e /zzz || -L /zzz ]]; then
    echo 'STOP: the lab dummy /zzz still exists.' >&2
    exit 1
fi
echo '/zzz is absent.'
echo '+ numeric UID-0 records'
awk -F: '$3 == 0 {print $1 ":" $3}' /etc/passwd
cmp <(awk -F: '$3 == 0 {print $1 ":" $3}' /etc/passwd) ../provenance/uid0-normal.txt
echo '+ inspect privileged shell processes'
processes=$(ps -eo pid=,ppid=,ruid=,euid=,tty=,comm=,args=)
suspects=$(printf '%s\n' "$processes" | awk '$4 == 0 && $6 ~ /^(bash|sh|dash|zsh|ksh|fish)$/')
if [[ -n $suspects ]]; then
    printf '%s\n' "$suspects"
    echo 'STOP: inspect these privileged shells; do not claim session cleanup yet.' >&2
    exit 1
fi
sha256sum -c SOURCE_SHA256SUMS
ls -l cow_attack cow_control
for binary in cow_attack cow_control; do
    [[ -f $binary && ! -L $binary && -x $binary &&
       $(stat -c '%u:%a' "$binary") == "$(id -u):755" ]] || exit 1
done
echo 'Checked: exact normal passwd/charlie/UID-0 baseline, no attacker/su/root shell, no /zzz.'
echo 'S11 must also contain a fresh non-sudo charlie login with the original nonzero UID.'
