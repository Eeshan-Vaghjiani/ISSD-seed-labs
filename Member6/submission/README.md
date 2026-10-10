# Member 6 — finished report, presentation and demonstration pack

**Both official Dirty COW tasks, fresh non-sudo UID-0 authentication, exact restoration and final cleanup are complete and verified.** Experiments took place on **9 October 2026** in the separate SEED12 VM. The user approved the **Member 6 — ISSD** cover.

## Open these

| Deliverable | Use |
|---|---|
| **[REPORT.pdf](REPORT.pdf)** / [REPORT.docx](REPORT.docx) / [REPORT.md](REPORT.md) | Completed 16-page report: the template's ten sections, actual results, 19 captioned figures, limitations, references and assistance disclosure |
| **[MAIN_PRESENTATION.pptx](MAIN_PRESENTATION.pptx)** / [PDF](MAIN_PRESENTATION.pdf) | Editable 10-slide deck: six main slides plus four evidence/reference backups; notes embedded |
| **[LIVE_PREPARATION.pdf](LIVE_PREPARATION.pdf)** / [Markdown](LIVE_PREPARATION.md) / [Word](LIVE_PREPARATION.docx) | Existing VM state, exact start/preparation steps, presentation route, recovery and rehearsal |
| **[LIVE_COMMANDS.pdf](LIVE_COMMANDS.pdf)** / [Markdown](LIVE_COMMANDS.md) / [Word](LIVE_COMMANDS.docx) | One-page command sheet for the short live dummy demonstration and cleanup |
| **[LIVE_DEMO.pdf](LIVE_DEMO.pdf)** / [Markdown](LIVE_DEMO.md) / [Word](LIVE_DEMO.docx) | Full ordered preparation, normal-COW control, bounded live trial, recorded Task 2 transition and cleanup |
| **[SLIDE_NOTES.pdf](SLIDE_NOTES.pdf)** / [Markdown](SLIDE_NOTES.md) / [Word](SLIDE_NOTES.docx) | Speaker notes, terminal transitions and lecturer Q&A |
| **[video/TASK2_FALLBACK.mp4](video/TASK2_FALLBACK.mp4)** | Genuine **66.6-second** recorded Task 2 edit; [source intervals and original recordings](video/README.md) retained |
| [RESULTS.md](RESULTS.md) | Detailed EXPECTED / ACTUAL / EXPLANATION ledger, timings, exact hashes and authentication failure |
| [BUILD_VERIFICATION.md](BUILD_VERIFICATION.md), [READINESS_REVIEW.md](READINESS_REVIEW.md) | Completed package checks, content review and precise remaining human actions |

The presentation's live transition is **slide 4 → LIVE_DEMO Part 1**. Prepare Part 0 beforehand; slide 5 uses recorded account evidence; complete Part 3 afterward. The suggested 5–7-minute slot is provisional. A spoken rehearsal and course upload remain human actions.

## CHECKPOINT | STATUS | EVIDENCE | VERIFICATION

Image names below are under [`evidence/`](evidence/); source provenance and diagnostic originals remain in the [fresh evidence directory](../evidence/incoming/opus-fresh-20261008/README.md).

| CHECKPOINT | STATUS | EVIDENCE | VERIFICATION |
|---|---|---|---|
| M6-S01 | Verified | `M6-S01-vm-setup.png`, c/d views | Separate SEED12 profile, 2048 MB, two CPUs and disk chain |
| M6-S02 | Verified | `M6-S02-environment.png`, b | Actual release, 32-bit architecture, kernel/package, GCC, seed UID and ext4 workspace |
| M6-S03 | Verified | `M6-S03-code-build.png`, b/c | Four original hashes, fresh build exit 0, seed-owned 0755 ELF32 binaries and actual source |
| M6-S04 | Verified | `M6-S04-dummy-baseline.png` | Root:root 0644, original 19 bytes, direct write denied and hash unchanged |
| M6-S05 | Verified | `M6-S05-normal-cow.png`; control log | Private memory changed; whole backing file and original hash unchanged |
| M6-S06 | Completed trial verified | `M6-S06-task1-running.png`; `fresh-t1-01` logs | Actual ordinary-seed command; 30-second limit, 0 integer elapsed seconds; image taken after completion |
| M6-S07 | Exact Task 1 success | `M6-S07-task1-result.png`; full copies/verifiers | Exact six-character replacement, fresh read, restrictive metadata and 19-byte length retained |
| M6-S08 | Verified | `M6-S08-charlie-baseline.png`, b; snapshot provenance | Fresh UID-1001/GID-1002 login, exact protected baseline and powered-off prepared snapshot |
| M6-S09 | Exact Task 2 file success | `M6-S09-task2-uid-change.png`, b; `fresh-t2-01` logs | Only same-width UID field `1001` → `0000`; other bytes and root:root 0644/2040-byte metadata retained |
| M6-S10 | Fresh UID-0 login verified | `M6-S10-task2-root-proof.png`, b; transcript/video | First authentication failed; retry non-sudo login returned UID 0; proof shell 3392 later absent |
| M6-S11 | Exact restoration verified | `M6-S11-account-restored.png`, b; full restored copy | Original whole-file hash/bytes restored; new non-sudo charlie login returned UID 1001; exit to seed |
| M6-S12 | Optional — not performed; discussion only | Report §7 | No patched-guest run, measurement or image claimed |
| M6-S13 | Cleanup/export verified | `M6-S13-cleanup.png`; cleanup and export records | No attacker/wrapper/control/su/test root shell, original UID-0 list, absent dummy, ordinary binaries; closed export verified |

