# ISSD — Member 6: Dirty COW lab pack

**Verified fresh run — 9 October 2026:** **both official tasks, the fresh non-sudo UID-0 login, exact restoration and final cleanup are complete.** Each sole 30-second-bound trial recorded 0 integer elapsed seconds; full-file/live/offline checks passed. Charlie is restored to UID 1001 / GID 1002, `/zzz` is removed, the closed evidence archive is verified, and the VM is powered off normally. See the [submission package](submission/README.md), [complete checkpoint table](evidence/incoming/opus-fresh-20261008/README.md), [actual results](submission/RESULTS.md) and [image review](evidence/incoming/opus-fresh-20261008/EVIDENCE_REVIEW.md).

**Historical handoff — 8 October 2026:** [OPENCODE_HANDOFF.md](OPENCODE_HANDOFF.md) and [OPUS_5_5_FRESH_RUN_PROMPT.md](OPUS_5_5_FRESH_RUN_PROMPT.md) preserve the original fresh-run request and pre-experiment state. The completed run above supersedes that handoff. Actual fresh-run assistance was GPT-6 Astra through OpenCode on Arch; the required guest remained the historical 32-bit SEED12 VM.

The separate `ISSD-Member6-SEED12` VM and both `M6-clean-SEED12` / `M6-charlie-normal-ready` snapshots are retained. See [the current checkpoint status](EXECUTION_STATUS.md), [repository audit](REPOSITORY_AUDIT.md), [Arch setup](ARCH_HOST_SETUP.md), [VM session guide](VM_SESSION_GUIDE.md), [capture plan](evidence/CAPTURE_PLAN.md), and [completed submission](submission/README.md). Older pre-boot records describe their original checkpoints.

**Open the finished [report and presentation package](submission/README.md).** For the next demonstration, use [LIVE_PREPARATION.md](submission/LIVE_PREPARATION.md). The original [START_TO_FINISH_GUIDE.md](START_TO_FINISH_GUIDE.md) and its Word copy remain the full installation/experiment instructions.

## Critical environment distinction

The lecturer's Dirty COW link is under `Labs_20.04`, but the official page explicitly requires the **32-bit SEED Ubuntu 12.04 VM**. Its historical manual describes kernel **3.5.0-37-generic**. Check your actual running kernel. The SEED Ubuntu 16.04 and 20.04 images have the Dirty COW fix and are unsuitable for reproducing the vulnerable behaviour.

Member 5 uses Ubuntu 20.04 for an application-level race. Member 6 uses the separate old VM for **CVE-2016-5195**, a kernel copy-on-write race. This fresh Member 6 run used VirtualBox on **Arch**, with its own guest disk and snapshots. The original Windows setup instructions are retained for reference.

## Contents

| File | Purpose |
|---|---|
| `START_TO_FINISH_GUIDE.md` / `.docx` | Installation, tools, commands in sequence, all official tasks, observations, cleanup and troubleshooting |
| `REPORT_TEMPLATE.md` / `.docx` | Prepared explanation structure with explicit actual-result and screenshot placeholders |
| `PRESENTATION_PLAN.md` / `.docx` | Slide content, speaker notes, short demo and Q&A |
| `lab-files/cow_attack.c` | Explained lab adaptation: fixed dummy-file and charlie-UID task modes |
| `lab-files/cow_control.c` | Normal private-copy demonstration for the dummy file |
| `lab-files/build.sh` | Compile using Linux GCC and pthreads |
| `lab-files/run_trial.sh` | Bounded trial, before/after copies, hashes and output logs |
| `evidence/SCREENSHOT_CHECKLIST.md` | When to capture each screenshot and what it establishes |
| `tools/export_documents.py` | Original guide/template Word exporter |
| `tools/build_submission.py`, `build_recorded_fallback.py`, `verify_submission.py` | Host-only completed-document/media build and package verification |
| `VERIFICATION.md` | Fresh-run verification plus dated historical preparation checks |
| `submission/` | Completed report, presentation, recorded fallback, live-demo guides and verified supporting evidence |

The official lab has **Task 1: modify a dummy read-only file** and **Task 2: modify charlie's UID to obtain root privilege**. The countermeasure discussion and short demonstration come from the group division. The normal-COW control and optional patched-VM comparison are explanatory additions, not additional numbered SEED tasks.

## Evidence status

Research/preparation began **29 September 2026**. The fresh practical was completed **9 October 2026**, with 21 selected genuine originals and two closed transcripts. The optional patched comparison is **not performed; discussion only**. Use `submission/` for the actual findings; the original guide/templates retain their instructional role.

The supplied course files are preserved in [`../Member5/course-materials/`](../Member5/course-materials/). They contain no deadline, presentation allowance or final report format; confirm those details with the group/lecturer.

## Sources and attribution

1. Supplied `ISSD presentation division .pdf`, Member 6 row, and `text from division from lec.txt`.
2. [Official Dirty COW lab page](https://seedsecuritylabs.org/Labs_20.04/Software/Dirty_COW/).
3. [Official task PDF](https://seedsecuritylabs.org/Labs_20.04/Files/Dirty_COW/Dirty_COW.pdf).
4. [Official Labsetup ZIP](https://seedsecuritylabs.org/Labs_20.04/Files/Dirty_COW/Labsetup.zip).
5. [Upstream task text](https://github.com/seed-labs/seed-labs/blob/master/category-software/Dirty_COW/Dirty_COW.tex) and [original cow_attack.c](https://github.com/seed-labs/seed-labs/blob/master/category-software/Dirty_COW/Labsetup/cow_attack.c).
6. [SEED VM downloads](https://seedsecuritylabs.org/labsetup.html) and [Ubuntu 12.04 VM manual](https://seedsecuritylabs.org/Labs_12.04/Ubuntu12_04_VM_Manual.pdf).
7. [Ubuntu CVE-2016-5195 advisory and package-specific fixes](https://ubuntu.com/security/CVE-2016-5195).
8. [mmap(2)](https://man7.org/linux/man-pages/man2/mmap.2.html), [madvise(2)](https://man7.org/linux/man-pages/man2/madvise.2.html), and [proc_pid_mem(5)](https://man7.org/linux/man-pages/man5/proc_pid_mem.5.html).
9. [Official SEED submission expectations](https://github.com/seed-labs/seed-labs/blob/master/common-files/submission.tex).

The task structure and exploit pattern are adapted from **Wenliang Du / SEED Labs**, whose lab text is licensed **CC BY-NC-SA 4.0**. This educational adaptation is shared under the same [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) terms. Retain attribution, explain your code, and acknowledge assistance according to course rules. The historical VM manual is separately licensed under the GNU Free Documentation License; it is referenced, not republished in this pack.
