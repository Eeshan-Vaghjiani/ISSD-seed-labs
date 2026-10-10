# Member 6 — the actual VM session, checkpoint by checkpoint

**Completed-run pointer — 9 October 2026:** all required checkpoints now pass; see [the verified results](submission/RESULTS.md) and [fresh evidence table](evidence/incoming/opus-fresh-20261008/README.md). The VM is powered off normally with charlie restored and the dummy removed. Use `submission/LIVE_PREPARATION.md` for the next rehearsal. The procedure below remains instructional and its expected/actual placeholders are not current results.

**Fresh-run update — 8 October 2026:** the previous session booted the VM and completed environment/transfer/build checks, then stopped before the experiments. The user now requests new screenshots; see [OPENCODE_HANDOFF.md](OPENCODE_HANDOFF.md). This document retains the prepared full procedure. Its per-step expected/actual placeholders are instructions, not a current results ledger. The original [START_TO_FINISH_GUIDE.md](START_TO_FINISH_GUIDE.md) supplies the assignment, source explanation and troubleshooting. Use the existing four lab files. Every command in this document is **inside the SEED VM**, except an explicitly labelled HOST ACTION.

At each checkpoint record **EXPECTED / ACTUAL / EXPLANATION**. “Expected” below is a prediction, never a saved result. Stop at any unexpected environment, setup, account or verification error and send its actual output. Keep failed/partial trials under their original labels.

## 1. First login and environment — S02

**MANUAL ACTION REQUIRED — VM**

* Log in as `seed` using the documented SEED password `dees`.
* Open **Ctrl+Alt+T**. Run:

```bash
whoami
id
lsb_release -a
uname -r
uname -m
gcc --version
command -v gcc
command -v bash
command -v timeout
command -v unzip
command -v wget
command -v nano
command -v python
dpkg-query -W "linux-image-$(uname -r)"
dpkg-query -W -f='${Package}\t${Version}\t${Architecture}\t${Source}\n' "linux-image-$(uname -r)"
cat /sys/class/dmi/id/product_name
date -u
```

**EXPECTED:** ordinary nonzero `seed` identity, Ubuntu 12.04, i386/i686-family architecture, **3.5.0-37-generic**, installed matching i386 kernel package, GCC and the listed tools. The `${Source}` field helps identify the kernel family. Compare the actual package and official image/manual/Ubuntu CVE tracker; the OS name or version number alone does not prove vulnerability.

**ACTUAL:** not observed yet. Save/send all output and `M6-S02-environment.png` (a/b images if necessary). **Stop here for review before running the experiments.** If the release/architecture/kernel is wrong, do not build/run the experiment, substitute a modern guest, or upgrade the vulnerable kernel.

## 2. Transfer onto native guest storage

**MANUAL ACTION REQUIRED — VM: mount an input source and copy**

The primary `M6pack` share is already configured read-only. Try:

```bash
mkdir -p ~/m6-transfer
sudo mount -t vboxsf M6pack ~/m6-transfer
ls ~/m6-transfer/lab-files
```

If prompted, enter the **VM** sudo password directly; nothing is displayed as you type. Expected: the supplied `.c` and `.sh` files. If the mount fails, retain the exact error and use the attached **M6PACK data CD** instead:

```bash
mkdir -p ~/m6-cd
sudo mount -o ro /dev/sr0 ~/m6-cd
ls ~/m6-cd/lab-files
```

Use **one** source below, according to the successful mount:

```bash
# Share route:
bash ~/m6-transfer/automation/prepare-workspace.sh
```

```bash
# Data-CD route instead:
bash ~/m6-cd/automation/prepare-workspace.sh
```

Expected: a new `/home/seed/issd-member6`, all four original hashes OK, no CR line endings, native filesystem, and GCC found. The helper refuses an existing workspace; if one already exists, send its listing/diff rather than overwriting it. It copies the original C/shell files and supplemental checks; it does not compile or run the race.

```bash
cd ~/issd-member6/lab-files
pwd
df -T .
ls -l
sha256sum -c SOURCE_SHA256SUMS
bash ../automation/check-environment.sh
```

Send output/errors. Work only in this native path. A `vboxsf`, network, container or unexpected filesystem stops the workflow.

## 3. Start a real terminal transcript and build — S03

**MANUAL ACTION REQUIRED — VM**

