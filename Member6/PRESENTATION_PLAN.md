# Member 6 — Dirty COW presentation and live demo

The completed deck, embedded notes, recorded fallback and exact rehearsal commands are in [submission/](submission/README.md). The main six-slide structure below is retained. Suggested length **5–7 minutes** remains provisional because the course allowance is unconfirmed; no spoken rehearsal duration has been measured.

## Slide 1 — what is Dirty COW? (40 seconds)

**Title:** Dirty COW — a kernel race that breaks file-write protection

Show:

* CVE-2016-5195, disclosed in 2016.
* Local unprivileged code races Linux copy-on-write handling.
* Files normally readable but not writable can be modified on affected kernels.

**Say:** “Member 5 showed an application race. This example is inside the kernel. Copy-on-write should isolate private changes from the original file. Dirty COW breaks that separation under a particular concurrent sequence.”

## Slide 2 — normal COW and attack mechanism (50 seconds)

Show the diagram from the guide and these three roles:

1. Main thread opens and privately maps the file read-only.
2. Write thread writes mapped memory through `/proc/self/mem`.
3. Discard thread repeatedly calls `MADV_DONTNEED`.

**Say:** “The program is writing its own memory interface, not opening the protected file normally for writing. The vulnerable kernel mishandles the race so that the backing file can change. A direct assignment to read-only memory is not the method used.”

## Slide 3 — environment and normal protection (45 seconds)

Insert M6-S01–S04 selectively. Show actual kernel, ordinary identity, `/zzz` permissions and denied ordinary write.

**Say:** “Although the website link includes 20.04, SEED explicitly requires the old 32-bit Ubuntu 12.04 VM for this lab. My running kernel was 3.5.0-37-generic, package 3.5.0-37.58~precise1 from linux-lts-quantal. This is a separate VM from the Member 5 lab. The attack executable has no Set-UID bit and runs without sudo.”

## Slide 4 — short live dummy-file demonstration (90 seconds)

Before your presentation slot:

* Restore/reset the known `/zzz` lab baseline to `111111222222333333`, mode 0644 root:root.
* Confirm no `cow_attack` process is running.
* Open the terminal in `~/issd-member6/lab-files` with large text.
* Select a fresh log label, for example `presentation-dummy-1`.
* Have your saved genuine Task 1 evidence ready if the race misses the short window.

Run:

```bash
id
ls -l /zzz
cat /zzz
echo 99999 > /zzz
./cow_control
cat /zzz
bash run_trial.sh dummy 15 presentation-dummy-1
cat /zzz
ls -l /zzz
```

Explain each result:

* Ordinary direct write is denied.
* Normal private-copy modification leaves the file intact.
* The vulnerable-kernel race may change the actual backing file to `111111******333333`.

**Say:** “This run is bounded to keep the presentation on time. If it does not succeed in this window, I will show the genuine recorded result and state its measured runtime.”

Do not change file permissions or use `sudo` to produce the expected result. If the live race fails, identify the saved result as recorded evidence.

## Slide 5 — account impact (50 seconds)

Show M6-S08–S10, particularly the exact diff and `su - charlie` → `id -u` result.

```text
charlie:x:1001:1002:...  ->  charlie:x:0000:1002:...
```

These are the actual fresh-run UID/GID values. Show the unchanged field width and full-file verification.

**Say:** “The same mechanism replaced only charlie's UID field. UID 0 confers root privilege, independently of the account name. The first authentication failed; a second fresh login without sudo produced numeric UID 0. After the proof shell exited, exact restoration and a new UID-1001 login passed.”

This is recorded Task 2 evidence unless you explicitly perform the full account experiment live. The small dummy target is the simpler live demonstration; completing the account task beforehand is still required.

## Slide 6 — countermeasures and takeaway (60 seconds)

Show:

* Patch the kernel and confirm the fixed kernel is booted.
* Maintain a supported OS and system updates.
* Limit unnecessary local access and execution of untrusted code.
* Monitor account integrity, unexpected UID-0 records and privileged sessions.

If you performed the optional patched comparison, show M6-S12 and actual result. Otherwise label this as a defence discussion, not a tested comparison.

**Say:** “The primary fix is in the kernel. File permissions were already restrictive; removing a Set-UID bit or enabling Member 5's symlink protection does not fix this flaw. Monitoring may reveal the account change or login, but cannot replace patching.”

**Final takeaway:** “Private memory changes must remain private; kernel races can undermine the account database even when application-level file permissions look correct.”

## Questions to practise

**Why does the URL say 20.04 while you use 12.04?** That is the website category. The lab page and task text explicitly require the old SEED 12.04 VM because later SEED images are patched.

**Does every Ubuntu 12.04 installation have Dirty COW?** No. Kernel updates/backports matter. Record the actual running kernel/package and use vendor information.

**Is this a remote attack?** No. The attacker needs local code execution. Another attack could provide that foothold, but that is not demonstrated here.

**What does `MAP_PRIVATE` mean?** Private modifications should not update the mapped file. It does not mean the application can normally bypass file write permissions.

**Why not write directly through the read-only pointer?** That normally faults. The exploit uses `/proc/self/mem` and a kernel race.

**What does `MADV_DONTNEED` do here?** It discards page state so subsequent access can repopulate/refault the mapping, racing the write/COW handling.

**Why are the two operations repeated?** Timing is probabilistic. Many concurrent operations increase chances of encountering the vulnerable interleaving.

**Why change 1001 to 0000 rather than 0?** An in-place overwrite must preserve the UID field's byte width to avoid leftover characters or damage to separators/other fields.

**Why not modify seed?** Charlie is a disposable lab account; altering seed affects other experiments and makes resets harder.

**Why does the user appear as root after `su - charlie`?** Both names now resolve to UID 0. Numeric identity is the evidence, not the shell prompt.

**Does restoring passwd end existing root sessions?** No. Existing processes retain their credentials; terminate those sessions as well.

**Does an unsuccessful 15-second run prove the kernel is safe?** No. It may reflect timing, setup errors or patching. Interpret it alongside successful setup and vendor patch evidence.

## Rehearsal checklist

* [ ] Confirm time allowance and who introduces/transitions to this segment.
* [ ] Insert actual environment, timings and screenshots.
* [ ] Build/check binaries before presentation; no compilation debugging during the slot.
* [ ] Reset dummy target with process stopped and choose a new log label.
* [ ] Explain normal COW before the attack result.
* [ ] Keep genuine Task 1/2 screenshots or a short video outside the VM.
* [ ] Distinguish recorded results from live output.
* [ ] Close root sessions, stop processes and reset after rehearsal.
