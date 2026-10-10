# Fresh Member 6 run — prompt for Claude Opus 5.5

Act as my technical lab agent and complete my university ISSD Member 6 Dirty COW assignment as far as technically possible, including fresh genuine screenshots, verified results, report and presentation. I am authorised to perform this lab in my isolated disposable SEED VM.

## Execution location

You are running OpenCode on my **Arch Linux host**. The required guest is **32-bit SEED Ubuntu 12.04**. Current OpenCode V2 has no supported Linux i686 build, so operate the guest from the host through a verified VM-control channel. Do not try to solve this by replacing or upgrading the required guest.

Host repository:
`/home/DHB/Downloads/ISSP/ISSD-seed-labs`

Repository origin:
`https://github.com/Eeshan-Vaghjiani/ISSD-seed-labs.git`

VirtualBox VM:
`ISSD-Member6-SEED12`

VM UUID:
`242db196-83e1-4b7a-9f0b-e399d6f8b9dc`

Existing clean snapshot:
`M6-clean-SEED12`

Native guest workspace:
`/home/seed/issd-member6/lab-files`

Execute all experiments and all operations on `/zzz`, `/etc/passwd` and charlie **only inside that VM**. Check whether every tool command executes on HOST or VM before using it. Never run the exploit on Arch, and never modify the host's password file, kernel, boot configuration or user permissions. Explain any necessary host changes under **HOST ACTION**, with exact commands.

## Read the assignment before acting

Use the repository as the authoritative specification. Read these files in full:

* `Member6/README.md`
* `Member6/START_TO_FINISH_GUIDE.md`
* `Member6/REPORT_TEMPLATE.md`
* `Member6/PRESENTATION_PLAN.md`
* `Member6/VERIFICATION.md`
* `Member6/evidence/SCREENSHOT_CHECKLIST.md`
* All four supplied files in `Member6/lab-files/`
* `Member6/OPENCODE_HANDOFF.md` and `Member6/EXECUTION_STATUS.md`
* The shared lecturer allocation in `Member5/course-materials/`

Use the existing repository audit and inspect Member 5's finished submission/evidence to match its organisation and verification quality. Preserve the existing Member 6 material. This is not a request for a generic Dirty COW tutorial.

## Starting point and fresh evidence

The previous session verified/downloaded the official SEED image, configured the VM, took the clean snapshot, booted the guest, checked its environment, copied the four original files onto ext4, and built them. It stopped **before the normal-COW control or either Dirty COW experiment**. Reinspect the live state because I may have changed or reset the VM since then. Avoid repeating the completed image download or VirtualBox installation.

Previous measured guest values were Ubuntu 12.04.2 LTS, i686/32-bit, kernel `3.5.0-37-generic`, package `3.5.0-37.58~precise1`, source package `linux-lts-quantal`, GCC 4.6.3 and seed UID/GID 1000. These are previous observations, not a substitute for this run's verification.

I want **a completely fresh screenshot set**. Save it here on the host:
`/home/DHB/Downloads/ISSP/ISSD-seed-labs/Member6/evidence/incoming/opus-fresh-20261008/`

When the writable M6export share is mounted, the same destination inside the VM is:
`/home/seed/m6-export/opus-fresh-20261008/`

Confirm the share is really mounted before writing. `M6pack` / `~/m6-transfer` is read-only input. Do not run the C programs from either shared folder: use the native guest workspace, and copy/export evidence afterward.

Retain earlier screenshots/logs as previous-session material. Do not count them as fresh evidence. Use fresh trial labels, and do not overwrite any existing run, good account baseline or capture. Preserve useful guest data before any snapshot rollback. Reset only identified lab state, following the repository; inspect unfamiliar files/accounts first.

## Screenshot style and honesty

Use a normal Ubuntu terminal with readable text, a simple solid background and standard prompts. Show short, relevant commands and their actual output. Keep verbose automation traces, JSON, checklists and internal narration out of the screenshot view; retain detailed verification in separate logs.

You may clear the terminal display between checkpoints after the previous output has been saved. Capture the actual command/result again. Do not redraw terminal text, manufacture screenshots, alter a failure into a success, change prompts to imply privilege, or replay an old log while labelling it a new experiment. Preserve failures and use factual captions. Keep source and assistance attribution accurate.

For every experiment maintain **EXPECTED / ACTUAL / EXPLANATION** in the results record. Never substitute expected output for observed output.

## Required practical work

