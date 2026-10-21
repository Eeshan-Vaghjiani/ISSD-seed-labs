#!/usr/bin/env bash
# Member 6 — after-demo cleanup (part of the live-demo kit).
#
# WHERE: inside the SEED VM, inside the recording shell, as seed.
# WHEN : right after the demonstration (before you close anything).
# HOW  :     bash ~/demo-cleanup.sh
#
# Keeps an honest record even if the live race did not win.

cd ~/issd-member6/lab-files || exit 1

echo '== 1. save after-metadata, then let the trial verifier check the live run =='
RUN=$(cat logs/.presentation-RUN 2>/dev/null)
if [ -n "$RUN" ]; then
  (set -C; stat -c '%u:%g:%a:%s' /zzz > "logs/$RUN-metadata-after.txt")
  (set -C; python ../automation/verify-trial.py dummy "logs/$RUN" --live > "logs/$RUN-verification.log" 2>&1)
  echo "trial verifier exit code: $?   (0 = verified; anything else = honest 'race did not win' result, kept in logs)"
else
  echo 'no trial label found — was the demo prepped on another terminal?'
fi

echo '== 2. guards: no attacker or su process left behind =='
source ../automation/guest-guard.sh
m6_no_attacker && m6_no_process su

echo '== 3. /etc/passwd still the normal copy? (cmp prints nothing when identical) =='
sudo cmp /etc/passwd /root/issd-member6-passwd.normal && echo 'passwd: identical'

echo '== 4. remove the demo file and run the full cleanup checker =='
sudo rm -f -- /zzz
bash ../automation/check-cleanup.sh
echo '== CLEANUP DONE — now type:  exit   (leaves the recording shell) =='
