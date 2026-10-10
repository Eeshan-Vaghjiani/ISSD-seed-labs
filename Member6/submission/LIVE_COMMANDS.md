# Live commands — Member 6 — ISSD

**All commands on this sheet run inside ISSD-Member6-SEED12 as seed.** Prepare the VM and a fresh `$RUN` using Part 0 of `LIVE_DEMO.md` before presenting. Actual experiments are complete; the classroom sequence is **prepared, not orally rehearsed**.

## Slide 4 → live dummy demonstration

Keep the same terminal used for preparation. Explain normal COW before starting.

```bash
id
ls -l /zzz
cat /zzz
echo 99999 > /zzz
./cow_control
cat /zzz
sha256sum -c ../provenance/dummy-normal.sha256
bash run_trial.sh dummy 15 "$RUN"
cat /zzz
ls -l /zzz
```

Say what actually happened: direct write denied; normal COW changed private memory only; inspect the race's backing-file result. The 15-second classroom bound differs from the recorded 30-second trials. Then verify the whole result:

```bash
(set -C; stat -c '%u:%g:%a:%s' /zzz > "logs/$RUN-metadata-after.txt")
(set -C; python ../automation/verify-trial.py dummy "logs/$RUN" --live > "logs/$RUN-verification.log" 2>&1)
echo $?
```

Exit 0 means the verifier accepted the exact result and metadata. For another exit, inspect the retained verification/program logs and describe the actual outcome. If the race does not succeed, show **recorded S07 from 9 October 2026**: exact replacement, 0 integer elapsed seconds in its 30-second-bound trial. Keep the new trial's failure/logs.

## Slide 5 → recorded account proof

Show S08 → S09 → S10 → S11, or `video/TASK2_FALLBACK.mp4` with its excerpt labels. Say: **“This is recorded Task 2 evidence from 9 October.”**

* Original UID/GID: **1001 / 1002**. Exact UID field: **1001 → 0000**.
* First authentication failed; second non-sudo login returned **UID 0**, `whoami` root.
* The proof shell ended; complete restoration and a new **UID 1001** login passed.

## After the demonstration → cleanup

After the bounded trial returns, verify seed and stopped processes. Remove only this preparation's known `/zzz`.

```bash
id
source ../automation/guest-guard.sh
m6_no_attacker && m6_no_process su
sudo cmp /etc/passwd /root/issd-member6-passwd.normal
sudo rm -- /zzz
bash ../automation/check-cleanup.sh
```

Enter any sudo password directly in the VM. Stop on an unexpected account/process/permission result and use `LIVE_DEMO.md` recovery. Close/export the recording before shutdown or rollback. Recorded success does not predetermine a future live outcome.
