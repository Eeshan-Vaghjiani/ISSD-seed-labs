# Member 5 — audited practical-lab evidence

**Practical experiments and screenshot checkpoints S01–S15: complete.**

Follow-up audit: **3 October 2026**, session `20261003-064223`. The screenshots were inspected as images, not accepted merely because their filenames existed. Use the copies in [`audit-20261003-064223/selected/`](audit-20261003-064223/selected/) for the report. The original files, earlier failures, and original frame sequence are retained.

**Submission work remains:** the repository's `Member5/REPORT_TEMPLATE.md` still contains unfilled identity/course fields, results/figure placeholders, and presentation/rehearsal sections. Completing the practical and collecting its evidence does not complete that written report or establish that a presentation was rehearsed/submitted.

## Checked screenshots and captions

| Checkpoint | Selected image(s) | Verified observation / caption |
|---|---|---|
| S01 | [VM setup](audit-20261003-064223/selected/S01-vm-setup.png) | VM `Eeshan4`, 2048 MB RAM, VMSVGA and attached `SEED-Ubuntu20.04.vdi`. The preset says Oracle Linux; S02/S03 establish the actual Ubuntu guest. The effective one-vCPU count is shown in S03. |
| S02 | [Guest environment](audit-20261003-064223/selected/S02-guest-environment.png) | `seed` UID 1000, Ubuntu 20.04.1 LTS, x86-64, kernel 5.4.0-54-generic and GCC 9.3.0. |
| S03 | [Fresh setup](audit-20261003-064223/selected/S03-lab-permissions.png) | Clean baseline check, both protections 0, sticky `/tmp`, root-owned Set-UID victims, seed-owned attackers, ordinary-user identity and one vCPU. |
| S04 | [No-delay source](audit-20261003-064223/selected/S04-vulnerable-code.png) | Source default `DEMO_DELAY=0`, separate `access()` and `fopen()`, protected append code, and original binary imports. No imported `sleep` or `seteuid` in `vulp`. |
| S05 | [Task 1 validation](audit-20261003-064223/selected/S05-task1-target-validation.png) | **Administrator-assisted manual validation, not exploit success.** Shows manual insertion, one authentication failure and a successful non-sudo retry with UID 0. The failure is preserved. |
| S06 | [Fresh timing view](audit-20261003-064223/selected/S06-task2a-timing.png) | `vulp_slow` reports its explicit 10-second wait with RUID 1000/EUID 0 while seed switches XYZ from `/dev/null` to `/etc/passwd`. Clean, separate commands and link targets are readable. |
| S07 | [Fresh slow result](audit-20261003-064223/selected/S07-task2a-result.png) | The single slow invocation produced the exact record; a non-sudo `su - test` followed by actual `id`/`whoami` verified UID 0. |
| S08 | [Live initialization](audit-20261003-064223/selected/S08a-task2b-running.png), [live start/status](audit-20261003-064223/selected/S08b-task2b-running.png) | Native full-desktop original frames show the ordinary-user naive attacker and monitor in the recorded no-delay run. Initialization, command, original victim permissions, controls 0/0, then Start/Limit/Before status are visible. See timing/provenance details below. |
| S09 | [Recorded run result](audit-20261003-064223/selected/S09-task2b-result.png) | `task2b-audit1-20261003-064223`: **1 attempt, monitor 0 seconds, runner wall 0.237911 seconds**, exact record, non-sudo login and UID 0. Earlier verified 20-attempt success remains in the original report/logs. |
| S10 | [Original sticky failure](audit-20261003-064223/selected/S10a-task2b-sticky-bit.png), [new File-exists failure](audit-20261003-064223/selected/S10b-task2b-file-exists.png) | Actual unlink denial, root-owned regular XYZ, mode-1777 `/tmp`, preserved original-log context, and a subsequent actual File-exists failure. |
| S11 | [Atomic result](audit-20261003-064223/selected/S11-task2c-atomic-result.png) | Atomic `RENAME_EXCHANGE` method, initialized attacker, no-delay `vulp`, **1 attempt / 0 integer seconds / 0.272765 runner seconds**, exact record and verified non-sudo UID-0 login. |
| S12 | [Concurrent trial](audit-20261003-064223/selected/S12a-task3a-trial.png), [code and controls](audit-20261003-064223/selected/S12b-task3a-controls.png) | **9,455 attempts / 300 seconds**, controls 0/0, target unchanged, privilege drop before check/open, denied protected write and successful ordinary-file append. |
| S13 | [Concurrent trial](audit-20261003-064223/selected/S13a-task3b-trial.png), [stable-link denial](audit-20261003-064223/selected/S13b-task3b-controls.png) | Original vulnerable victim with controls 1/0; **9,177 attempts / 300 seconds**, unchanged target, and actual denied privileged open of a stable seed-owned `/dev/null` link in sticky `/tmp`. |
| S14 | [Latest cleanup](audit-20261003-064223/selected/S14-cleanup.png) | Original baseline restored and checked; no test record or experiment/su processes; lab links removed; victims 0755; final user-selected settings 1/2. Saved 0/0 file is retained and is not represented as original VM defaults. |
| S15 | [Artifact view](audit-20261003-064223/selected/S15-deliverables.png) | The organised selected evidence, review and actual recorded outcomes. Optional checkpoint. |

