# Member 6 — verified fresh evidence set

**Both official tasks, fresh non-sudo UID-0 authentication, exact restoration and final cleanup are complete.** Experiments occurred on **9 October 2026**. The requested directory name `opus-fresh-20261008` is retained. Earlier-session captures/logs remain separate and have not been relabelled.

Start with [the completed results](../../../submission/RESULTS.md), [image review](EVIDENCE_REVIEW.md), and [submission package](../../../submission/README.md).

## Execution boundary and final state

All target/account operations and C programs ran inside **ISSD-Member6-SEED12**, UUID **242db196-83e1-4b7a-9f0b-e399d6f8b9dc**, in `/home/seed/issd-member6/lab-files` on native ext4. Arch-host tools delivered public commands, captured the real framebuffer and verified exported artifacts. Passwords were entered interactively by the user.

The fresh guest reported **Ubuntu 12.04.2 LTS, i686/32-bit, kernel 3.5.0-37-generic, package 3.5.0-37.58~precise1 from linux-lts-quantal, GCC 4.6.3, seed UID/GID 1000**. Configured resources were 2048 MB and two CPUs. All four supplied source hashes matched, and the ordinary fresh build returned 0 with seed-owned 0755 ELF32 binaries.

The VM is now **powered off normally**, after export verification. Its cable remains disconnected. Charlie remains an ordinary UID **1001**, GID **1002** account with its tested password and protected post-creation baseline. `/zzz` is absent. No attack/wrapper/control/su/test privileged shell remained at cleanup.

Both snapshots are retained:

* `M6-clean-SEED12` — `7ecb8a4e-7430-497d-8772-fe3317d43b30`, pre-execution.
* `M6-charlie-normal-ready` — `0d3457ab-f5ce-4606-8bee-1842809ca831`, taken powered off after ordinary login, protected backup comparison, stopped processes, dummy reset and verified pre-Task 2 export.

M6pack was read-only and M6export writable during verified transfers. M6pack was explicitly unmounted. The final noninteractive M6export unmount required a password and did not succeed; normal guest shutdown subsequently closed remaining mounts. See `provenance/final-powered-off-state.json`.

## CHECKPOINT | STATUS | EVIDENCE | VERIFICATION

| CHECKPOINT | STATUS | EVIDENCE | VERIFICATION |
|---|---|---|---|
| M6-S01 | Verified | `M6-S01-vm-setup.png`, c/d host views; host preflight | Separate named 32-bit guest, 2048 MB, 2 CPUs and disk chain |
| M6-S02 | Verified | `M6-S02-environment.png`, b | Actual release, architecture, kernel/package, compiler, ordinary identity and native workspace |
| M6-S03 | Verified | `M6-S03-code-build.png`, b/c code views | Original hashes/LF; ordinary build exit 0; seed-owned 0755 ELF32; mapping and workers |
| M6-S04 | Verified | `M6-S04-dummy-baseline.png` | Root:root 0644 original 19 bytes; direct write denied, content/hash unchanged |
| M6-S05 | Verified | `M6-S05-normal-cow.png`; `logs/fresh-control-01.txt` | Private memory changed; fresh backing-file read/hash/full baseline unchanged |
| M6-S06 | Completed trial verified | `M6-S06-task1-running.png`; `fresh-t1-01` logs | Seed UID 1000; 30-second bound; 0 integer elapsed seconds; captured after completion |
| M6-S07 | Exact Task 1 success | `M6-S07-task1-result.png`; live/offline checks | Exact full replacement, unchanged root:root 0644 and 19-byte length |
| M6-S08 | Verified | `M6-S08-charlie-baseline.png`, b; prepared-snapshot record | Fresh UID-1001/GID-1002 login; full protected baseline; powered-off normal snapshot |
| M6-S09 | Exact Task 2 file success | `M6-S09-task2-uid-change.png`, b; `fresh-t2-01` logs | Only four-character UID field replaced `1001` → `0000`; all other bytes and metadata retained |
| M6-S10 | Fresh UID-0 login verified | `M6-S10-task2-root-proof.png`; b shell-exit view | Non-sudo `su - charlie`; first auth failed, retry succeeded; `id -u` 0; proof PID 3392 subsequently absent |
| M6-S11 | Exact restoration verified | `M6-S11-account-restored.png`, b; restoration artifacts | Complete original file/hash; fresh non-sudo UID-1001 login; exit to seed |
| M6-S12 | Optional — not performed; discussion only | Report countermeasure discussion | No patched-VM measurement or screenshot claimed |
| M6-S13 | Cleanup/export verified | `M6-S13-cleanup.png`; cleanup log, final export and poweroff records | No experiment/su/root shell; only root:0; dummy absent; ordinary binaries; closed exports verified |

