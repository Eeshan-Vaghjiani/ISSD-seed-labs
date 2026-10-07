# Member 6 — repository and requirement audit

Audit date: **7 October 2026**. Baseline commit: **`2906f262d2f9364dc8dddd3ec69a9087b4b413de`**. Origin: `https://github.com/Eeshan-Vaghjiani/ISSD-seed-labs.git`. The worktree was clean at the start.

## Scope actually reviewed

All **616 tracked files** were read/hash-inventoried (254 distinct payloads). Unique PNG, Office ZIP/XML, PDF-text, JSON/JSONL, shell/Python syntax and evidence-archive structures passed the applicable checks. The complete file inventory and check results are in [evidence/host/repository-audit-20261007.json](evidence/host/repository-audit-20261007.json).

| Area | Tracked files at audit | Role |
|---|---:|---|
| Root README, attributes, ignore file | 3 | Pack navigation, attribution, LF rules and artifact exclusions |
| `Member6/` | 14 | Six Markdown specification documents, three Word copies, four supplied lab files, exporter |
| `Member5/` | 212 | Shared course allocation, historical preparation, finished submission, selected evidence, source/helpers |
| Root `evidence/` | 7 | Earlier Member 5 captures |
| `idk just check/` | 380 | Retained Member 5 VM export, raw transcripts, source, captures and archives |

Read in full: the shared lecturer text and two-page division PDF; all Member 6 Markdown/C/shell/Python; the Member 5 guides/templates, final report, presentation notes, readiness/build reviews, live guides, source/build/monitor and packaged automation. The retained raw report and evidence reviews explain the older archives. Representative Member 5 setup, identity, real-result and cleanup screenshots were visually inspected. Structural checks of all image files are distinct from semantic visual review.

The independent consistency check found **19 selected original images** matching both published copies and raw captures, **24 derivatives** matching their manifest/crop pixels, and **7 trial result records** agreeing with summaries, identities and hashes. This assesses retained evidence; it is not a new reproduction of Member 5's VM experiments.

## Exact assignment

The division's Member 6 row requires: perform Dirty COW; explain COW and the vulnerability; demonstrate protected-data modification; document commands; capture environment/attack/result; explain vulnerability and impact; discuss **kernel patching, system updates, limiting local access, monitoring privilege escalation**; prepare a short live demo.

| Requirement | Authoritative repository location | Required execution / proof |
|---|---|---|
| Historical environment | `README.md`; guide §§3–4 | Separate SEED Ubuntu **12.04, 32-bit** VM; inspect actual kernel/package; historical manual identifies **3.5.0-37-generic** |
| Official media | guide §3.1 | `SEEDUbuntu12.04.zip`, official SEED-linked DigitalOcean source; published MD5 `6ec9c429a2f4a9163530ada20f0621dc` |
| Guest location | guide §4.2 | `/home/seed/issd-member6/lab-files`, native Linux filesystem; transfer from share first |
| Build | guide §5; `lab-files/build.sh` | Ordinary-user `bash build.sh`; GNU99, warnings, O2, `-pthread` for attack; normal 0755 executables |
| Task 1 baseline | guide §6 | Root:root 0644 `/zzz`, **19 bytes** including newline: `111111222222333333\n`; ordinary redirection denied |
| Normal-COW control | guide §6.1 | Private writable mapping changes to stars; a fresh file read/hash remains original |
| Task 1 race | guide §7 | `bash run_trial.sh dummy 30 task1-run1`; exact full backing file becomes `111111******333333\n`; owner/mode preserved |
| Task 2 baseline | guide §8 | New lab-only `charlie`, actual nonzero UID, successful normal non-sudo login; backup **after creation**, never overwrite after attack |
| Task 2 race | guide §9 | `bash run_trial.sh passwd 30 task2-run1`; only actual charlie UID digits change to equal-width zeroes |
| Actual privilege | guide §9.1 | Stopped attacker; fresh **non-sudo** `su - charlie`, actual `id`, `id -u` = 0, `whoami`; record login failure if any |
| Restore | guide §9.2 | Exit UID-0 shells; restore `/root/issd-member6-passwd.normal`; compare bytes; fresh charlie login has original nonzero UID |
| Cleanup | guide §13 | No experiment processes/privileged test shells; correct account baseline; known `/zzz` removed; artifacts exported |
| Optional comparison | guide §11; S12 | Separate patched VM, dummy only; valid bounded run and unchanged file plus vendor fix evidence, or explicitly **not performed** |

There are **two official numbered tasks**. The COW control is an explanatory addition. The countermeasure discussion is compulsory; the patched-VM experiment is optional.

## Source and trial audit

The supplied `cow_attack.c` has fixed `dummy`/`passwd` modes, ordinary-identity checks, a bounded pattern search, root-owned/non-writable target validation, `O_RDONLY`, `PROT_READ` with `MAP_PRIVATE`, two worker threads, same-width UID replacement and a 64-bit `off_t` address conversion. `/proc/self/mem` receives the process's virtual address via `pwrite`; the other worker repeatedly applies `MADV_DONTNEED`.

