# Evidence checklist — completed and audited

The selected original PNGs are in this folder. Complementary `a`/`b` images cover larger checkpoints. See [EVIDENCE_REVIEW.md](EVIDENCE_REVIEW.md) for the actual filenames, captions and timing qualifications. Checkmarks refer to collected practical evidence, not a claim that a classroom presentation or upload has occurred.

| Done | ID / suggested filename | When | What must be visible |
|---|---|---|---|
| [x] | `S01-vm-setup.png` | VM setup | VM name, RAM and attached disk; effective CPU count supplemented in S03 |
| [x] | `S02-guest-environment.png` | Guest checks | Ubuntu version, kernel, GCC and seed identity |
| [x] | `S03-lab-permissions.png` | Lab setup | Root-owned Set-UID victims, controls 0/0, sticky /tmp |
| [x] | `S04-vulnerable-code.png` | Source review | Default delay zero and separate access/fopen |
| [x] | `S05-task1-target-validation.png` | Manual validation | Actual failed attempt and successful UID-0 retry; administrator insertion labelled |
| [x] | `S06-task2a-timing.png` | Slow wait | Check-passed message and actual link switch |
| [x] | `S07-task2a-result.png` | Slow result | Complete record and verified non-sudo UID 0 |
| [x] | `S08a/b-task2b-running.png` | Recorded naive run | Actual native initialization/start frames; precise timing qualification in review |
| [x] | `S09-task2b-result.png` | No-delay result | Actual one-attempt summary, full record, login and UID 0 |
| [x] | `S10a/b-task2b-*.png` | Failures | Root-owned regular file, actual errors and sticky bit |
| [x] | `S11-task2c-atomic-result.png` | Atomic result | Initialized method and verified UID 0 |
| [x] | `S12a/b-task3a-*.png` | Least privilege | 9,455 / 300 s, unchanged target, denied protected write and allowed control |
| [x] | `S13a/b-task3b-*.png` | OS defence | Original victim, 1/0 controls, 9,177 / 300 s and denied stable-link open |
| [x] | `S14-cleanup.png` | Final cleanup | Original baseline, no test account, Set-UID removed, chosen 1/2 policy |
| [x] | `S15-deliverables.png` | Evidence inventory | Organised captured evidence and sources at the audit checkpoint |

## Example factual caption

**S09 — recorded no-delay naive run.** The seed-launched victim changed the target after one attempt (0 integer monitor seconds; 0.237911 runner seconds). The complete record was inspected and an actual non-sudo su/id login reported UID 0. Earlier failures and the separate 20-attempt success remain in the logs.

## Accompanying saved material

* Actual `logs/*-summary.txt` files, with unique run labels for retries.
* Last-output logs where they help explain a failure or blocked operation.
* The exact final source files and `input.txt` used.
* Original and experiment sysctl values and environment versions.
* Written attempts/time/outcome notes for each task.
* A short recording of a genuine no-delay success, if useful for presentation backup.

Capture command and result together; a terminal that only shows `uid=0` without the preceding attack/login context is weak evidence. Do not substitute administrator login output for exploit proof.
