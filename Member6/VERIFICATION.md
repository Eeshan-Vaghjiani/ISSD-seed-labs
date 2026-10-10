# Member 6 — preparation and verification status

## Fresh verification — 9 October 2026

Fresh guest S02/S03 captures now establish Ubuntu 12.04.2, i686/32-bit, kernel `3.5.0-37-generic` / package `3.5.0-37.58~precise1` from `linux-lts-quantal`, GCC 4.6.3, seed UID/GID 1000 and the native ext4 workspace. Four guest source hashes match the host originals. `bash build.sh` returned 0 and produced seed-owned 0755 ELF32 binaries. Both source-worker views were captured and reviewed. See the [fresh image review](evidence/incoming/opus-fresh-20261008/EVIDENCE_REVIEW.md) and [current checkpoint table](evidence/incoming/opus-fresh-20261008/README.md).

The guest guard and Python 2.7.3 verifier parse returned 0; the timeout compatibility check returned 124. Following the user's authentication, both transfer mounts were verified. S01's complementary CPU/disk images are now reviewed. S04/S05 establish the denied ordinary write and unchanged backing file under normal COW. The Task 1 trial `fresh-t1-01` produced the exact 19-byte replacement with root:root 0644 retained; the live guest verifier and independent exported-file verifier both passed. Its 30-second bound produced a measured 0 integer elapsed seconds, without any finer runtime or attempt-count claim. See `submission/RESULTS.md` and the fresh S06/S07 captures.

Charlie was created with UID 1001 / GID 1002, and an ordinary non-sudo login was verified before the protected full-file baseline and powered-off `M6-charlie-normal-ready` snapshot. The sole Task 2 trial `fresh-t2-01` changed only the same-width UID field to `0000`, retaining root:root 0644 and 2040 bytes. Live and offline verification passed. One authentication attempt failed; the retry succeeded with actual UID 0, GID 1002, `whoami` root and proof PID 3392. That shell exited before exact full-file restoration; a new charlie login then reported UID 1001 and exited to seed.

The complete cleanup checker returned 0, finding no attacker/wrapper/control/su/root shell, only the original `root:0` entry, no `/zzz`, matching account baseline and ordinary 0755 binaries. Both native transcripts are closed and hash-verified on the host. The 46-file final archive passed source, transcript, trial-artifact and complete restored-file checks. The input share was unmounted; a password-required final output-share unmount is retained as a failure, followed by normal guest shutdown. VirtualBox confirms the powered-off final state, disconnected network cable and both retained snapshots. See `provenance/final-export-verification.json` and `provenance/final-powered-off-state.json` in the fresh folder.

All required checkpoints are complete. **S12 is not performed; discussion only.** The original preparation sections below describe their dated state, not outstanding practical work. The user approved the generic **Member 6 — ISSD** cover; course deadline/format/identity/speaking allowance and future spoken rehearsal/upload remain human follow-up.

## Historical handoff — 8 October 2026

The host reboot and guest boot succeeded. Actual guest checks established Ubuntu 12.04.2, i686, kernel 3.5.0-37-generic / package 3.5.0-37.58~precise1, GCC 4.6.3 and seed UID/GID 1000. Source transfer onto ext4 and the guest build passed; both binaries were seed-owned 0755 ELF32. Actual records are in `evidence/incoming/M6-S02-environment.log`, `M6-preflight-extra.log`, `M6-transfer-native.log` and `M6-S03-build.log`.

The user stopped the prior workflow before any normal-COW control, dummy-file attack or account experiment and requested fresh screenshots with Opus 5.5. Follow [OPENCODE_HANDOFF.md](OPENCODE_HANDOFF.md) and the [fresh-run prompt](OPUS_5_5_FRESH_RUN_PROMPT.md). The new screenshot folder is `evidence/incoming/opus-fresh-20261008/`. Reverify the current VM; earlier captures are not this new run's evidence.

## Historical execution preparation — 7 October 2026, before first boot

The full current audit is [EXECUTION_STATUS.md](EXECUTION_STATUS.md); the completed pre-boot checks and retained records are in [PREPARATION_VERIFICATION.md](PREPARATION_VERIFICATION.md). The repository audit covered all 616 original tracked files, with no detected structural/integrity errors. All Member 6 requirements/source and the relevant Member 5 coursework, finished documents, evidence/provenance and helper code were reviewed.

