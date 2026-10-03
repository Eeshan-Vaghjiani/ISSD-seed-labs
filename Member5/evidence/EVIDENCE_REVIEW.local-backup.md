# Member 5 evidence review — 3 October 2026

Reviewed the seven images pulled in commit `21ab53a`, alongside the existing S01/S02 evidence. Newly uploaded originals are in the repository-level `evidence/` folder. Some original names use the letter **O** (`SO3`, `SO4`, `SO5`) instead of zero; the links below identify them explicitly.

## Selected evidence and captions

| Checkpoint | Selected image | Observation / suggested caption |
|---|---|---|
| S01 | [VM setup](S01-vm-setup.png) | VirtualBox has the SEED Ubuntu 20.04 disk attached, 2048 MB RAM, VMSVGA and NAT. The Oracle Linux OS-profile label is metadata; S02 establishes the guest release. |
| S02 | [Guest environment](S02-guest-environment.png) | User seed has UID 1000; the guest is Ubuntu 20.04.1 LTS, kernel 5.4.0-54-generic, x86_64, with GCC 9.3.0. |
| S03 | [Latest permissions](../../evidence/SO3-lab-permission.png) | The terminal reports a matching saved password-file baseline, both protection controls set to zero, seed UID 1000, a sticky /tmp directory and three root-owned Set-UID victim binaries. |
| S04 | [Readable vulnerable excerpt](../../evidence/S04-vulnerable-code.png) | access() checks the pathname before a separate fopen() resolves it again. The delay is conditional on DEMO_DELAY; the privilege drop is conditional on LEAST_PRIVILEGE. These are separate compile-time variants. |
| S04 supplement | [Longer source listing](../../evidence/SO4-vulnerable-code.png) | Shows DEMO_DELAY defaulting to zero, the input handling and the broader source. Text is smaller; prefer the readable excerpt for a slide. |
| S05 | [Target validation](../../evidence/SO5-task1-target-validation.png) | The user cannot directly write /etc/passwd. The record is manually appended with sudo. The first su attempt fails; the subsequent attempt succeeds and id reports UID 0. This is manual validation, not race exploitation. |
| S06 | [Timing crop](S06-task2a-timing-cropped.png) | Terminal B runs ./vulp_slow without sudo and reports RUID 1000, EUID 0 and the 10-second wait. Terminal A shows the link switch toward /etc/passwd. |
| S07 | [Result crop](S07-task2a-result-cropped.png) | Following the delayed run, the test record appears in /etc/passwd. An ordinary seed shell invokes su - test, and the resulting shell reports UID 0 and whoami root. |

The older [S03 permissions image](../../evidence/S03-lab-permissions.png) remains useful supplementary build evidence.

## Evidence qualifications

- S05 correctly reports record length 43. The intended record `test:U6aMy0wojraho:0:0:test:/root:/bin/bash` contains 43 ASCII characters, excluding the terminating newline, within the victim's 50-character input limit. A subsequent user-provided `sed -n 'l'` and `awk` check confirms the displayed record and length. The review initially stated 38 in error; that calculation has been corrected.
- The reason for S05's first authentication failure is not visible. Describe it as a failed first attempt followed by success, without guessing what password was entered.
- S06/S07 have terminal wrapping/redraw clutter. Cropping preserves this text; it does not repair, erase or reconstruct commands. A later clean recapture could improve presentation quality, but these images show the timing demonstration and login outcome.
- S07 supports a successful delayed Task 2.A result. It does not establish success of the no-delay Task 2.B/2.C experiments. No attempt count or no-delay timing is available yet.
- The clean reset after S07 is not shown in the uploaded images. Exit the root session and reset before the next experiment.
- Earlier pasted output recorded saved protection values of 0/0. These are recorded starting values, not evidence of the image's original default hardening settings.

## Crop provenance

The two crops retain both terminal title bars and all visible terminal output, removing the desktop launcher, top bar and unused lower space. Originals remain at:

- `../../evidence/S06-task2a-timing-20261003-051013.png`
- `../../evidence/S07-task2a-result-20261003-051108.png`

Reproduce from the repository root with `python Member5/tools/crop_member5_evidence.py` (requires Pillow). The script performs rectangular cropping only; no rescaling or content alteration.

## Next checkpoints

1. Exit any root session, stop lab processes and restore/verify the saved password-file baseline.
2. Input validation is confirmed by the subsequent pasted output: the intended record is present and its length is 43.
3. Task 2.B: run `./attack_naive` as seed in A; after its ready message, run `bash run_trials.sh ./vulp 300 task2b` as seed in B. Save S08, the summary log, and S09 if the record and UID-0 login are verified.
4. If the naive attacker fails, record the actual error and /tmp/XYZ ownership (S10 if the sticky-bit failure occurs). Do not assume every failed run is the same failure.
5. Complete Task 2.C, both Task 3 defences, cleanup, report and rehearsal using the main guide.
