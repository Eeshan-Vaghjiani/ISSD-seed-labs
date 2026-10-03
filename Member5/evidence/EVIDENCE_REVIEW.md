# Member 5 — checked evidence and captions

**The practical tasks and S01–S15 evidence are complete.** The selected original images are directly in this folder; their original paths/hashes are recorded in `SELECTION.json`. The full VM archive remains under `/home/seed/issd-member5/exports/`.

The finished report, main findings presentation and exact A/B command guide are in [../submission/](../submission/README.md). Classroom rehearsal and upload are human actions; they are not claimed to have already taken place.

| Checkpoint | Actual selected files | What the images establish |
|---|---|---|
| S01 | [VM setup](S01-vm-setup.png) | Eeshan4, 2048 MB RAM and attached SEED Ubuntu disk. The VirtualBox preset label says Oracle Linux; S02 establishes the actual Ubuntu guest. One vCPU is also recorded in S03. |
| S02 | [Guest environment](S02-guest-environment.png) | seed UID 1000, Ubuntu 20.04.1, x86-64, kernel 5.4.0-54-generic and GCC 9.3.0. |
| S03 | [Lab permissions](S03-lab-permissions.png) | Clean baseline, controls 0/0, sticky /tmp, root-owned 4755 victims and seed-owned attackers. |
| S04 | [Vulnerable code](S04-vulnerable-code.png) | Default delay zero; separate access/fopen; no imported sleep/seteuid in the original vulp binary. |
| S05 | [Manual validation](S05-task1-target-validation.png) | Administrator insertion, preserved authentication failure, and successful non-sudo retry reporting UID 0. This is validation, not exploit proof. |
| S06 | [Slow timing](S06-task2a-timing.png) | The explicit ten-second wait and seed switching XYZ from /dev/null to /etc/passwd. |
| S07 | [Slow result](S07-task2a-result.png) | Complete record and actual non-sudo UID-0 login after the teaching-window attack. |
| S08 | [Initialization](S08a-task2b-running.png), [start/status](S08b-task2b-running.png) | Original native frame excerpts of the naive attacker and no-delay monitor. See the timestamp qualification below. |
| S09 | [No-delay result](S09-task2b-result.png) | Audited naive run: one attempt, 0 integer seconds, 0.237911 runner seconds; exact record and non-sudo UID-0 login. |
| S10 | [Sticky ownership](S10a-task2b-sticky-bit.png), [File-exists trial](S10b-task2b-file-exists.png) | Real unlink denial, root-owned regular XYZ, sticky /tmp, and a distinct new File-exists failure. |
| S11 | [Atomic result](S11-task2c-atomic-result.png) | Initialized RENAME_EXCHANGE, no-delay victim, one attempt, 0.272765 runner seconds and verified UID 0. |
| S12 | [Trial](S12a-task3a-trial.png), [controls](S12b-task3a-controls.png) | 9,455 attempts / 300 seconds with controls 0/0; target unchanged; protected operation denied and permitted-file write retained. |
| S13 | [Trial](S13a-task3b-trial.png), [controls](S13b-task3b-controls.png) | Original vulp with controls 1/0; 9,177 attempts / 300 seconds unchanged; stable seed-owned symlink causes an actual denied privileged open. |
| S14 | [Cleanup](S14-cleanup.png) | Original baseline restored, no test account/processes, temporary paths gone, victim modes 0755 and selected final policy 1/2. |
| S15 | [Evidence inventory](S15-deliverables.png) | Actual organised experimental evidence inventory at the audit checkpoint. The finished written documents were produced afterward. |

## S08 timing and provenance

The earlier still/burst captures missed the live interval and remain labelled as startup/failure images. The follow-up native GStreamer recording preserved 25 original PNG frames in 10.004403 seconds; 30 FPS was requested, not achieved.

Frame 9 displayed the initialized attacker and monitor command. Their PID/start-time identities were alive at encoder-input and file-completion observations (06:47:24.685478 and 06:47:24.740806). Frame 10 displayed Start/Limit/Before; both were alive at encoder input (06:47:24.827170), and both had ended by file completion (06:47:24.934415). Encoding completion is later than the displayed image; the latter frame is not claimed to show processes still running at file-write completion.

The full [frame sequence metadata](../submission/provenance/task2b-audit1-frames/recording.json) and [selected-frame mapping](../submission/provenance/S08-selected-frame-provenance.json) are supplied. Original whole-desktop PNGs were retained. Report/slide crops are explicitly identified in `../submission/figures/CROP_MANIFEST.json`; they are not fabricated terminal output.

## Preserved qualifications

* The old naive log ended at 76,000 attempts / 227 seconds without a final summary. Its final totals remain unknown.
* The earlier verified naive success took 20 attempts; the one-attempt S09 image is a separate, later recorded run. The report keeps their labels and timings distinct.
* All claimed successes include complete-record inspection and actual non-sudo su/id proof, rather than hash change alone.
* Finite defence trials establish no success observed in those attempts/times, supported by the code and ownership rules.
* Final protections 1/2 were explicitly chosen. The saved file still records 0/0 and does not establish the VM's original runtime defaults.
* Prior transcripts and failures were preserved before the user-requested terminal clears. No authentication password was embedded in scripts.