1. Verify actual ordinary identity, release, architecture, running kernel/package, compiler and tools. Use the prescribed historical environment; stop and explain any mismatch. Do not upgrade its kernel.
2. Use the existing `cow_attack.c`, `cow_control.c`, `build.sh` and `run_trial.sh`. Verify source hashes, LF line endings, native filesystem and permissions. Build using `bash build.sh` as ordinary seed. Avoid unnecessary rewrites of these supplied files.
3. Prepare `/zzz` exactly as specified: root:root, 0644, `111111222222333333` plus a newline. Establish that the ordinary user's normal write fails and the original file remains unchanged.
4. Run the supplied normal-COW control. Verify its private-memory result against a fresh backing-file read and the original hash. Explain its writable private mapping versus the exploit's read-only mapping and `/proc/self/mem` path.
5. Perform the supplied bounded Task 1 trial as seed. Verify the **whole actual backing file** becomes the exact expected replacement, with owner/mode retained. Preserve before/after files, hashes, program output and the actual runtime. Record and diagnose unchanged/partial/error outcomes honestly.
6. Create the lab-only charlie account if absent; inspect any existing account first. Record its real original nonzero UID and verify an ordinary non-sudo login. Take the protected baseline only after creation, preserve it without overwriting, and take `M6-charlie-normal-ready` in the documented stopped/normal state.
7. Perform Task 2 as ordinary seed using charlie's actual UID. Verify that only those UID digits changed to the same number of zeroes. A modified file or changed hash does not prove a successful privileged login.
8. Verify a fresh **non-sudo `su - charlie`** followed by actual `id`, `id -u` and `whoami`. Numeric UID 0 is the required privilege evidence. Keep passwords/shadow contents out of screenshots, logs and the repository.
9. Exit every test privileged shell, stop experiment processes, restore the exact normal password-file baseline, and verify a fresh charlie login has the original nonzero UID. Clean/reset the known dummy and temporary state as specified. Preserve the evidence and leave a reproducible VM.

The patched comparison is optional. If not performed, label it **not performed; discussion only**. Do not infer a patched result from an installation or setup failure.

## Fresh screenshot names

Use the checklist's exact checkpoint names in the fresh directory, with a/b suffixes when needed:

* `M6-S01-vm-setup.png`
* `M6-S02-environment.png`
* `M6-S03-code-build.png`
* `M6-S04-dummy-baseline.png`
* `M6-S05-normal-cow.png`
* `M6-S06-task1-running.png`
* `M6-S07-task1-result.png`
* `M6-S08-charlie-baseline.png`
* `M6-S09-task2-uid-change.png`
* `M6-S10-task2-root-proof.png`
* `M6-S11-account-restored.png`
* `M6-S12-patched-comparison.png` only if actually performed
* `M6-S13-cleanup.png`

Use real guest screenshots or `VBoxManage controlvm ... screenshotpng` of the genuine displayed state. The latter cannot capture the HOST VirtualBox settings window for S01; obtain a genuine host capture for that checkpoint. Review every image for readable command/result context and consistency with its logs, not just the filename's existence.

## Report and presentation

Complete the existing report structure using only this run's actual evidence. Explain COW, `MAP_PRIVATE`, read-only mappings, `/proc/self/mem`, `madvise(MADV_DONTNEED)`, race conditions, CVE-2016-5195, normal write denial, UID 0, vulnerable/patched behaviour and the four required countermeasure themes. Do not invent measurements or kernel race-attempt counts; the supplied wrapper measures integer wall seconds.

Prepare the presentation, screenshot order, concise speaker notes, short live dummy-file demo, genuine recorded Task 2 fallback, lecturer Q&A and cleanup/rehearsal instructions. Keep the organisation comparable to `Member5/submission/`. Distinguish live output from recorded evidence. Retain Wenliang Du / SEED Labs attribution and an accurate assistance acknowledgement.

Finish with **CHECKPOINT | STATUS | EVIDENCE | VERIFICATION** for every M6 checkpoint, then Task 1, Task 2 and Environment summaries, plus precise remaining manual actions. Ask for missing course identity/deadline/format/time details when needed; do not invent them or block independent technical work.

## Manual-action protocol

When I must enter a password, click something, capture a host screen, restore a snapshot or intervene, stop and say **MANUAL ACTION REQUIRED** (and **MANUAL ACTION REQUIRED — VIRTUALBOX** for its UI). Give HOST/VM, the exact command/menu/action, expected state, what I should send back, and what happens next. Do not request passwords in chat. Continue independent safe preparation while appropriate.

Start by confirming the actual execution boundary, reading the handoff/specification, checking the current VM state and preparing the fresh capture directory. Then carry out the assignment rather than stopping at a plan.
