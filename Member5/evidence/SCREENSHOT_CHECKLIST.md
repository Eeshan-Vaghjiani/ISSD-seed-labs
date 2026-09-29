# Evidence checklist — capture during your own VM run

Store PNGs in this folder. For a large evidence checkpoint, use suffixes such as `S11a-...png` and `S11b-...png`. These entries are **placeholders, not completed observations**.

| Done | ID / suggested filename | When | What must be visible |
|---|---|---|---|
| [ ] | `S01-vm-setup.png` | After configuring VirtualBox | VM name, memory/CPU and attached SEED virtual disk |
| [ ] | `S02-guest-environment.png` | First guest checks | Ubuntu version, kernel, GCC and ordinary-user identity |
| [ ] | `S03-lab-permissions.png` | After building and disabling lab controls | Root-owned Set-UID victims, controls at 0, sticky bit on `/tmp` |
| [ ] | `S04-vulnerable-code.png` | Before Task 1 | Readable `access()` and `fopen()` operations |
| [ ] | `S05-task1-target-validation.png` | During Task 1 | Manual validation labelled as such, login behaviour, `id` |
| [ ] | `S06-task2a-timing.png` | During the 10-second delay | Check-passed message and link changed to target |
| [ ] | `S07-task2a-result.png` | After slow victim finishes | Record created through victim and verified UID 0 |
| [ ] | `S08-task2b-running.png` | During real naive race | Attacker/monitor running without sudo, progress/status |
| [ ] | `S09-task2b-result.png` | At genuine no-delay success | Exact record, actual summary, login and UID 0 |
| [ ] | `S10-task2b-sticky-bit.png` | If naive attacker encounters the failure | Root-owned regular file, unlink error and `/tmp` mode; if absent, state not observed |
| [ ] | `S11-task2c-atomic-result.png` | During/after improved run | Atomic method, actual summary and verified result |
| [ ] | `S12-task3a-least-privilege.png` | After fixed-program experiment | Fix excerpt, settings 0/0, trial summary, unchanged target and allowed write |
| [ ] | `S13-task3b-symlink-protection.png` | After OS-defence experiment | Original victim, settings 1/0, summary, denied open and unchanged target |
| [ ] | `S14-cleanup.png` | At end | Restored controls/password file, removed test account/Set-UID bits |
| [ ] | `S15-deliverables.png` | Optional final check | Organised evidence, logs and source files |

## Caption template

**Figure [INSERT] — [TASK].** I ran `[COMMAND]` in `[ENVIRONMENT]`. The output showed `[ACTUAL OBSERVATION]`. This supports `[SPECIFIC CONCLUSION]` because `[REASON]`.

## Additional items to save

* Actual `logs/*-summary.txt` files, with unique run labels for retries.
* Last-output logs where they help explain a failure or blocked operation.
* The exact final source files and `input.txt` used.
* Original and experiment sysctl values and environment versions.
* Written attempts/time/outcome notes for each task.
* A short recording of a genuine no-delay success, if useful for presentation backup.

Capture command and result together; a terminal that only shows `uid=0` without the preceding attack/login context is weak evidence. Do not substitute administrator login output for exploit proof.
