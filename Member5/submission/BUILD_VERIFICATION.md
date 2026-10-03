# Member 5 — document and evidence verification

## Review scope — 3 October 2026

Reviewed the supplied lecturer allocation, official seven-page SEED task PDF, completed report, presentation, speaker notes, live-demo command guides, selected screenshots, crop manifests, relevant source/helpers and saved trial results. See [READINESS_REVIEW.md](READINESS_REVIEW.md) for the content assessment and screenshot qualifications.

## Completed checks

* 19 selected PNGs: valid images and SHA-256 matches against SELECTION.json, Member5/evidence, submission/evidence and the retained raw-capture paths under the repository's `idk just check/evidence` directory.
* 24 figure derivatives: original/derivative hashes match CROP_MANIFEST.json; decoded pixels are identical to the specified rectangular crop of the selected original.
* Seven labelled trial-result JSON files: attempt counts and outcomes agree with the corresponding summaries; unchanged/changed hashes agree; runner identity is 1000/1000 and stopped-attacker status is recorded.
* Python AST syntax checks for packaged Python helpers.
* Separate Git for Windows Bash `-n` checks for build.sh, run_trials.sh, reset.sh, audit-setup.sh, cleanup.sh and both task3 control helpers.
* DOCX ZIP integrity and successful reopening with python-docx.
* DOCX paragraph/table text agrees with exported PDFs after normalizing whitespace/soft hyphens and excluding page furniture.
* Completed Markdown sources contain no INSERT/OBSERVED/PASS-FAIL result placeholders; report image references exist and match its DOCX image count.
* PDF text bounds: no extracted words outside the page bounds.
* PPTX successfully reopens; 12 slides have notes; shape bounds stay inside slides; PPTX text agrees with corresponding PDF pages.
* Visual review of the report's screenshot figures, slide layouts, live-demo guide and preparation companion. Dense original terminal captures require enlargement for projection; see the readiness review.

## Deliverables

| Artifact | PDF pages / slides | Embedded report figures |
|---|---:|---:|
| REPORT | 21 | 19 |
| MAIN_PRESENTATION | 12 slides | 3 proof excerpts on backup slide 9 |
| LIVE_DEMO | 5 | — |
| LIVE_COMMANDS | 2 | — |
| SLIDE_NOTES | 3 | — |
| LIVE_PREPARATION | 4 | — |

The corrected presentation was regenerated with python-pptx and exported using installed Microsoft PowerPoint. The new preparation companion was generated with python-docx and exported using installed Microsoft Word. Existing report/demo/notes exports were checked in place.

## Reproduce the automated package checks

From the repository root:

```powershell
python Member5/tools/verify_submission.py
```

Requires Python, Pillow, PyMuPDF, python-docx and python-pptx. The verifier reads the package and retained raw evidence; it does not execute the lab. Bash syntax checking is separate. `tools/export_review.ps1` exports the corrected deck and preparation companion using Microsoft Office on Windows.

## Verification limits

No VM was running in the local VirtualBox running-VM list at review time. No new exploit run, Linux compilation, authentication or oral rehearsal was performed in this review. Hash agreement establishes consistency with the supplied evidence manifests, not independent proof of events outside the captures. Automated bounds checks supplement visual review; they are not a guarantee of readability from a classroom projector. Use LIVE_PREPARATION for the remaining actual-VM and timed-rehearsal checks.
