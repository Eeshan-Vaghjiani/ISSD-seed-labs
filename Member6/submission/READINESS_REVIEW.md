# Member 6 — final readiness review

**Result: practical, evidence and presentation materials complete; ready for personal review and rehearsal.** The exact checkpoint table and artifact links are in [README.md](README.md). The cover uses the user-approved **Member 6 — ISSD** identity.

## Assignment coverage

| Requirement | Completed material and verified finding |
|---|---|
| Prescribed environment | Actual Ubuntu 12.04.2, i686/32-bit, running kernel/package family, GCC and ordinary seed recorded in S02; separate VM configuration in S01 |
| Original code and build | Four original source hashes, native ext4 workspace, fresh ordinary build, seed-owned 0755 ELF32 and readable worker/mapping excerpts in S03 |
| Protection baseline | Root:root 0644 dummy, denied direct write and unchanged content/hash in S04 |
| Explain normal COW | Writable private-mapping control with private stars and an unchanged fresh backing-file read/hash in S05; report §2 and slide 2 explain the difference from the exploit |
| Task 1 | One bounded ordinary-seed trial; exact full backing-file replacement and unchanged metadata; S06/S07 and complete logs |
| Task 2 baseline | Actual original UID 1001 / GID 1002, fresh ordinary login, protected post-creation backup and stopped powered-off prepared snapshot |
| Task 2 file change | Exact four-character UID field `1001` → `0000`; every other byte and root:root 0644/2040-byte metadata retained |
| Task 2 privilege | Fresh non-sudo login followed by actual `id`, `id -u` = 0 and `whoami` root; first authentication failure preserved |
| Restoration | Old proof shell ended, full normal file/hash restored, fresh non-sudo login returned UID 1001 and exited to seed |
| Cleanup | No experiment/wrapper/control/su/test root shell, original root-only UID-0 list, dummy absent, ordinary binaries, closed evidence/export verified |
| Mechanism explanation | COW, MAP_PRIVATE, read-only mapping, /proc/self/mem, pwrite virtual address, MADV_DONTNEED, scheduling and kernel/application distinction |
| Four countermeasure themes | Kernel patching, maintained system updates, limiting local execution and monitoring privilege escalation; report §7 and main slide 6 |
| Report structure | Executive summary plus all ten supplied-template sections, actual figures, EXPECTED / ACTUAL / EXPLANATION, limitations and source/assistance attribution |
| Presentation and fallback | Six main slides, four backup/reference slides, embedded/external notes, 66.6-second labelled recording and lecturer Q&A |
| Live demonstration support | One-page command sheet, full preparation/live/recovery/cleanup guide and provisional speaking route |

## Honest interpretation

Each sole attack trial was bounded at **30 seconds** and recorded **0 integer elapsed seconds**. This timing does not establish instantaneous execution or a kernel-level attempt count. The trial wrapper detects file change, while complete-byte verification establishes the intended exact outcome. Fresh authentication separately establishes the UID applied to a new process.

The first account authentication failed for an unestablished reason; the second non-sudo attempt succeeded without a second exploit trial. Restoring the account file does not revoke an already-running process's credentials, so proof shell 3392 was exited and checked absent first. The post-restoration ordinary login is actual S11 evidence.

The optional patched comparison is **not performed; discussion only**. The final VM is powered off normally with charlie ordinary, `/zzz` absent, both snapshots retained and network cable disconnected. Source/helper and capture provenance distinguish native VM execution from host capture/export/document work.

## Evidence presentation

All **21 selected originals** were visually inspected against the corresponding recorded outputs. Eighteen are actual guest framebuffers and three are user-provided host settings views. S01's disk-path text is truncated in the UI; the full disk chain is retained in host provenance. S06 and S09 are completed-trial captures.

The 20 report/slide crops preserve their source pixels and have explicit crop rectangles/hashes. Cropping removes unused desktop/terminal space for readability; original views remain in `evidence/`. The account-proof slide retains the failed and successful non-sudo login sequence. Dense code/build/full-file screenshots can be enlarged from the originals during questions.

The short video has distinct title cards and identifies the omitted authentication wait. Its native source recordings remain byte-identical and uncut. It shows the trial, real privileged identity commands and exit; the final card points to separately captured restoration/cleanup evidence. Video duration is not the exploit's measured runtime.

## Presentation route

1. Explain the kernel race and normal private-copy promise before switching to the VM.
2. Establish ordinary protection and run the control, then a fresh **15-second classroom dummy trial** using the supplied wrapper and a new label. Describe that attempt's actual outcome.
3. Use recorded S07 if the new attempt times out or is incomplete, explicitly identifying it as the 9 October result.
4. Present recorded Task 2 as the exact UID-field change plus a separate fresh non-sudo UID-0 proof; explain the failure, restoration and new ordinary login.
5. Cover the four countermeasures and conclude. Complete the guide's cleanup/export sequence after the live session.

The proposed timing is approximately **5 minutes 35 seconds before extra transitions**, not a measured rehearsal. Full video playback needs additional time compared with the static proof slide. Course speaking allowance remains unconfirmed.

## MANUAL ACTION REQUIRED — remaining human work

* **HOST / course:** open `REPORT.pdf` and `MAIN_PRESENTATION.pptx` or its PDF; review the wording and verify any required identity, class/group/lecturer, deadline, upload format and speaking allowance. The generic cover was approved because those details were absent.
* **HOST / VIRTUALBOX → VM:** follow `LIVE_PREPARATION.md` to start **ISSD-Member6-SEED12**, log in as seed and prepare Part 0. Rehearse the explanation and slide/terminal transitions, measure speaking time and confirm display legibility. Authenticate directly in the VM when requested, then complete Part 3 cleanup.
* **HOST / course:** submit the requested formats through the course channel and deliver the presentation. These actions have not occurred automatically.

The completed evidence already establishes both official tasks and the restored state. The rehearsal verifies your delivery and a new bounded dummy attempt on its own observations. Wenliang Du / SEED Labs attribution and the GPT-6 Astra/OpenCode assistance disclosure are retained in the report and reference slide.
