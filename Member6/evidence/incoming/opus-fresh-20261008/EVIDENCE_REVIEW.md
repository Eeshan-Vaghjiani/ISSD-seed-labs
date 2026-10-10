# Fresh Member 6 screenshots — reviewed observations

Experiment/review date: **9 October 2026**. The selected set contains **18 fresh guest captures and three user-supplied host views**, covering all required checkpoints. Guest PNG hashes are checked against their original capture sidecars. Review observations for S02–S07 are retained in the earlier review JSONs; S08–S13 and the final login/cleanup observations are recorded below and in `provenance/screenshot-review-20261009-task2.json`. S12 is **not performed; discussion only**.

| Checkpoint | Image | ACTUAL | Verification |
|---|---|---|---|
| S01 | `M6-S01-vm-setup.png`, `M6-S01-c-vm-setup.png`, `M6-S01-d-vm-setup.png` | VM name, Ubuntu 12.04 32-bit profile, 2048 MB, 2 CPUs, and SEEDUbuntu12.04.vmdk under M6-SCSI are visible across the three views. | Complete checkpoint. The CPU/disk images are user-supplied region captures; the disk location text is truncated, with the full parent/differencing chain established by host provenance. |
| S02 | `M6-S02-environment.png` | seed UID/GID 1000; Ubuntu 12.04.2 LTS; kernel `3.5.0-37-generic`; i686; 32 bits; kernel package `3.5.0-37.58~precise1`; GCC 4.6.3. | Fresh commands and outputs are readable in the real Ubuntu terminal. |
| S02 | `M6-S02-b-environment.png` | Required tools are present; kernel package architecture/source is `i386 linux-lts-quantal`; DMI says VirtualBox; workspace is `/home/seed/issd-member6/lab-files` on ext4. Both transfer directories are not mountpoints. | Native execution location established. The unmounted export directory has not been used as a share. |
| S03 | `M6-S03-code-build.png` | Four source checks pass. Sources are seed-owned 0644. `bash build.sh` returns 0 and produces seed-owned 0755 ELF32 binaries. | Ordinary identity and build command are visible; no compiler error is shown. |
| S03 | `M6-S03-b-code-build.png` | Supplied source opens the target read-only, uses `PROT_READ` with `MAP_PRIVATE`, converts the memory address and starts two workers. | Readable, numbered excerpts from the actual guest source. |
| S03 | `M6-S03-c-code-build.png` | Discard worker repeats `MADV_DONTNEED`; writer opens `/proc/self/mem` and calls `pwrite`, with error checks. | Actual source explains the two paths involved in the race. |
| S04 | `M6-S04-dummy-baseline.png` | Root:root 0644, 19-byte original file; seed's ordinary redirection is denied with exit 1; content and SHA-256 remain unchanged. | Correct ordinary write-protection baseline. |
| S05 | `M6-S05-normal-cow.png` | Private memory changes to stars; backing file stays original; fresh read/hash and complete baseline comparison pass. | Normal private COW does not change the backing file. |
| S06 | `M6-S06-task1-running.png` | `fresh-t1-01` finishes with a content change, 30-second limit and 0 integer elapsed seconds; ordinary identity, mapping details and diff are visible. | This is a **completed-trial** capture, not evidence that the process was still running at capture time. |
| S07 | `M6-S07-task1-result.png` | Exact full replacement and fresh file read; root:root 0644, 19 bytes; expected-byte comparison returns 0. | Live guest and exported artifact verification both pass. |
| S08 | `M6-S08-charlie-baseline.png` | Actual record `charlie:x:1001:1002:,,,:/home/charlie:/bin/bash`; fresh non-sudo login gives UID 1001 / GID 1002, whoami charlie; exit returns to seed. | Normal account authentication precedes protected backup and attack. |
| S08 | `M6-S08-b-charlie-baseline.png` | Root-held backup is 2040 bytes, root:root 0644; complete `cmp` returns 0; saved normal hash passes; seed cannot write the file. | Exact post-creation baseline. Powered-off prepared snapshot is separately documented. |
| S09 | `M6-S09-task2-uid-change.png` | Ordinary seed runs `fresh-t2-01`; 30-second limit, 0 integer elapsed seconds; UID field `1001` → `0000`; offset 2002, width 4. | Completed-trial capture; sole fresh Task 2 exploit. The summary is not itself login proof. |
| S09 | `M6-S09-b-task2-uid-change.png` | Full diff contains only the charlie UID-field replacement; live file matches retained after-copy; root:root 0644, 2040 bytes. Numeric UID-0 query finds root and charlie. | Live/offline full-byte comparisons agree. The two original zero digits remain zero. |
| S10 | `M6-S10-task2-root-proof.png` | First `su - charlie` fails; second succeeds. `id` reports UID 0 / GID 1002, `id -u` = 0, `whoami` = root, proof-shell PID 3392. | Genuine fresh non-sudo privilege proof. Failure preserved; its cause is not established. Terminal background redraw is visible in the recording, not an edited result. |
| S10 | `M6-S10-b-proof-shell-exited.png` | Seed UID 1000 restored as caller; PID 3392 absent and `pgrep su` finds none, each exit 1. | Old privileged shell ended before restoration. The window title is not the numeric identity proof. |
| S11 | `M6-S11-b-baseline-restored.png` | Protected full-file comparison succeeds, saved hash is OK, original charlie record/UID and root:root 0644/2040-byte metadata return. | Restoration is exact, not a single-field visual check. |
| S11 | `M6-S11-account-restored.png` | New non-sudo login reports UID 1001 / GID 1002 and whoami charlie; exit returns to seed UID 1000. | Actual fresh ordinary authentication after full restoration. |
| S13 | `M6-S13-cleanup.png` | No attacker/control/su matches; proof PID absent; normal hash and UID 1001; only root:0; `/zzz` removed; binaries seed-owned 0755; input share unmounted. | Supplemented by successful full cleanup checker, closed transcript/export verification and normal powered-off state. |