## Task and environment summaries

**Task 1:** direct write denied; normal COW kept the backing file intact; the sole `fresh-t1-01` race produced exactly `111111******333333\n`. Full live and independent exported-file checks passed, retaining root:root 0644 and 19 bytes.

**Task 2:** the sole `fresh-t2-01` race changed charlie's four-character UID field **1001 → 0000**, retaining GID 1002 and every other file byte. After one preserved authentication failure, a fresh non-sudo login returned **UID 0**. The proof shell ended before exact full-file restoration; another fresh login returned **UID 1001**, then exited to seed.

Both original trials used a **30-second limit** and measured **0 integer elapsed seconds**. This is the wrapper's resolution, not instantaneous execution. No finer race runtime or kernel attempt count was measured.

**Environment:** Ubuntu **12.04.2**, **i686/32-bit**, kernel **3.5.0-37-generic**, package **3.5.0-37.58~precise1 / linux-lts-quantal**, GCC **4.6.3**, seed **UID/GID 1000**. All target/account operations ran in **ISSD-Member6-SEED12**, UUID **242db196-83e1-4b7a-9f0b-e399d6f8b9dc**, on native ext4. Arch handled orchestration, genuine captures and exported-artifact checks.

The final guest is **powered off normally**, with the network cable disconnected. Charlie remains ordinary UID 1001 / GID 1002; `/zzz` is absent. The protected baseline and both `M6-clean-SEED12` / `M6-charlie-normal-ready` snapshots are retained. M6pack was explicitly unmounted; a password-required final M6export unmount failed, after which normal shutdown closed remaining mounts. That failure remains documented.

## Supporting material

* `evidence/` — **21 byte-identical selected originals**, 18 guest framebuffers and three user-supplied host views; capture sidecars and `SELECTION.json`.
* `figures/` — **20 documented readability crops**, with exact original-pixel comparisons in `CROP_MANIFEST.json`; 19 are embedded in the report.
* `source/` — the four unchanged supplied lab files, `SOURCE_SHA256SUMS` and attribution.
* `automation/` — the actual guest verification/export helpers copied from the verified final archive.
* `logs/` — both closed raw transcripts, original trial/control logs, full before/after/restored files, metadata and cleanup output.
* `provenance/` — source/capture/snapshot/export and document verification. Raw diagnostic framebuffers referred to by these records are retained in the fresh evidence directory.
* `video/` — labelled H.264 fallback, its source/edit manifest and byte-identical uncut WebM originals.

The final **46-file guest export**, `member6-fresh-final-20261009.tar.gz`, remains in the fresh evidence directory with checksum:

```text
08fe8d346f51f506a6b205683ead027d031a7d9fca34839045af7595bbb35fa1
```

Earlier captures, preparation failures and original archives remain preserved. The directory suffix `20261008` is the requested destination, not the experiment date. `SHA256SUMS` inventories the finished submission files; see the build verification for the host check command.

## MANUAL ACTION REQUIRED — final review, rehearsal and submission

1. **HOST / course:** review the report and slides under the approved **Member 6 — ISSD** identity. Confirm any course-required personal/class/group/lecturer details, deadline/upload format and speaking allowance; these were not specified in the supplied materials.
2. **HOST → VM:** follow [LIVE_PREPARATION.md](LIVE_PREPARATION.md) to start the exact prepared VM, log in as seed, and complete `LIVE_DEMO` Part 0. Rehearse the slide-4 dummy demonstration, recorded Task 2 transition and cleanup; record your actual speaking time. Enter passwords directly in the VM.
3. **HOST / course:** after personal review, submit the required files through the course channel and deliver the presentation. No course upload or oral delivery has been performed automatically.

**Attribution:** Wenliang Du / SEED Labs, Copyright 2017, **CC BY-NC-SA 4.0**, retained for the task/exploit pattern. **Assistance:** GPT-6 Astra through OpenCode supported command delivery, genuine capture, verification and document preparation; the user supplied host views and performed interactive authentication. See `REPORT.md` for the full disclosure.
