# Member 5 — full readiness review

Reviewed on **3 October 2026** against the supplied Member 5 allocation and the seven-page official SEED Race Condition Vulnerability Lab.

## Verdict

**The completed report and saved practical evidence cover the full assigned lab. The presentation is suitable for presenting the findings. The classroom demonstration still needs a timed rehearsal in the actual VM.** No missing compulsory experiment or missing success/defence checkpoint was identified in the saved package.

This was a repository/document review: requirements, source and helpers, result logs, screenshot figures, exported document text, image integrity and slide layouts. The local VirtualBox running-VM list was empty. The reviewer did not rerun attacks, authenticate, inspect the current guest filesystem or perform an oral rehearsal. Recorded VM outcomes are supported by the supplied images/logs, not newly reproduced results.

## Lecturer requirements

| Required item | Where covered | Assessment |
|---|---|---|
| Set up and perform Race-Condition lab | Report sections 3–10, S01–S13 | Covered by recorded work |
| Define the race before demonstration | Slides 1–2, report section 2 | Correct ordering; explain concurrent timing and TOCTOU |
| Show vulnerable program/situation | Slide 2, S04, source/vulp.c, LIVE_DEMO Part 0 | Correct access/fopen and real/effective-UID explanation |
| Important commands and steps | Report code blocks; full setup guide; LIVE_DEMO | Covered; live helper installation assumptions clarified in LIVE_PREPARATION |
| Setup, attack and result screenshots | 19 selected PNGs covering S01–S15 | Core evidence present; readability qualifications below |
| Why it happens and attacker gain | Slides 2, 4, 6, 8; report sections 2, 7, 11 | Correct privileged write and actual non-sudo UID-0 login chain |
| Secure handling, permissions, atomic operations, temporary files | Report section 11; slides 6–8 and notes | All four themes covered; distinguish attacker's atomic exchange from secure defender design |
| Short live demonstration | LIVE_COMMANDS, LIVE_DEMO, LIVE_PREPARATION | Prepared; duration and execution must be rehearsed |

The supplied lecturer documents do not specify a marking rubric, exact duration, deadline or upload format. Their absence cannot be resolved from repository content.

## Full SEED task coverage

| Task | Saved evidence / result | Assessment |
|---|---|---|
| 1 — target validation | S05: 43-character seven-field entry, administrator insertion, failed login then successful non-sudo UID-0 retry | Complete; correctly distinguished from exploitation |
| 2.A — slow machine | S06/S07: explicit ten-second wait, link switch, exact record, non-sudo login/id | Complete; explicitly labelled simulation |
| 2.B — real attack | S08a/b and S09: initialized naive method, original no-delay victim, one-attempt audited success and login; earlier 20-attempt success retained | Complete; timing is run-specific |
| 2.B failure / 2.C motivation | S10a/b: actual unlink denial, separate File-exists trial, root-owned regular XYZ under sticky /tmp | Complete; original partial log's final totals remain unknown |
| 2.C — improved method | S11: initialized atomic exchange, no-delay victim, one attempt, 0.272765 runner seconds, exact record and UID 0 | Complete; does not claim universal speed superiority |
| 3.A — least privilege | S12a/b: 9,455 attempts / 300 monitor seconds, unchanged target, protected denial and successful permitted-file write | Complete; source drops privilege through file work |
| 3.B — OS protection | S13a/b: original victim, controls 1/0, 9,177 attempts / 300 monitor seconds, unchanged target and stable-link denied open | Complete; ownership/context mechanism and limitations explained |
| Cleanup | S14: baseline comparison, no test account/processes, victim modes 0755 and chosen final policy 1/2 | Recorded cleanup supported; recheck after each new rehearsal |

## Screenshot quality — good evidence, with specific qualifications

All **19 selected originals** match the SHA-256 selection manifest in both evidence folders and the retained raw-capture paths. All **24 derivatives** match their manifest hashes and the exact original crop pixels. This demonstrates consistency with the supplied provenance, not independent authentication of everything that happened outside the captures.

