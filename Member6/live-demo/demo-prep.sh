#!/usr/bin/env bash
# Member 6 — presentation prep (part of the live-demo kit).
#
# WHERE: inside the SEED VM (ISSD-Member6-SEED12), as seed.
# WHEN : after the recording shell is already running (step 2 of DEMO_SCRIPT.md).
# HOW  : you must SOURCE it (keeps the $RUN label for later commands):
#
#     cd ~/issd-member6/lab-files
#     source ~/demo-prep.sh          # or paste this whole file instead
#
# It asks for the VM sudo password once — type it, nothing appears.
# Re-prep is safe: it rewrites /zzz and picks a fresh RUN label (rehearse freely),
# but run it once per round on the day so the RUN label stays unique.
test "${BASH_SOURCE[0]}" != "$0" || { echo 'Run it with:  source demo-prep.sh'; return 1 2>/dev/null || exit 1; }

echo '== 1. basic guards: right VM, no leftover attacker, account file untouched =='
source ../automation/guest-guard.sh &&
  m6_require_guest && m6_require_workspace &&
  m6_no_attacker && m6_no_process su &&
  sha256sum -c ../provenance/passwd-normal.sha256 &&
  id charlie || { echo 'STOP: a basic check failed — use the recorded evidence instead (see DEMO_SCRIPT.md).'; return 1 2>/dev/null || true; }

echo '== 2. creating the root-owned demo file /zzz =='
sudo sh -c 'printf "111111222222333333\n" > /zzz'
sudo chown root:root /zzz
sudo chmod 0644 /zzz
sha256sum -c ../provenance/dummy-normal.sha256

echo '== 3. unique trial label + before-evidence metadata =='
RUN="presentation-dummy-$(date -u +%Y%m%dT%H%M%SZ)-$$"
echo "$RUN" > "logs/.presentation-RUN"
(set -C; stat -c '%u:%g:%a:%s' /zzz > "logs/$RUN-metadata-before.txt")
echo "RUN=$RUN   (label saved to logs/.presentation-RUN)"
echo '== PREP DONE — /zzz is ready. Do NOT close this terminal until after the cleanup script =='
