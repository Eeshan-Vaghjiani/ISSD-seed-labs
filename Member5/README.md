# ISSD — Member 5 lab pack

**Completed work:** open [submission/README.md](submission/README.md) for the finished report, main findings PPTX, slide notes, and the exact A/B live-demo command guide. The audited screenshots are directly in [evidence/](evidence/); see [the evidence review](evidence/EVIDENCE_REVIEW.md).

**Start with [START_TO_FINISH_GUIDE.md](START_TO_FINISH_GUIDE.md).** It takes you from installing VirtualBox to collecting evidence and presenting the SEED Race-Condition Vulnerability Lab.

Prefer Word? Open **`START_TO_FINISH_GUIDE.docx`**, **`REPORT_TEMPLATE.docx`**, and **`PRESENTATION_PLAN.docx`** in this folder. The Word report has the same evidence placeholders, ready for inserting screenshots. Markdown is the source for regeneration; edits made directly in Word will not be copied back to Markdown.

| File / folder | Purpose |
|---|---|
| `START_TO_FINISH_GUIDE.md` | Full setup, commands in order, all official tasks, screenshot checkpoints, troubleshooting and cleanup |
| `REPORT_TEMPLATE.md` | Write-up with explanations drafted and clearly marked placeholders for your actual evidence |
| `PRESENTATION_PLAN.md` | Slide outline, speaking notes, live-demo sequence and questions to practise |
| `lab-files/` | C programs and Bash helpers; copy this whole folder into the SEED VM |
| `evidence/SCREENSHOT_CHECKLIST.md` | Screenshot names and what each must prove |
| `tools/export_documents.py` | Optional Word export using Python and `python-docx` |
| `VERIFICATION.md` | Checks completed here and the remaining VM execution checks |

## What the supplied materials say

* `course-materials/text from division from lec.txt`: lecturer topic list and links to the Race-Condition and Dirty-COW labs. It contains no deadline, marking rubric, slide count or submission format.
* `course-materials/ISSD presentation division .pdf`, Member 5 row: perform and explain the Race-Condition lab, document commands, capture setup/attack/result screenshots, explain impact and countermeasures, and prepare a short live demonstration.
* Dirty COW is assigned to **Member 6**. Members 1–4 handle the authentication topics. Coordinate your transition with them, but your practical work is the Race-Condition lab.

This pack covers SEED Tasks **1, 2.A, 2.B, 2.C, 3.A and 3.B**. These task details come from the lecturer-linked SEED lab, not extra instructions invented for the lecturer.

## Current execution status

The Member 5 practical tasks and S01–S15 evidence were completed and audited in the SEED VM on **3 October 2026**. Both no-delay attack methods have actual non-sudo UID-0 login proof, and the two independent defences have completed 300-second trials. The VM was cleaned up with an original-baseline comparison, removed Set-UID, and the explicitly chosen final 1/2 protection policy. The saved 0/0 file does not establish original VM defaults.

The final documents use **Member 5 — ISSD** on the cover as requested. The main presentation explains findings and terminal output; the exact live commands are in `submission/LIVE_COMMANDS.pdf` and the fuller `LIVE_DEMO.pdf`. Presentation rehearsal and course submission are human actions, not claimed as already performed.

### Historical preparation status — 29 September 2026

Prepared from the supplied materials and official online references; reviewed for the combined repository on **29 September 2026**. The existing user-supplied `evidence/S01-vm-setup.png` and `evidence/S02-guest-environment.png` are preserved. The remaining experiments and report fields must be completed from your own VM sessions; this pack does not preclaim attack success, a root session or countermeasure results. No running SEED Linux VM was available to the preparation agent for end-to-end verification.

The guide assumes an Intel/AMD Windows host. Use the prebuilt **SEED Ubuntu 20.04 VM**, as specified by the linked lab. All attack commands are for that disposable VM. SEED Labs is a collection of teaching labs and VM images, not a Windows application you install with `pip`.

For the other practical, see [Member 6's Dirty COW pack](../Member6/README.md). It uses a separate old SEED Ubuntu 12.04 guest; your Ubuntu 20.04 image is not its vulnerable environment.

## Sources and attribution

1. Supplied lecturer text and group-division PDF above.
2. [Official Race-Condition lab page](https://seedsecuritylabs.org/Labs_20.04/Software/Race_Condition/).
3. [Official task PDF](https://seedsecuritylabs.org/Labs_20.04/Files/Race_Condition/Race_Condition.pdf).
4. [Official lab setup ZIP](https://seedsecuritylabs.org/Labs_20.04/Files/Race_Condition/Labsetup.zip).
5. [SEED VM downloads](https://seedsecuritylabs.org/labsetup.html) and [VM installation manual](https://github.com/seed-labs/seed-labs/blob/master/manuals/vm/seedvm-manual.md).
6. [SEED task source](https://github.com/seed-labs/seed-labs/blob/master/category-software/Race_Condition/Race_Condition.tex) and [upstream vulnerable program](https://github.com/seed-labs/seed-labs/blob/master/category-software/Race_Condition/Labsetup/vulp.c).
7. [SEED submission expectations](https://github.com/seed-labs/seed-labs/blob/master/common-files/submission.tex): a detailed report, screenshots, observations, important code snippets and explanations; code alone is insufficient.
8. [Linux kernel documentation for `protected_symlinks` and `protected_regular`](https://www.kernel.org/doc/html/latest/admin-guide/sysctl/fs.html).

The task structure, example password-file entry and vulnerable-program pattern are from **SEED Labs, Wenliang Du**. The upstream lab text is licensed **CC BY-NC-SA 4.0**. This educational adaptation is shared under the same [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) terms; retain attribution when distributing it. The monitoring, build helpers and presentation/report organisation were prepared for this pack. Acknowledge assistance according to your course rules and explain all submitted code yourself.