| Checkpoint | Quality and interpretation |
|---|---|
| S01 | Sufficient VM name/RAM/disk evidence. Oracle Linux is the VirtualBox profile label; S02/S03 establish the real Ubuntu guest. Optional cosmetic recapture only; no need to redo the lab for this. |
| S02 | Guest identity, release, kernel and GCC are readable. Some wrapped group/compiler output and extra apt output are cosmetic. |
| S03 | Strong baseline, controls, ownership and Set-UID evidence. Full original also contains CPU/environment output in A; the report crop focuses on B. |
| S04 | Readable source and imported symbols. Shows separate access/fopen and default zero delay. |
| S05 | Sufficient manual-validation proof. Preserve the failed first login and successful retry; the cause of failure is unknown. |
| S06/S07 | Clearer audited replacements cover the teaching wait and result. Root-prompt/title-setting commands add clutter in S07, but the actual su/id chain is visible. |
| S08a/S08b | Valid initialization/start frames. They are successive original recording frames, not one combined instant. Preserve the report's capture/encoder/file-write timing qualification. A still image alone does not measure concurrency duration. |
| S09 | Strong complete result chain: labelled no-delay run, summary, stopped attacker, exact record, non-sudo login and UID 0. Dense at full-desktop fit; use the report figure or slide 9 excerpts for viewing. |
| S10a/S10b | Actual errors and root-owned-file mechanism supported. The report's S10b crop shows B's ownership/result; the actual File-exists error is in A of the full original and in the attacker log. |
| S11 | Atomic initialization/command and UID-0 result are visible in the full original. A retains earlier naive-run history; distinguish the labelled atomic run. The B crop is clearer for the result. |
| S12a/S12b | Full trial and permitted/protected controls are readable in enlarged report figures. The fixed code is explained in report section 9 and supplied as source; the selected images primarily show execution/results. |
| S13a/S13b | Correct original-victim trial, controls 1/0 and denied privileged open are visible. |
| S14 | Adequate cleanup evidence. Dense terminal text benefits from zooming. |
| S15 | Historical evidence inventory, not proof that final report/slides existed at capture time. Its left terminal explicitly says written submission work remained then. Correctly qualified in the evidence review; keep optional or label as earlier inventory. |

**No compulsory screenshot recapture is indicated by this review.** For classroom projection, enlarge relevant terminal areas rather than putting all whole-desktop screenshots on slides. The current deck intentionally uses explanatory slides and live terminals, with one dedicated backup proof slide; the full report carries the wider evidence set.

## Slides and written documents

* MAIN_PRESENTATION has **12 slides**, with slides **1–8** forming the main talk and **9–12** providing evidence/Q&A/recovery/references. All slides have embedded speaker notes.
* The reviewed slide layouts are readable, with consistent headings and contrast. Explain the four countermeasure themes orally using notes; the report contains their fuller technical qualifications.
* Slide 5 previously called the Bash timer resolution sub-second. Corrected to **whole seconds; 0 s does not mean zero runtime**, then regenerated PPTX/PDF.
* REPORT is **21 PDF pages**, with **19 embedded figures** covering the required experimental evidence. S15 is optional and is not required as a report figure. Important snippets have explanations; results are populated rather than placeholders.
* LIVE_COMMANDS is **2 pages**, LIVE_DEMO **5 pages**, and SLIDE_NOTES **3 pages**. Their DOCX and PDF text agree, including code/table content, after accounting for headers/footers and layout whitespace.
* The report has a few cosmetic source-format remnants, such as literal backticks within a bold sentence and stars around reference titles. They do not obscure the meaning or leave missing content.

## Improvements made during this review

1. Corrected the slide 5 timer explanation and regenerated both slide formats.
2. Added LIVE_PREPARATION in Markdown/Word/PDF: guest prerequisites, missing-helper transfer, directory assumptions, display setup, full/short presentation routes, fallback mapping and Q&A.
3. Clarified in the entry-point README that the finished report is submission/REPORT, while parent templates/plans are historical preparation material.
4. Documented the old setup guide's sudo-read and saved-0/0 cleanup differences. Current classroom setup/cleanup is LIVE_DEMO Part 0/Part 4.
5. Included the original task3a-controls.sh and task3b-controls.sh helpers from the retained VM export. Their commands appear in the screenshots; previously they were outside submission/automation. These are preserved historical helpers, not newly modified experiment code.
6. Added BUILD_VERIFICATION.md to resolve the missing verification link, plus a reusable read-only verification tool.

## Remaining actions before presenting

1. Boot the actual SEED VM and follow LIVE_PREPARATION's checks. A Windows pull does not update the guest. Confirm all helpers, the audited monitor, binaries, input, writable logs directory and the VM's own original baseline exist.
2. Rehearse the complete explanation → terminal switch → observed result → exit/reset → cleanup sequence. No rehearsal duration or fresh VM run is claimed by this review.
3. If the group's slot is tight, perform the slow teaching demonstration live and present the recorded no-delay/defence findings. Add the bounded atomic run and OS control when the allowance permits; both routes are documented.
4. Open the PDF backup and the relevant screenshot fallbacks on the presentation laptop in advance.
5. Confirm the group's exact duration, submission naming/format and deadline.

**Bottom line:** the recorded full-lab work is substantively ready. Presentation readiness now depends mainly on a successful timed VM rehearsal and using the finished submission files, rather than collecting a new set of screenshots.