Start a uniquely named terminal recording; `script` records the real displayed terminal stream. Ordinary password prompts disable input echo; do not place passwords in commands.

```bash
cd ~/issd-member6/lab-files
LOG="../evidence/logs/session-$(date -u +%Y%m%dT%H%M%SZ)-$$.typescript"
test ! -e "$LOG" && script -q -f "$LOG"
```

You should be at a fresh shell prompt in the same directory. Run:

```bash
cd ~/issd-member6/lab-files
bash ../automation/check-environment.sh
sha256sum -c SOURCE_SHA256SUMS
bash build.sh
ls -l cow_attack cow_control
file cow_attack cow_control
nl -ba cow_attack.c | sed -n '31,61p'
nl -ba cow_attack.c | sed -n '100,152p'
```

Expected: compiler succeeds, seed-owned normal 0755 ELF 32-bit binaries, no Set-UID. Capture **M6-S03-code-build.png**, plus a/b code views as needed. The actual build output and any compiler error must be retained.

Read the reference already copied to native storage:

```bash
cd ~/issd-member6/reference
unzip -l Labsetup.zip
unzip -n Labsetup.zip
find . -name cow_attack.c -print
cd ~/issd-member6/lab-files
```

This original source stays under `reference/`; the assignment adaptation stays under `lab-files/`. Inspect the found source and the five-page `Dirty_COW.pdf`.

## 4. Dummy baseline and normal COW — S04/S05

First inspect `/zzz`:

```bash
ls -l /zzz
```

Expected on the clean image: no such file. If present, determine its origin before replacing it.

**MANUAL ACTION REQUIRED — VM: administrative target setup**

Only after confirming it is absent or a known earlier lab target:

```bash
sudo sh -c 'printf "111111222222333333\n" > /zzz'
sudo chown root:root /zzz
sudo chmod 0644 /zzz
id
cat /zzz
ls -l /zzz
echo 99999 > /zzz
cat /zzz
sha256sum /zzz
```

Expected: the ordinary `echo` redirection fails with **Permission denied**; root:root 0644 and the full original 19-byte file remain. Capture **M6-S04-dummy-baseline.png**. If the ordinary write works, **stop**; this is not a valid baseline.

Save the first baseline without overwriting an earlier record, then run the control:

```bash
(set -C; sha256sum /zzz > ../provenance/dummy-normal.sha256)
./cow_control
cat /zzz
sha256sum -c ../provenance/dummy-normal.sha256
```

Expected: `Private memory` shows `111111******333333`; `Backing file` and the fresh `cat` show `111111222222333333`; the saved hash check is OK. Capture **M6-S05-normal-cow.png** and record the actual strings/hash. Explain that the control uses `PROT_READ | PROT_WRITE` and `MAP_PRIVATE`, while the attack uses a read-only mapping and `/proc/self/mem`.

## 5. Task 1 bounded trial — S06/S07

**MANUAL ACTION REQUIRED — VM: start the supplied experiment in the verified guest**

```bash
cd ~/issd-member6/lab-files
id
bash ../automation/trial-with-evidence.sh dummy 30 task1-run1
cat logs/task1-run1-summary.txt
cat logs/task1-run1-program.txt
```

The supplementary wrapper visibly invokes **`bash run_trial.sh dummy 30 task1-run1`**; the original implementation performs the race. It records owner/mode/size before and after and runs a whole-file verifier. Capture **M6-S06-task1-running.png** during or immediately after this bounded run, as allowed by the repository. If captured afterward, caption it as a completed trial rather than claiming that a process was still alive.

```bash
diff -u logs/task1-run1-before.txt logs/task1-run1-after.txt
cat /zzz
ls -l /zzz
sha256sum /zzz
python ../automation/verify-trial.py dummy logs/task1-run1 --live
```

Expected full result: `111111******333333\n`, exactly six replacement bytes, unchanged length, root:root 0644, live file matching the retained after-copy. Capture **M6-S07-task1-result.png** with the elapsed time and before/after evidence visible.

**If unchanged/partial/error:** preserve output and files, check `program.txt`, the exact running kernel/package, baseline, ordinary identity and compiler. A wrapper returning 0 or reporting a change does not establish complete success. The verifier's `unchanged`, `partial-or-unexpected-change`, nonzero exit or missing-artifact error must be recorded. Do not proceed as if Task 1 succeeded.