## S08 recording qualification

The earlier session's ordinary and GDK burst captures missed the short live interval. They remain legitimate startup/failure evidence and were not relabelled as live success.

The follow-up used native **GStreamer `ximagesrc` → lossless PNG frames**, beginning before the monitor was launched. No attacker/victim was paused, no artificial delay was added to `vulp`, and no terminal output was inserted or manufactured. The recording requested 30 FPS but actually produced **25 original frames in 10.004403 seconds** on this one-vCPU VM; requested rate is not claimed as delivered rate.

* `frame-00009.png` shows the initialized attacker and monitor command. Their recorded PID/start-time identities were alive at the raw-frame encoder-input and completed-file observations (06:47:24.685478 and 06:47:24.740806).
* `frame-00010.png` shows Start, Limit and Before status before the result was displayed. Both processes were alive at its raw-frame encoder-input observation (06:47:24.827170); both had ended by completed-file observation (06:47:24.934415). PNG encoding completion is later than the displayed frame; this image is not claimed to show processes still alive at file-write completion.
* These are copies of whole-desktop original frames, with matching SHA-256 values. Their pixels were not cropped, redrawn or composited.
* Full frame sequence, timestamps and process observations: [`task2b-audit1-frames/recording.json`](audit-20261003-064223/task2b-audit1-frames/recording.json).
* Selected-frame mapping: [`S08-selected-frame-provenance.json`](audit-20261003-064223/S08-selected-frame-provenance.json).

The subsequent exact record and non-sudo UID-0 login establish that this recorded no-delay trial succeeded. The screenshot does not replace that login verification. Frame capture adds scheduling overhead, so this one-attempt result is not a speed guarantee or a benchmark of the vulnerable instruction window.

## Follow-up operations and final state

At the user's request, the terminal screens were cleared **after preserving their prior transcripts/history and the existing export**. Fresh readable setup/code/timing/run/cleanup captures were made. Both root login shells from the follow-up were exited before reset; the cleanup helper checked for remaining experiment and su processes first.

The follow-up repeated one delayed invocation for clearer S06/S07 and one bounded no-delay naive trial to obtain S08. Both exact post-attack files were compared against the final clean baseline plus exactly `newline + input.txt record`. Both had real, non-sudo UID-0 login tests. No password or empty-password keystroke was supplied by automation; the user entered authentication input directly in B.

The completed 300-second least-privilege and symlink-protection trials were checked against their existing images/logs and retained. They support **“no success observed in N attempts over T seconds”**, not a universal empirical proof.

Final clean SHA-256: `b2386623b8c504aa933d9c519b96158bd55e5e6eb4ae75183d5abf9e5a191d67`. Final controls: `protected_symlinks=1`, `protected_regular=2`, as explicitly selected by the user. `sysctl-before.txt` is still the saved 0/0 file. The original backup `/root/issd-member5-passwd.original` is retained.

The earlier log ending at **76,000 attempts / 227 seconds** still has unknown final totals. Its failure, original metadata/file contents, and subsequent 9-attempt and 2-attempt sticky failures are retained. The original export remains an immutable earlier snapshot; the new audited export supplies the current evidence/checklist and manifest.
