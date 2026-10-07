# Member 6 — short live demonstration command sheet

**PREPARED, NOT REHEARSED.** Use only after the actual lab, S02 verification and genuine Task 1/2 evidence are complete. All commands below run in the separate SEED 12.04 VM as ordinary `seed`, except the labelled administrative target preparation/reset.

## Before the presentation

Confirm the group's allowance; the existing plan suggests 5–7 minutes. Open real S07, S09, S10 and S11 outside the VM as recorded-evidence backup. There are **no such M6 captures yet** at this preparation checkpoint.

**MANUAL ACTION REQUIRED — VM: prepare the known lab dummy**

```bash
cd ~/issd-member6/lab-files
bash ../automation/check-environment.sh
pgrep -x cow_attack
id
```

Proceed only if the environment is correct and no attacker remains. If `/zzz` exists, establish that it is the known lab target before resetting:

```bash
sudo sh -c 'printf "111111222222333333\n" > /zzz'
sudo chown root:root /zzz
sudo chmod 0644 /zzz
RUN=presentation-dummy-$(date -u +%Y%m%dT%H%M%SZ)
```

Enter any VM sudo password manually. Explain COW and the two worker operations before beginning the demonstration.

## Slide 4 → live terminal

```bash
id
ls -l /zzz
cat /zzz
echo 99999 > /zzz
./cow_control
cat /zzz
bash ../automation/trial-with-evidence.sh dummy 15 "$RUN"
cat /zzz
ls -l /zzz
cat "logs/$RUN-summary.txt"
```

Explain the **actual** output in order: ordinary write denial; private-memory change but original file unchanged; bounded race result verified from a fresh file read. If the live run is partial/unchanged, say so and show an earlier genuine S07 only if it has actually been collected. Identify it as recorded and use its real runtime. Do not promise success within 15 seconds.

## Slide 5 → recorded account proof

Show the actual S08 normal UID, S09 exact UID-only diff and S10 **non-sudo** login/`id -u` proof. State that the account experiment was recorded. Explain unchanged field width, password continuity and numeric UID 0. Show S11 restoration as the final account state. Do not type a template UID in place of the measured UID.

## After rehearsal/presentation

**MANUAL ACTION REQUIRED — VM:** close any test login shells; confirm no attacker, remove the known dummy, and verify the normal account baseline:

```bash
pgrep -x cow_attack
pgrep -x su
id
sudo rm -f /zzz
bash ../automation/check-cleanup.sh
```

Keep the new presentation trial logs. A successful future oral rehearsal, duration, classroom demonstration or course upload has not been claimed by this preparation sheet.