The control uses a writable private mapping and direct `memcpy`; it is not an identical exploit with one worker removed. The supplied build and trial helpers were read in full. The trial records copies/hashes and stops on detected change or its time limit. Its timer is integer Bash wall time; polling is about 0.2 seconds. It does **not** count kernel race attempts. An interrupted run can lack final artifacts; such a run must remain incomplete, with its raw output retained.

Original source hashes are preserved in [lab-files/SOURCE_SHA256SUMS](lab-files/SOURCE_SHA256SUMS). Supplemental helpers add environment guards, metadata and whole-file comparisons around these files. They do not replace the supplied C/build/trial implementation. Their guest runtime remains to be verified.

## Comparison with Member 5

| Aspect | Member 5 | Member 6 |
|---|---|---|
| Flaw | Application `access()` / `fopen()` TOCTOU | Historical kernel COW memory-management race |
| Guest | SEED 20.04, x86-64 | Separate SEED 12.04, 32-bit |
| Privileged victim | Root-owned Set-UID `vulp` installed | Ordinary `cow_attack`; no installed Set-UID victim |
| Account effect | Appends a new `test` UID-0 record | In-place overwrite of existing charlie UID digits |
| Main controls | Least-privilege variant, symlink protection | Normal COW control; primary defence is patched running kernel |
| Measurements | Repeated victim invocations and elapsed time | Elapsed wall seconds, hashes, exact file change; no race-attempt count |
| Evidence numbering | S01–S15, multiple complementary images | M6-S01–M6-S13, S12 optional, a/b suffixes allowed |
| Final organisation | `submission/`, `evidence/`, logs, source and provenance | Follow this pattern with actual M6 artifacts after execution |

Member 5's evidence strengths to retain: named original images, factual captions, exact file comparisons, authentic non-sudo login proof, failure/retry preservation, stopped-process cleanup, and transparent source/image provenance. Its recorded timings, Linux 20.04 binaries, Set-UID/sysctl commands and root-account record are specific to Member 5.

## Report and presentation requirements

`REPORT_TEMPLATE.md` defines: (1) aim/scope; (2) background/security model; (3) actual environment; (4) code/build; (5) Task 1 baseline/control/race; (6) Task 2 normal account/overwrite/login/restoration; (7) countermeasures and optional comparison status; (8) consolidated expected/actual findings; (9) cleanup/conclusion; (10) references/attribution, plus final deliverables.

`PRESENTATION_PLAN.md` defines six main slides: definition; COW/mechanism; environment/protection; short live dummy demonstration; recorded account impact; countermeasures/takeaway. Its 5–7 minutes is a suggestion. The supplied Q&A covers kernel/version choice, local access, mapping semantics, discard/write races, same-width zeroes, UID 0, persistent process credentials and finite negative trials.

The course documents do not specify a deadline, upload location, final format, rubric, personal identity details or exact speaking time. Those remain human/group inputs. Report results and findings slides are blocked until actual M6 VM experiments exist.

## Host findings and current blocker

The original host instructions are Windows-specific. [ARCH_HOST_SETUP.md](ARCH_HOST_SETUP.md) supplies exact Arch paths and installed-version settings while retaining the repository's experiment specification.

* VirtualBox **7.2.20**, DKMS and matching **7.2.9-arch1-1** headers/modules are installed.
* The running Arch kernel is **7.2.8-arch1-2**; its module tree is absent and `/dev/vboxdrv` is absent.
* Required next host step: manually reboot into the already-installed kernel, then check/load the installed VirtualBox module if necessary.
* The verified local ZIP was extracted, the distinct VM was registered, and its clean powered-off snapshot was taken. Guest release/kernel/tool output is still **unobserved**.

## Primary references checked during this audit

* Repository's shared allocation and complete Member 6 pack at the baseline commit.
* [Official lab page](https://seedsecuritylabs.org/Labs_20.04/Software/Dirty_COW/), five-page task PDF and original Labsetup source.
* [Official download page](https://seedsecuritylabs.org/labsetup.html), its linked ZIP and five-page [12.04 manual](https://seedsecuritylabs.org/Labs_12.04/Ubuntu12_04_VM_Manual.pdf).
* [Official upstream task](https://github.com/seed-labs/seed-labs/blob/master/category-software/Dirty_COW/Dirty_COW.tex) and submission instructions.
* Ubuntu's advisory URL returned HTTP 504 during the audit. The [official Ubuntu CVE tracker](https://git.launchpad.net/ubuntu-cve-tracker/plain/retired/CVE-2016-5195) was accessible. It lists `precise_linux` fixed at `3.2.0-115.157`, `precise_linux-lts-trusty` fixed at `3.13.0-100.147~precise1`, and `precise_linux-lts-quantal` ignored/end-of-life. These are separate package families.

SEED text and exploit-pattern attribution: **Wenliang Du / SEED Labs, CC BY-NC-SA 4.0**. This audit and orchestration assistance should be acknowledged in the final report.
