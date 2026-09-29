# ISSD — SEED security lab guides

Two complete preparation packs for the group lab allocation:

| Role | Start here | Required guest |
|---|---|---|
| **Member 5 — Race-Condition Vulnerability Lab** | [Guide](Member5/START_TO_FINISH_GUIDE.md) · [Word guide](Member5/START_TO_FINISH_GUIDE.docx) · [Pack index](Member5/README.md) | SEED Ubuntu **20.04** |
| **Member 6 — Dirty COW Attack Lab** | [Guide](Member6/START_TO_FINISH_GUIDE.md) · [Word guide](Member6/START_TO_FINISH_GUIDE.docx) · [Pack index](Member6/README.md) | SEED Ubuntu **12.04, 32-bit**, vulnerable kernel |

**Do not use the same guest image for both attacks.** Dirty COW's official URL contains `Labs_20.04`, but the page explicitly requires the old 12.04 image; the later SEED kernels are patched.

Each member folder contains:

* Installation and end-to-end commands, including which source/executable/helper to run.
* An editable Word guide, report template and presentation plan, plus Markdown sources.
* Lab C programs and Bash helpers.
* Screenshot checkpoints, evidence folder and verification status.
* Source citations, explanations, troubleshooting, reset and cleanup steps.

The original lecturer text and group-division PDF are preserved in [Member5/course-materials](Member5/course-materials/). Member 5's existing S01/S02 screenshots are retained. Reports contain placeholders for experiments still to perform; prepared documentation is not a claim that every experiment has been executed.

## Local layout

```text
group lab/
  .git/                 existing repository history, now at this level
  .gitattributes
  .gitignore
  README.md
  Member5/              Race-Condition pack and original course materials
  Member6/              Dirty COW pack
```

GitHub does not display `.git/`: that metadata folder exists only in local clones. The existing repository is [Eeshan-Vaghjiani/ISSD-seed-labs](https://github.com/Eeshan-Vaghjiani/ISSD-seed-labs); its original history is retained.

## Word export

On a host with Python 3.8+ and `python-docx` installed:

```powershell
python Member5/tools/export_documents.py
python Member6/tools/export_documents.py
```

The Member 6 exporter reuses the Member 5 document renderer. Edit Markdown before regenerating; edits made directly in Word are not automatically copied back. Lab code is compiled inside the corresponding Linux VM, not using a Windows C compiler.

## Attribution

Teaching content and vulnerable-program patterns are adapted from **Wenliang Du / SEED Labs**; see each member's README for primary references and **CC BY-NC-SA 4.0** attribution. The supplied lecturer/group documents remain attributed to their original authors. Retain source attribution and follow course requirements for acknowledging assistance.
