# Member 6 — execution checkpoint audit

## Current fresh-run checkpoint — 9 October 2026

The fresh session read the complete saved prompt/specification, four supplied files, shared allocation and handoffs, and visually reviewed Member 5's actual setup/environment/result/cleanup images. The fresh capture directory was empty. Actual host preflight records and the **current complete M6 checkpoint table** are in [the fresh-run record](evidence/incoming/opus-fresh-20261008/README.md).

Arch runs `7.2.9-arch1-1`; VirtualBox is `7.2.20r175154`, with matching module vermagic. Fresh S02 establishes Ubuntu 12.04.2, i686/32-bit, kernel `3.5.0-37-generic`, package `3.5.0-37.58~precise1` / `linux-lts-quantal`, GCC 4.6.3 and seed UID 1000. The workspace is native ext4. S03 source hashes, ordinary build exit 0 and seed-owned 0755 ELF32 binaries are verified. The final VM is **powered off normally**, with its cable disconnected and both snapshots retained.

**Task 1 is now complete.** After the user's sudo authentication, the shares were mounted/verified and the absent dummy was created exactly. S04 shows the denied ordinary write; S05 shows private-only normal COW. `bash run_trial.sh dummy 30 fresh-t1-01` produced the exact full `111111******333333\n` backing file, retaining root:root 0644 and 19 bytes. The wrapper recorded 0 integer elapsed seconds. S06/S07, the live verifier and the exported-file offline check agree. No attack process remained. Nine guest screenshots and all three host S01 views have now been reviewed. See `submission/RESULTS.md` for hashes and interpretation.

**Task 2 and cleanup are complete.** S08 verifies the original UID-1001/GID-1002 login, protected exact backup and powered-off prepared snapshot. `fresh-t2-01` replaced only the four-character UID field with `0000`; live and offline full-file checks passed, retaining root:root 0644 and 2040 bytes. The 30-second bound recorded 0 integer elapsed seconds. A first authentication failed; a second fresh non-sudo login reported UID 0. Proof shell 3392 exited before exact restoration. A new charlie login returned UID 1001, then exited to seed. The cleanup checker returned 0 with no experiment/su/root shell, normal UID-0 list, absent dummy and ordinary binaries.

Both transcripts are closed/exported; the 46-file final archive and original sources are hash-verified. There are 21 selected originals and genuine native Task 2 recordings. See [RESULTS.md](submission/RESULTS.md) and [the submission package](submission/README.md). The user approved **Member 6 — ISSD** for the cover. Remaining human work is course-specific details, spoken rehearsal, final review and upload. **S12 is not performed; discussion only.**

The sections below retain the **8 October historical handoff**. Their pending statuses are superseded by this fresh-run completion and the linked current checkpoint table.

## Previous-session handoff — 8 October 2026

Status date: **8 October 2026**. **Assignment incomplete; previous execution stopped at the user's request after environment verification and build.** The host reboot blocker was resolved. The user requests a new Opus 5.5 session and a fresh screenshot set; see [OPENCODE_HANDOFF.md](OPENCODE_HANDOFF.md).

Pre-boot configuration/source/media checks passed and are retained in [PREPARATION_VERIFICATION.md](PREPARATION_VERIFICATION.md). Those are historical checks of the frozen input bundle. Subsequent work booted the VM and collected the actual environment/build records below. Reverify the live state for the fresh run.

## CHECKPOINT | STATUS | EVIDENCE | VERIFICATION