## Captions ready for the report

**S02 — Guest environment.** The ordinary seed account reported UID 1000 on Ubuntu 12.04.2, using the 32-bit `3.5.0-37-generic` kernel and GCC 4.6.3. The package check returned `3.5.0-37.58~precise1`. These are the running guest's values, rather than values inferred from the VirtualBox profile.

**S02b — Tools and native workspace.** The required tools were available, and the workspace was on ext4. The kernel package belongs to the `linux-lts-quantal` family. The two transfer directories were unmounted at this checkpoint, so evidence export still required mounting the share.

**S03 — Source verification and build.** All four supplied source hashes matched. Running `bash build.sh` as seed returned 0 and produced ordinary 0755, 32-bit executables owned by seed. The attack executable has no Set-UID bit.

**S03b/c — Mapping and worker code.** The target is opened read-only and mapped privately with `PROT_READ`. One worker repeatedly discards mapping state with `MADV_DONTNEED`; the other writes to its own process-memory interface. The `pwrite` offset is a virtual address in the process, rather than an ordinary write offset into the protected file.

**S04 — Ordinary write protection.** `/zzz` contained the original 19-byte sequence and was root-owned with mode 0644. Seed's `echo 99999 > /zzz` failed with Permission denied and exit 1. A fresh read and matching hashes showed that the failed write left the file intact.

**S05 — Normal copy-on-write.** The control printed `111111******333333` from its private memory, while the backing file still contained `111111222222333333`. The saved hash passed and a complete byte comparison returned 0. The control uses a writable private mapping and a direct memory write.

**S06/S07 — Verified Task 1 result.** The ordinary-seed trial `fresh-t1-01` changed the full backing file to `111111******333333\n`. The file remained root:root 0644 and 19 bytes long. The wrapper recorded 0 integer wall seconds within a 30-second limit; this does not mean zero execution time. The fresh expected-byte comparison and both live/offline artifact checks passed. S06 was captured immediately after the trial completed.

## Separate detailed records

The first guest transcript, `/home/seed/m6-fresh-20261009-1946.typescript`, was closed before the prepared snapshot. Process absence and matching hashes verified the 26,479-byte record despite its missing completion footer. The initial footer assertion failure is retained in the verification record. The second, `fresh-task2-20261009.typescript`, was closed after cleanup; its native and exported 13,899 bytes match SHA-256 `0f859b0c502405232fd771d15d84bd97990c558c836612d507801520b0d546cf`. Both originals are retained in `logs/` and the guest archives. The Task 2 transcript has been reviewed through authentication, restoration, fresh ordinary login and cleanup.

Fresh public input actions are copied, with their original timestamps, in `provenance/console-actions-through-s03-20261009.jsonl`. Successful input delivery is not used as proof of command success; the actual framebuffer output was inspected separately.

Supporting diagnostic frames in `provenance/` retain the initial terminal, display setup, full source hashes, runtime checks and current target state. They are not additional completed lab checkpoints. The guest guard and Python verifier parse returned 0; the timeout compatibility check returned 124 as expected. `/zzz` was absent, `getent passwd charlie` returned 2, and the exact charlie-record grep returned 1. No attack or su process was found in the earlier process checks; the trial log directory was empty. `sudo -n true` returned 1 with an actual password-required message.

Those initial diagnostic frames describe the state **before** Task 1. The subsequent control and dummy race are now complete, as established above. Closed `fresh-control-01.txt` and `fresh-t1-01-*` artifacts were copied through the verified writable share and passed offline verification. `logs/fresh-t1-01-verification.log` preserves the live guest check and its JSON output; `provenance/fresh-t1-01-offline-check.json` preserves the separate host check. Neither check reads a host lab target.

After Task 1, another absent-charlie check preceded `adduser`. Creation and interactive ordinary-login verification completed before the protected baseline. The dummy was reset to its original hash and `M6-charlie-normal-ready` was taken powered off. Post-boot checks re-established the normal account and source state before Task 2. One authentication attempt failed after the exact file change; a subsequent non-sudo login succeeded. The successful UID-0 shell was exited before exact restoration and a new UID-1001 login.

Final export checksum, every source hash, the whole restored file and the cleanup log passed host verification. The input share was explicitly unmounted. A password-required failure prevented an explicit output-share unmount; the subsequent normal guest shutdown closed the remaining mount. The VM is powered off with its cable disconnected and both snapshots retained. This state is documented in `provenance/final-powered-off-state.json`.

## Presentation derivatives

Selected originals are copied byte-for-byte into `Member6/submission/evidence/`. Any report/slide crop is labelled as a readability excerpt, with its source, crop rectangle and hashes in `submission/figures/CROP_MANIFEST.json`; contained pixels are unchanged. Native VirtualBox recordings of the Task 2 trial and login are retained here. Presentation video excerpts identify any omitted waiting intervals and are not represented as a continuous live classroom run. No oral rehearsal or classroom demonstration has yet been performed.