For a known lab reset, first wait for the wrapper to finish. A long direct run can be stopped with **Ctrl+C in its own terminal**; then check:

```bash
pgrep -x cow_attack
```

Expected: no output, exit 1. If a PID remains, inspect it with `ps -p PID -o pid,ppid,ruid,euid,args` and stop only that confirmed lab process before reset. A `pgrep` option/error is not “no process.”

```bash
sudo sh -c 'printf "111111222222333333\n" > /zzz'
sudo chown root:root /zzz
sudo chmod 0644 /zzz
```

Retry under a new label such as `task1-run2`; preserve the first trial. These sudo writes are **reset**, never attack proof.

## 6. Charlie normal login and immutable baseline — S08

**MANUAL ACTION REQUIRED — VM: account creation and password entry**

```bash
getent passwd charlie
```

Expected: absent. If present, stop and inspect its origin. For the new lab-only account:

```bash
sudo adduser charlie
grep '^charlie:' /etc/passwd
id charlie
su - charlie
```

Choose/enter a lab-only charlie password directly in the VM and leave optional personal fields blank. In the actual successful charlie login:

```bash
id
id -u
exit
```

Back at seed:

```bash
id
```

Expected: charlie's fresh login has its actual nonzero UID; the final shell is seed. Save **M6-S08-a-charlie-baseline.png**. If authentication fails, preserve and resolve that error before taking a baseline or attacking.

Create the repository's root-held backup **once, after adduser and the successful normal login**:

```bash
sudo test ! -e /root/issd-member6-passwd.normal && sudo cp -a /etc/passwd /root/issd-member6-passwd.normal
sudo ls -l /root/issd-member6-passwd.normal
sudo cmp /etc/passwd /root/issd-member6-passwd.normal
sha256sum /etc/passwd
ls -l /etc/passwd
test -w /etc/passwd && echo 'Unexpected: writable' || echo 'seed cannot write /etc/passwd'
```

Stop on an existing backup or unexpected comparison. Preserve the backup; do not overwrite it after a trial. Capture **M6-S08-b-charlie-baseline.png** with backup comparison and mode/write check.

Save the actual non-secret baseline records without overwriting any existing file:

```bash
cd ~/issd-member6/lab-files
(
  set -eC
  sha256sum /etc/passwd > ../provenance/passwd-normal.sha256
  grep '^charlie:' /etc/passwd > ../provenance/charlie-normal.txt
  awk -F: '$3 == 0 {print $1 ":" $3}' /etc/passwd > ../provenance/uid0-normal.txt
)
```

