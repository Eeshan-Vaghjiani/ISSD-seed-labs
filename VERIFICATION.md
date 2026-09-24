# Preparation and verification status

Checked on **23 September 2026**.

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