## Task summaries

**Task 1:** ordinary write denied; normal COW changed only private memory; sole race `fresh-t1-01` produced the exact backing file `111111******333333\n`, retaining root:root 0644 and 19 bytes. Live and independent exported-file checks passed. Measured 0 integer wall seconds under a 30-second limit.

**Task 2:** sole race `fresh-t2-01` changed `charlie:x:1001:1002:,,,:/home/charlie:/bin/bash` to `charlie:x:0000:1002:,,,:/home/charlie:/bin/bash`, with the rest of the 2040-byte file identical and root:root 0644 retained. It measured 0 integer wall seconds under a 30-second limit. One authentication failure preceded a successful fresh non-sudo UID-0 login. After that shell ended, exact restoration and another fresh UID-1001 login passed.

**Environment:** prescribed historical guest freshly verified; targets and account confined to that VM; network disconnected. Final guest is powered off after successful cleanup and host export verification. No finer race runtime, kernel attempt count, patched trial or oral rehearsal was measured.

## Original artifacts and provenance

* `logs/fresh-control-01.txt`, `logs/fresh-t1-01-*`, `logs/fresh-t2-01-*`: actual program/summary output, complete before/after files, metadata and live verifier output. The verification `.log` files include two guard-output lines before JSON.
* `provenance/fresh-t1-01-offline-check.json`, `fresh-t2-01-offline-check.json`: independent host verification of exported copies only.
* `provenance/passwd-normal.sha256`, `charlie-normal.txt`, `uid0-normal.txt`: normal non-secret account baseline records. The protected root-held backup remains inside the VM.
* `logs/m6-fresh-20261009-1946.typescript`: closed 26,479-byte setup/control/Task 1/normal-account transcript.
* `logs/fresh-task2-20261009.typescript`: closed 13,899-byte Task 2/authentication/restoration/cleanup transcript.
* `member6-fresh-pre-task2.tar.gz` and checksum: verified export before the prepared snapshot. Its first footer-based transcript assertion failed; process-exit and matching-byte verification resolved closure without changing the transcript.
* `member6-fresh-final-20261009.tar.gz` and checksum: final 46-file guest export; SHA-256 **08fe8d346f51f506a6b205683ead027d031a7d9fca34839045af7595bbb35fa1**. Whole restored file, original sources, trial artifacts, closed transcript and cleanup log verified in `provenance/final-export-verification.json`.
* `M6-task2-recorded-screen0.webm`, `M6-task2-login-screen0.webm`: original native VirtualBox recordings. Presentation excerpts are documented in the submission's video provenance.
* `provenance/`: unedited diagnostic framebuffers, capture sidecars, snapshot/recording configuration and errors, image reviews and original public command-delivery records.

## Evidence presentation and remaining human actions

There are **21 selected originals**: 18 guest captures and three host views. Guest images are actual unedited VirtualBox framebuffers; S01 was supplied by the user. S06 and S09 show completed trials. Report/slide readability crops retain unchanged source pixels and explicit crop provenance. Authentication failures remain visible and explained. Recorded video is identified as recorded; omitted waiting intervals are documented.

The user approved the **Member 6 — ISSD** cover. Personal/course identity, deadline/upload channel, required final format and speaking allowance remain unconfirmed. Complete a spoken rehearsal, review the final documents and submit/present through the course's required channel. Independent technical and document preparation does not require those administrative details.

**Assistance:** GPT-6 Astra through OpenCode helped with public guest command delivery, verification, genuine captures and document preparation. The user supplied host screenshots and performed interactive authentication. The folder/prompt name does not establish use of Opus. Retain **Wenliang Du / SEED Labs, CC BY-NC-SA 4.0** attribution for the task and exploit-pattern adaptation.
