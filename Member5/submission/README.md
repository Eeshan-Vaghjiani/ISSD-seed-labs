# Member 5 — finished report, findings slides and live-demo guide

## Open these

* **LIVE_PREPARATION.md** / **LIVE_PREPARATION.pdf** — VM prerequisites, missing-helper recovery, display setup, full/short rehearsal routes, screenshot fallbacks and Q&A.
* **MAIN_PRESENTATION.pptx** — editable main presentation: mechanism, interpretation of terminal output, recorded findings and countermeasures. The live-demo transitions are slides 3, 5 and 7.
* **LIVE_COMMANDS.pdf** / **LIVE_COMMANDS.md** — compact A/B command sheet to keep beside you while presenting.
* **LIVE_DEMO.pdf** / **LIVE_DEMO.md** — full ordered A/B guide with setup, the ten-second demonstration, a bounded genuine no-delay run, a short defence control, cleanup and recovery explanations.
* **REPORT.pdf** / **REPORT.docx** / **REPORT.md** — completed experimental report with actual results, explanations, failures, captions, references and assistance disclosure.
* **MAIN_PRESENTATION.pdf** — portable slide copy.
* **SLIDE_NOTES.md** / **SLIDE_NOTES.pdf** — what to say and when to switch to the terminals. Notes are also embedded in the PPTX.

The cover uses **Member 5 — ISSD**, as requested. Unknown personal/administrative fields were omitted. The deck is organised around the live demonstration and findings rather than an imposed speaking length. The recorded measurements are not represented as the result of a future classroom attempt.

## Supporting material

* `evidence/` — selected original screenshots, with source/hash mapping.
* `figures/` — labelled readability crops used in documents; original images are retained and `CROP_MANIFEST.json` records each crop.
* `source/` — actual C/shell lab files and input record.
* `automation/` — the existing VM helpers used by the command guide.
* `logs/` — original labelled summaries, attacker outputs and controls, including failures.
* `provenance/` — verified login records, exact-append/recording metadata and monitor changes. The current evidence review is `../evidence/EVIDENCE_REVIEW.md`.
* `BUILD_VERIFICATION.md` — completed document and layout checks.
* `READINESS_REVIEW.md` — requirement-by-requirement review, screenshot qualifications and remaining rehearsal actions.

The complete raw VM evidence archive remains available at `/home/seed/issd-member5/exports/member5-evidence-audited-20261003-064223.tar.gz`. Earlier full captures and preservation records remain intact. Figure crops are for readability, not new or manufactured terminal output.

## Before the live demonstration

The VM was cleaned up: the original password file is restored, no test account or experiment process remains, and victims have mode 0755. **Start with Part 0 of LIVE_DEMO** to re-enable the documented lab setup. Use the prepared SEED VM path `/home/seed/issd-member5/lab-files`. The guide's lab helpers are already installed in that VM; opening this document directory does not itself set up a fresh VM.

All attacker/victim/monitor invocations run as seed. Enter passwords directly in the terminal when prompted. Exit root login shells and stop experiments before resetting. The final chosen protection policy is 1/2; the saved 0/0 file is not asserted to contain the original VM defaults.

Final human actions are to rehearse the explanation/live transitions, review the files, and upload or present them through the course's required channel. No oral rehearsal or submission upload is claimed to have occurred automatically.

## Attribution

The task and vulnerable-program pattern are adapted from Wenliang Du / SEED Labs, *Race Condition Vulnerability Lab*, copyright 2006–2020, Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International. See the report's references and assistance disclosure.
