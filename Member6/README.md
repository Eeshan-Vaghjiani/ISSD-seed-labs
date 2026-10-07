# ISSD — Member 6: Dirty COW lab pack

**Arch execution update — 7 October 2026:** the repository is audited and the separate `ISSD-Member6-SEED12` VM plus `M6-clean-SEED12` snapshot are created. **A host reboot is required before the first guest boot; the experiments remain unexecuted.** Start with [ARCH_HOST_SETUP.md](ARCH_HOST_SETUP.md), then [VM_SESSION_GUIDE.md](VM_SESSION_GUIDE.md). See [the complete checkpoint status](EXECUTION_STATUS.md), [repository audit](REPOSITORY_AUDIT.md), [capture plan](evidence/CAPTURE_PLAN.md), and [submission preparation](submission/README.md).

**Start with [START_TO_FINISH_GUIDE.md](START_TO_FINISH_GUIDE.md)** or its editable Word copy, `START_TO_FINISH_GUIDE.docx`.

## Critical environment distinction

The lecturer's Dirty COW link is under `Labs_20.04`, but the official page explicitly requires the **32-bit SEED Ubuntu 12.04 VM**. Its historical manual describes kernel **3.5.0-37-generic**. Check your actual running kernel. The SEED Ubuntu 16.04 and 20.04 images have the Dirty COW fix and are unsuitable for reproducing the vulnerable behaviour.

Member 5 uses Ubuntu 20.04 for an application-level race. Member 6 uses the separate old VM for **CVE-2016-5195**, a kernel copy-on-write race. Both may use the same Windows VirtualBox installation, but different guest disks and snapshots.

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
| `tools/export_documents.py` | Word exporter, run on the Windows host using Python 3.8+ and python-docx |
| `VERIFICATION.md` | Preparation checks and unexecuted VM checks |

The official lab has **Task 1: modify a dummy read-only file** and **Task 2: modify charlie's UID to obtain root privilege**. The countermeasure discussion and short demonstration come from the group division. The normal-COW control and optional patched-VM comparison are explanatory additions, not additional numbered SEED tasks.

## Evidence status

Research and preparation: **29 September 2026**. This pack is ready for execution, but no Dirty COW run or result has been fabricated. Fill in the report from your actual VM session. See `VERIFICATION.md` for precisely what has been checked.

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