Expected: all three files created from the **normal** state. No password or shadow content is needed. Now create **M6-charlie-normal-ready** using [the exact host snapshot procedure](ARCH_HOST_SETUP.md#4-snapshots). Stop experiment processes and end/flush the transcript before shutting down. Resume a **new unique transcript** after reboot. Send snapshot confirmation before Task 2.

## 7. Task 2 UID overwrite — S09

**MANUAL ACTION REQUIRED — VM: ordinary-seed bounded trial**

```bash
cd ~/issd-member6/lab-files
id
bash ../automation/trial-with-evidence.sh passwd 30 task2-run1
cat logs/task2-run1-summary.txt
cat logs/task2-run1-program.txt
grep '^charlie:' /etc/passwd
diff -u logs/task2-run1-before.txt logs/task2-run1-after.txt
python ../automation/verify-trial.py passwd logs/task2-run1 --live
```

This invokes the unchanged `bash run_trial.sh passwd 30 task2-run1`. It discovers the actual UID; no 1001 assumption is made. Expected: **only** charlie's UID digits become an equal number of zeroes; all other file bytes and the mode/owner remain unchanged. Save **M6-S09-task2-uid-change.png**, with suffixes for a readable diff/summary if necessary.

If unchanged, partial or otherwise incorrect: record the actual result, preserve the files, stop processes and restore the original normal baseline before another uniquely labelled attempt. An exact file change still does not prove a successful login.

## 8. Fresh non-sudo privilege verification — S10

**MANUAL ACTION REQUIRED — VM: authenticate as charlie**

From seed, after the exact-file check and stopped-attacker check:

```bash
pgrep -x cow_attack
grep '^charlie:' /etc/passwd
su - charlie
```

Enter the same lab-only password. In the resulting login:

```bash
id
id -u
whoami
echo "Proof shell PID=$$"
```

Expected for a successful experiment: numeric UID **0**. `whoami` may resolve that UID to `root`; GID can remain charlie's ordinary group. Capture **M6-S10-task2-root-proof.png** showing the preceding **`su - charlie`**, actual identity commands and result. Send the output/capture and proof-shell PID. Never substitute `sudo su`, a root-run attack or a shell prompt alone.

After capturing, **only if the login actually opened a child shell**, type `exit` once. Then run `id` and confirm seed. If authentication failed, you are already at seed; preserve the failure and do not blindly `exit` the parent session.

## 9. Restore and verify a new normal login — S11

**MANUAL ACTION REQUIRED — VM: close every test root shell, then restore**

```bash
pgrep -x cow_attack
pgrep -x su
id
sudo cp -a /root/issd-member6-passwd.normal /etc/passwd
sudo cmp /etc/passwd /root/issd-member6-passwd.normal && echo 'Normal-account baseline restored'
sha256sum -c ~/issd-member6/provenance/passwd-normal.sha256
grep '^charlie:' /etc/passwd
su - charlie
```

Run the restore only when both process checks show none and your shell is seed. In the fresh restored charlie login:

```bash
id
id -u
exit
```

Back at seed, run `id`. Expected: charlie's **original** nonzero UID and the exact saved normal record. Capture **M6-S11-account-restored.png**. Changing `/etc/passwd` does not revoke existing process credentials; the previous UID-0 shell must already have ended.

## 10. Optional S12 and final cleanup — S13

S12 is **not performed; discussion only** unless a separate patched VM is actually tested. The primary historical VM is not upgraded for this comparison. A bounded failed run on a different kernel would need valid setup, actual package/advisory evidence and its own results.

**MANUAL ACTION REQUIRED — VM: clean the known lab target and verify**

After all test logins/races have ended:

```bash
cd ~/issd-member6/lab-files
pgrep -x cow_attack
pgrep -x su
id
sudo cmp /etc/passwd /root/issd-member6-passwd.normal
grep '^charlie:' /etc/passwd
sudo rm -f /zzz
bash ../automation/check-cleanup.sh
ls -ld ~/issd-member6 ~/issd-member6/lab-files
find ../evidence ../provenance logs -maxdepth 2 -type f -print
```

Remove `/zzz` only because its origin was established at S04 as this lab's dummy. Keep the normal charlie account and its post-adduser baseline for reproducibility. The checker compares the complete file/hash/record and original UID-0 list, checks no attack/su/privileged shell remains, verifies `/zzz` absence and ordinary executable modes. If it reports a privileged service shell, inspect and explain it; do not terminate unrelated services or claim cleanup while a test shell remains.

Unmount any successful input mount after copying/using it:

```bash
# Run only for the mount route actually used:
sudo umount ~/m6-transfer
# Or, for the data-CD route:
sudo umount ~/m6-cd
```

Capture **M6-S13-cleanup.png**, with extra images for file inventory if needed. Send the actual cleanup output. This is required even after a failed/partial experiment that modified a target.

## 11. Export genuine artifacts before rollback

First `exit` the **script recording shell** to close its transcript, then remain in the ordinary outer seed shell. Do not export an actively changing transcript.

```bash
cd ~/issd-member6/lab-files
bash ../automation/export-evidence.sh session-1
```

Expected: a new `~/issd-member6/exports/member6-session-1.tar.gz` and matching `.sha256`. Use `session-2` for another export; preserve earlier exports.

**MANUAL ACTION REQUIRED — VM: mount the dedicated output share**

```bash
mkdir -p ~/m6-export
sudo mount -t vboxsf -o uid=$(id -u),gid=$(id -g) M6export ~/m6-export
cp -n ~/issd-member6/exports/member6-session-1.tar.gz ~/m6-export/
cp -n ~/issd-member6/exports/member6-session-1.tar.gz.sha256 ~/m6-export/
sudo umount ~/m6-export
```

Send the host filenames now present under `Member6/evidence/incoming/`. The agent will verify checksums, inspect the real logs/images, select evidence using the repository names, and complete the report/presentation from the observations. If the old share fails, retain the archive inside the VM and send the error for another transfer method. **Do not roll back before the export is verified on the host.**

The final cleaned VM can be shut down normally after evidence transfer. Rehearsal will reset only the documented targets, use fresh log labels, and repeat cleanup.
