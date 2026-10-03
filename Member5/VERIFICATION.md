# Preparation and verification status

## Completed execution — 3 October 2026

Member 5's practical tasks and screenshot checkpoints S01–S15 have now been performed and audited. See [the current evidence review](evidence/EVIDENCE_REVIEW.md) and [finished submission documents](submission/README.md). The final document/layout checks are recorded in [submission/BUILD_VERIFICATION.md](submission/BUILD_VERIFICATION.md).

* Task 1: administrator-assisted record validation, with a preserved authentication failure and successful retry.
* Task 2.A: explicit ten-second teaching window, exact record and actual non-sudo UID-0 login.
* Task 2.B: actual no-delay successes, preserved sticky failures and native original live-state frames; the audited success took one attempt (0 integer monitor seconds, 0.237911 runner seconds). Earlier verified success: 20 attempts, 1 integer second.
* Task 2.C: atomic exchange, no-delay victim, one attempt, verified non-sudo UID-0 login.
* Task 3.A: 9,455 attempts / 300 seconds without target change; protected denial and permitted-file write controls.
* Task 3.B: 9,177 attempts / 300 seconds without target change; actual stable-link denied open with the original victim.
* Cleanup: original baseline verified, no test account/processes, lab links removed, victim modes 0755. Final 1/2 policy was explicitly selected; saved 0/0 values are not represented as original defaults.

The following sections preserve the **historical pre-execution preparation review**, not the current run status.

Reviewed for the combined repository on **29 September 2026**. Existing user-supplied S01/S02 screenshots are preserved. Their presence does not establish completion of the attack experiments.

## Existing screenshot review

* S01 shows VM `Eeshan4`, 2048 MB RAM, VMSVGA, NAT and `SEED-Ubuntu20.04.vdi`. Its VirtualBox OS profile is labelled **Oracle Linux (64-bit)**; this is host configuration metadata, not the guest release. At a convenient powered-off configuration point, select Ubuntu (64-bit) for consistency and recapture S01 if needed.
* S02 actually shows `seed` UID 1000, **Ubuntu 20.04.1 LTS**, **5.4.0-54-generic**, **x86_64**, and **GCC 9.3.0**, with the required tool paths available. These are valid observed setup values from the supplied image, not invented run results.
* These screenshots support Member 5 setup. They are not evidence of a Dirty COW vulnerable environment, and do not replace Member 6's separate Ubuntu 12.04 setup.

## Completed here

* Read both supplied files: lecturer topic/link text and the group-division PDF.
* Mapped each Member 5 responsibility to guide sections and evidence checkpoints.
* Consulted the official SEED Race-Condition page, upstream task text, vulnerable source, VM installation manual and report-submission expectations.
* Checked the Linux kernel documentation for the symlink and regular-file sysctl behaviour.
* Covered every linked lab task: 1, 2.A, 2.B, 2.C, 3.A and 3.B.
* Reviewed the distinction between manual validation, delayed demonstration, genuine no-delay attack and countermeasure tests.
* Reviewed code paths for separate no-delay/slow/least-privilege builds, ordinary-user attacker execution, atomic-link initialization, stopped-process resets, input-length constraints and bounded monitoring.
* Ran Bash syntax checking **separately on both** `build.sh` and `run_trials.sh` using Git for Windows Bash; both passed `bash -n`.
* Generated all three `.docx` documents and reopened them successfully using `python-docx`; paragraph/table counts matched their generated structures.

## Still to execute in the SEED VM

* Build the C programs with Linux GCC; no Linux C compilation has been performed here.
* Verify Set-UID behaviour and the actual VM filesystem/protection settings.
* Validate the legacy account hash with the VM's authentication configuration.
* Perform and record every attack and countermeasure experiment.
* Collect actual screenshots, attempt counts, timings, hashes and UID output.
* Rehearse the presentation and complete cleanup.

The Windows host has a Windows-targeting GCC installation, but that cannot validate Linux `renameat2`/Set-UID semantics. The available Docker client has no running engine, and no running SEED VM was available. Accordingly, the pack does **not** claim successful exploitation or end-to-end runtime testing.

The Word files were checked for generation/readability by the document library, not visually paginated in Microsoft Word. Open them in Word before submitting, adjust page breaks if needed and insert your actual images. Commands remain available in the Markdown source if Word changes copy/paste formatting.

## Outstanding course details

The local lecturer text and division do not specify a deadline, marking rubric, personal presentation duration or final submission format. No LMS materials beyond the supplied files were available. Confirm those details with the group/lecturer and fill the guide's placeholders.
