# Member 6 — submission preparation status

**The experimental submission is not complete.** The Arch host/VM configuration is prepared, but a host reboot is required before the first guest boot. There are no actual M6 trial results or screenshots yet.

| Material | Current location / status |
|---|---|
| Assignment audit and Member 5 comparison | [../REPOSITORY_AUDIT.md](../REPOSITORY_AUDIT.md) — completed repository review |
| Arch/VirtualBox setup | [../ARCH_HOST_SETUP.md](../ARCH_HOST_SETUP.md) — VM/snapshot created; reboot handoff |
| Exact guest session | [../VM_SESSION_GUIDE.md](../VM_SESSION_GUIDE.md) — prepared, unexecuted |
| Capture requirements | [../evidence/CAPTURE_PLAN.md](../evidence/CAPTURE_PLAN.md) — every checkpoint mapped |
| Report structure and concepts | [../REPORT_TEMPLATE.md](../REPORT_TEMPLATE.md) — authoritative existing template |
| Actual-results record | [RESULTS.md](RESULTS.md) — explicitly not run, ready to populate from evidence |
| Speaker notes and evidence order | [SLIDE_NOTES.md](SLIDE_NOTES.md) — prepared six-slide segment and Q&A |
| Short demonstration commands | [LIVE_COMMANDS.md](LIVE_COMMANDS.md) — prepared; actual rehearsal pending |
| Per-checkpoint status | [../EXECUTION_STATUS.md](../EXECUTION_STATUS.md) |

## Final packaging after execution

Follow Member 5's organisation: `REPORT.md/.docx/.pdf`, `MAIN_PRESENTATION.pptx/.pdf`, speaker notes/live command sheet, original named screenshots, final source, actual trial logs and provenance. The M6 report must use the existing template's ten sections; retained failures and actual cleanup are part of the findings.

Before generating final results prose or slides, inspect each screenshot and the matching raw log/copies. Fill the environment table from **guest output**, not the host profile. Fill timings from the supplied helper's integer `Elapsed` field; never invent kernel attempt counts. The complete byte comparison and fresh non-sudo login support different claims and both are required for Task 2.

The existing template Word exporter uses `python-docx` and Member 5's shared renderer. The Arch host currently has LibreOffice but lacks the Python document libraries; document-tool setup/export can be done when real report data are available. A generated template is not a completed lab report. No finished experimental report/PPTX is being represented as ready before the VM work.

Remaining course inputs: name/registration number if required, group/lecturer, deadline/upload format and personal speaking allowance. The supplied course documents do not establish them.

Suggested assistance disclosure to finalise after execution: “An AI technical assistant through OpenCode helped audit the repository, prepare the separate VirtualBox environment, add verification/collection helpers and organise the write-up. Experimental conclusions are tied to actual VM captures/logs. Authentication and any specified manual steps were performed interactively.” Adjust this to the actions actually completed; retain Wenliang Du / SEED Labs attribution.