| CHECKPOINT | STATUS | EVIDENCE | VERIFICATION |
|---|---|---|---|
| Repository audit | **Complete** | [Audit](REPOSITORY_AUDIT.md), `evidence/host/repository-audit-20261007.json` | All 616 original tracked files inventoried; applicable format/syntax/integrity checks passed; complete M6 requirements read |
| Arch diagnosis | **Resolved on 7 October** | `evidence/host/host-inventory-post-reboot-20261007.json` | Running kernel and driver matched 7.2.9; VirtualBox successfully started the guest |
| Official image | **Verified and extracted** | [Host setup](ARCH_HOST_SETUP.md), host media provenance | Exact official MD5, local SHA-256 and all-entry ZIP CRC; split disk descriptor + 41 extents |
| Source transfer | **Completed in previous session** | `evidence/incoming/M6-transfer-native.log` | Four source hashes matched; destination `/home/seed/issd-member6/lab-files` on ext4; inspect current state before reuse |
| Clean snapshot | **Complete** | `evidence/host/vm-setup-20261007T181036Z.log` | `M6-clean-SEED12`, UUID `7ecb8a4e-7430-497d-8772-fe3317d43b30`, before first boot |
| **M6-S01** | **VM configured; screenshot pending** | Actual VM setup log; `M6-S01-*.png` not yet collected | Correct profile/resources/disk chain; needs readable host settings capture |
| **M6-S02** | **Previous environment verified; fresh capture requested** | `evidence/M6-S02-environment.png`, `M6-S02-b-tools.png`; `evidence/incoming/M6-S02-environment.log` | Ubuntu 12.04.2, i686, kernel 3.5.0-37-generic / package 3.5.0-37.58~precise1, GCC 4.6.3, seed 1000. The earlier `M6-S02-a-environment.png` is a failed input attempt. |
| **M6-S03** | **Previous guest build passed; fresh capture requested** | `evidence/incoming/M6-S03-build.log`; previous build/mapping/worker captures | Supplied build produced seed-owned 0755 ELF32 binaries; Python 2.7.3 parsed verifier; timeout test returned 124. New screenshot set must be independently reviewed. |
| **M6-S04** | **Not executed** | No dummy baseline evidence | Need exact root:root 0644 file, denied direct write, actual hash |
| **M6-S05** | **Not executed** | No control evidence | Need actual private output versus unchanged backing-file read/hash |
| **M6-S06** | **Not executed** | No actual trial log/capture | Need original bounded ordinary-user dummy race and real summary |
| **M6-S07** | **Not executed** | No Task 1 result | Need exact whole-file replacement, actual live read/hash and unchanged ownership/mode |
| **M6-S08** | **Not executed** | No charlie baseline/login/backup record | Need actual original UID/login and one-time post-adduser backup; prepared snapshot pending |
| **M6-S09** | **Not executed** | No account trial/diff | Need same-length UID-only change, full comparison and actual runtime |
| **M6-S10** | **Not executed** | No privilege proof | Need real fresh non-sudo `su - charlie` → `id -u` = 0 |
| **M6-S11** | **Not executed** | No restoration proof | Need exact normal file and fresh original-nonzero-UID login; end old root shells |
| **M6-S12** | **Optional — not performed; discussion only** | Countermeasure theory in existing report/plan | No empirical patched-VM outcome claimed |
| **M6-S13** | **Not executed** | No post-experiment cleanup proof | Need stopped processes/shells, normal baseline, absent `/zzz`, organised/exported artifacts |
| Report | **Structure/concepts prepared; actual findings pending** | Existing `REPORT_TEMPLATE.md`, [results ledger](submission/RESULTS.md) | Final report must be populated only from guest evidence |
| Presentation | **Notes/command sheet prepared; findings deck/rehearsal pending** | Existing plan, `submission/SLIDE_NOTES.md`, `submission/LIVE_COMMANDS.md` | Six-slide evidence order/Q&A prepared; no recorded demo or spoken rehearsal yet |

## TASK 1

* **Status:** not executed.
* **ACTUAL:** no `/zzz` baseline, control output, race result or trial duration has been observed in the VM.
* **Evidence:** none for S04–S07 yet; collection/verification helpers are prepared.
* **Remaining:** reverify current S02/S03 state and make fresh captures; establish baseline, run control and supplied bounded race, inspect exact backing file/metadata, retain all trials and screenshots.

## TASK 2

* **Status:** not executed.
* **ACTUAL:** charlie's UID and login state are unobserved; no account attack or restoration has run.
* **Evidence:** none for S08–S11 yet.
* **Remaining:** create/test normal account, preserve baseline once, take prepared snapshot, run UID-only experiment, authenticate without sudo for numeric privilege proof, exit all privileged shells and verify restoration.

## ENVIRONMENT

* **VM:** `ISSD-Member6-SEED12`, UUID `242db196-83e1-4b7a-9f0b-e399d6f8b9dc`; successfully booted in the previous session. Inspect its current state before acting.
* **Architecture observed:** `i686`, `getconf LONG_BIT` = 32.
* **Kernel observed:** `3.5.0-37-generic`; package `3.5.0-37.58~precise1`, i386, source `linux-lts-quantal`.
* **Other observations:** Ubuntu 12.04.2 LTS, GCC 4.6.3, seed UID/GID 1000, ext4 workspace, two CPUs. Configured RAM 2048 MB; guest `free -m` reported 2016 MB usable.
* **Networking:** NAT was initially disconnected for the lab. Later inspection found it connected and the guest at 10.0.2.15; the user now reports internet access. Reinspect for the new run.
* **OpenCode issue:** the official V2 installer has no Linux i686 target. Use the host OpenCode/Opus session to operate the required VM; do not substitute another guest architecture/kernel.

## Next manual handoff

1. Follow [OPENCODE_HANDOFF.md](OPENCODE_HANDOFF.md): open a new host OpenCode session, select Claude Opus 5.5 and give it the saved fresh-run prompt.
2. New screenshots belong in `evidence/incoming/opus-fresh-20261008/`, visible through the mounted guest path `/home/seed/m6-export/opus-fresh-20261008/`. Earlier captures remain previous-session records.
3. Verify current guest state and use explicit manual gates for passwords, host settings captures and any necessary snapshot recovery. No Task 1/2 success has yet been established by this agent.
4. Confirm course identity/deadline/format/speaking allowance, then complete the practical, evidence-led documents, timed rehearsal and course upload.

The snapshot is a verified **pre-execution rollback point**, not substitute evidence for S11/S13 cleanup. No assignment-complete claim is warranted at this checkpoint.