* Reused and verified the official-checksum local `SEEDUbuntu12.04.zip`: MD5 match, SHA-256 recorded, every ZIP entry CRC checked; extracted the split VMDK outside the repository.
* Created the separate 32-bit `ISSD-Member6-SEED12` profile with 2048 MB, 2 CPUs, VMSVGA 64 MB/3D-off, matching LSI Logic disk controller, disconnected NAT and transfer shares.
* Took powered-off `M6-clean-SEED12` before first boot. Actual command/configuration output is retained in `evidence/host/`.
* Found the host boot blocker: Arch runs 7.2.8 while installed headers/DKMS VirtualBox modules target 7.2.9. No guest has booted; actual kernel, package, GCC, control, attack, login and cleanup checks remain pending.
* Added source-hash, guest-boundary, metadata, whole-file comparison, raw-frame capture and evidence-export helpers. The four supplied C/build/trial files remain byte-identical to the audited commit. Host shell/Python syntax checks, in-memory comparison checks and actual Arch-host rejection passed. Guest runtime compatibility is still unverified.
* Added the Arch setup companion, exact guest session/capture procedure, explicit expected/actual results ledger and presentation/demo notes. The original report/template/plan remains the basis for final evidence-led documents.

**No M6 screenshots or experimental results have been fabricated or collected.** A template/host inventory is not guest proof. Follow the manual reboot handoff in [ARCH_HOST_SETUP.md](ARCH_HOST_SETUP.md), then verify the actual guest before any trial.

## Historical preparation review

Research/check date: **29 September 2026**.

## Completed during preparation

* Reviewed the lecturer's links and the PDF's Member 6 responsibilities.
* Read the official Dirty COW lab page, complete upstream task text and original `cow_attack.c`.
* Read the five-page historical SEED Ubuntu 12.04 VM manual: it identifies Ubuntu 12.04, original kernel 3.5.0-37-generic, seed/dees account and historical VM configuration.
* Confirmed the official page explicitly requires the old SEED 12.04 image despite the `Labs_20.04` URL.
* Checked Ubuntu's CVE-2016-5195 advisory, including package-specific fix versions and backport considerations.
* Consulted memory-mapping/discard documentation to distinguish normal COW, read-only pointers and the `/proc/self/mem` write path.
* Mapped both official tasks and every Member 6 division item to the guide, report, presentation and evidence checklist.
* Reviewed the C source for bounded mapping search, exact account-prefix matching, same-length UID replacement, address-width handling, checked setup calls and ordinary-user execution.
* Checked `build.sh` and `run_trial.sh` individually with `bash -n` using Git for Windows Bash; both passed.
* Generated and reopened all three Word documents using `python-docx`, with matching paragraph/table counts and closed Markdown code fences.

## Not executed here

* No SEED Ubuntu 12.04 guest was installed or booted by the preparation agent.
* No Linux GCC compilation or C runtime verification was performed here. The host's GCC targets Windows, which cannot validate Linux COW/mmap/proc semantics.
* No dummy-file exploitation, account overwrite, root login or patched-kernel comparison is claimed.
* The monitor's process stopping and exact exploit behaviour must be verified during the documented VM trials.
* Word documents have been library-reopened, not visually paginated in Microsoft Word. Check page breaks, image placement and long commands when preparing the final submission.

## Checks identified during the original preparation

1. Confirm actual image/kernel/architecture and build with Linux GCC.
2. Verify ordinary dummy writes are denied and normal private COW leaves the backing file unchanged.
3. Observe the exact Task 1 replacement, retain failed/partial attempts and unique run logs.
4. Verify charlie starts with a normal UID, back up after its creation, then test Task 2.
5. Validate only the intended UID field changes and a fresh non-sudo login has UID 0.
6. Restore normal UID, close privileged sessions and confirm no attacker process remains.
7. Label the patched comparison accurately as performed or discussion-only.

The public source links are research references. The old VM image itself was not downloaded or checksum-tested here; the guide instructs you to verify your download. Deadlines, report format and personal speaking time remain to be confirmed because they are absent from the supplied course material.
