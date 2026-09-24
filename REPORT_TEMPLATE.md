# ISSD — Race-Condition Vulnerability Lab report

**Status: TEMPLATE — replace placeholders with your own execution evidence before submission.**

| Field | Details |
|---|---|
| Student name | [INSERT] |
| Student / registration number | [INSERT] |
| Course / unit | ISSD — [INSERT full course title if required] |
| Group / class | [INSERT] |
| Assigned role | Member 5 — Race-Condition Vulnerability Lab |
| Lecturer | [INSERT] |
| Experiment dates | [INSERT] |
| Submission date | [INSERT] |

## 1. Aim and scope

The aim of this lab is to investigate a time-of-check-to-time-of-use (TOCTOU) race in a privileged application, demonstrate its effect on a protected file, and evaluate countermeasures. The work follows the lecturer-linked SEED Ubuntu 20.04 Race-Condition Vulnerability Lab: Task 1, Tasks 2.A–2.C, and Tasks 3.A–3.B.

My division responsibilities are to set up and perform the lab; explain the vulnerability and vulnerable program; document commands and observations; capture setup, execution and result evidence; explain attacker gain and countermeasures; and prepare a short live demonstration.

## 2. Background

A race condition occurs when concurrent operations interact with shared state and the outcome depends on their relative timing. In a TOCTOU vulnerability, a program checks a property of an object, but that property or the object referred to by its pathname can change before use.

The lab program is a root-owned Set-UID executable. When invoked by the ordinary `seed` user, its real UID belongs to `seed` while its effective UID is 0. The program uses `access()` to check the real user's write permission on `/tmp/XYZ`, then uses `fopen()` to open that path with its effective privileges. Because the two calls independently resolve the pathname, an attacker can change the symlink between them.

```text
1. Attacker points /tmp/XYZ to writable /dev/null.
2. Victim's access() check passes as the real user.
3. Attacker changes /tmp/XYZ to /etc/passwd.
4. Victim opens the new target with root-effective privileges.
5. Victim appends attacker-controlled input to the protected file.
```

This is a local privilege-escalation experiment: it assumes an ordinary local user and the deliberately vulnerable privileged executable. It does not demonstrate remote compromise.

## 3. Environment and preparation

| Item | Actual value from my VM |
|---|---|
| Windows host version and architecture | [INSERT] |
| VirtualBox version | [INSERT] |
| VM image | [INSERT downloaded SEED image filename] |
| Guest OS and architecture | [INSERT `lsb_release -a`, `uname -m`] |
| Kernel | [INSERT `uname -r`] |
| VM RAM and CPUs | [INSERT] |
| GCC version | [INSERT] |
| Guest working directory and filesystem | [INSERT] |
| Ordinary user's UID/GID | [INSERT `id` output] |
| Original `fs.protected_symlinks` | [INSERT] |
| Original `fs.protected_regular` | [INSERT] |
| Initial password-file SHA-256 | [INSERT] |
| Snapshot and original-file backup | [INSERT names / paths] |

The files were placed on the VM's native Linux filesystem, rather than compiled or executed from a shared folder. Before the experiments, I [INSERT actual backup/snapshot procedure]. For the attack experiments, `fs.protected_symlinks` and `fs.protected_regular` were set to 0, as required by the Ubuntu 20.04 lab instructions. The sticky bit on `/tmp` was retained.

**[INSERT S01: VM settings. Caption: actual VM resources and attached SEED disk.]**

**[INSERT S02: guest identity, OS, kernel and compiler.]**

**[INSERT S03: protections, sticky bit, root ownership and Set-UID permissions.]**

Important setup commands:

```bash
bash build.sh
sudo sysctl -w fs.protected_symlinks=0
sudo sysctl -w fs.protected_regular=0
ls -l vulp vulp_slow vulp_least
```

The build helper compiles three variants from the same source. It applies root ownership before mode 4755 to the victim executables. The attack programs remain ordinary-user executables. `sudo` is used for lab configuration and restoration, not to run the attacks.

## 4. Vulnerable program and supporting code

Key vulnerable operations:

```c
if (access(fn, W_OK) != 0) {
    puts("No permission");
    return 1;
}
fp = fopen(fn, "a+");
```

Here `fn` is `/tmp/XYZ`. The permission check does not reserve or lock the checked file. The later open may therefore target a different object. Mode `a+` opens for reading/appending and can create a file when the pathname is absent; this matters to Task 2.B's failure case.

The provided adaptation of SEED's program adds checked input/I/O, an optional slow-demonstration delay and a least-privilege variant. The ordinary `vulp` executable has no artificial delay. The maximum input is 50 non-whitespace characters.

**[INSERT S04: readable vulnerable-code excerpt.]**

**[INSERT any additional modifications you made, or state that you used the supplied adaptation unchanged.]**

## 5. Task 1 — target selection and account validation

`/etc/passwd` was chosen because ordinary users cannot write it, and an entry with UID 0 can map an account to root privileges. The proposed record was:

```text
test:U6aMy0wojraho:0:0:test:/root:/bin/bash
```

The seven fields represent username, password hash, UID, GID, comment, home and shell. UID 0 is the source of privilege; the account name is not. The inline legacy hash avoids separately modifying `/etc/shadow` in this teaching example.

**Procedure actually used:** [INSERT commands for manual insertion, `su - test`, `id`, exit and baseline restoration. If the fallback hash was necessary, document it and the reason.]

**Observed login behaviour:** [INSERT whether pressing Enter worked; exact error or successful output.]

**Observed UID:** [INSERT]

**[INSERT S05: manual validation and UID output.]**

This task uses administrator privileges to validate the account record and is **not** evidence of race exploitation. The account was removed by [INSERT restoration method] before Task 2.

## 6. Task 2.A — slow-machine simulation

The slow variant inserts a 10-second delay after the successful permission check. I first pointed `/tmp/XYZ` to `/dev/null`. After starting `./vulp_slow < input.txt`, I changed the symlink to `/etc/passwd` during the delay.

Important commands:

```bash
ln -s /dev/null /tmp/XYZ
./vulp_slow < input.txt
# Other terminal, after the check passes:
ln -sfn /etc/passwd /tmp/XYZ
# After the victim returns:
grep '^test:' /etc/passwd
su - test
id
```

**Actual observations:** [INSERT link targets, success/failure, output and any retries.]

**[INSERT S06: wait message and link replacement.]**

**[INSERT S07: injected account and verified UID result.]**

**Explanation:** The check evaluated the writable target, but the privileged open resolved the same pathname to the protected target. The delay makes the window visible for teaching; it does not represent the genuine no-delay attack. [INSERT a sentence connecting this explanation to your observed output.]

## 7. Task 2.B — genuine no-delay attack

The ordinary `vulp` build was used without `sleep`. The naive attacker repeatedly removed and recreated `/tmp/XYZ`, alternating its target between `/dev/null` and `/etc/passwd`. A separate monitor repeatedly ran the victim with redirected input.

```c
unlink("/tmp/XYZ");
symlink("/etc/passwd", "/tmp/XYZ");
```

These calls are separate operations. The complete attack also switches back to the writable target so that some checks can pass.

```bash
# Terminal A:
./attack_naive
# Terminal B:
bash run_trials.sh ./vulp 300 task2b
```

The helper compared password-file SHA-256 values, stopped on a change and checked for the exact record. A hash change was then independently validated by login and `id` rather than treated as sufficient proof on its own.

| Run / log label | Limit (seconds) | Attempts | Actual elapsed time | Result | Reset / diagnostic |
|---|---|---|---|---|---|
| [INSERT] | [INSERT] | [INSERT] | [INSERT] | [INSERT] | [INSERT] |
| [INSERT if retried] | [INSERT] | [INSERT] | [INSERT] | [INSERT] | [INSERT] |

**[INSERT S08: concurrently running attack and monitor.]**

**[INSERT S09: real-attack result, summary and UID proof.]**

### Sticky-bit failure analysis

**Observed in my runs:** [INSERT yes/no and evidence; do not invent an occurrence.]

**[INSERT S10 if observed; otherwise explicitly state not observed.]**

If the victim opens the path after `unlink()` but before `symlink()`, it can create a root-owned regular file. The sticky bit on `/tmp` prevents the ordinary attacker from removing this file. The naive attack therefore has its own race. If an administrator-assisted reset was needed, it was [INSERT details]. This reset is a limitation of that attempt, not an unprivileged attack operation.

## 8. Task 2.C — atomic-exchange improvement

The improved attacker creates two links during initialization, then repeatedly exchanges them using:

```c
renameat2(AT_FDCWD, "/tmp/XYZ", AT_FDCWD, "/tmp/ABC", RENAME_EXCHANGE);
```

The victim is started only after link initialization. Atomic exchange avoids leaving `/tmp/XYZ` absent during switching and therefore prevents the particular root-owned-file creation gap described above. The victim's separate check and use remain vulnerable.

```bash
# Terminal A:
./attack_atomic
# Terminal B:
bash run_trials.sh ./vulp 300 task2c
```

**Actual attempts / elapsed time / outcome:** [INSERT]

**Exact account and UID verification:** [INSERT]

**[INSERT S11: improved attack, summary and verified outcome.]**

**Comparison with Task 2.B:** [INSERT what changed in your observations; do not infer guaranteed speed from a single timing result.]

## 9. Task 3.A — least-privilege countermeasure

The modified victim temporarily lowers its effective UID with `seteuid(getuid())` before checking or opening the user-selected path. The reduced privilege remains in effect through writing and closing. The saved privileged effective UID is restored only after file work to illustrate the official task; permanent removal is preferable when no further privileged action is needed.

```c
uid_t privileged_euid = geteuid();
/* Check the return value in the complete program. */
seteuid(getuid());
/* access, open, write and close execute with ordinary-user privileges. */
seteuid(privileged_euid);
```

Both OS protection settings were kept at 0 for this test so that the program-level change could be evaluated independently.

```bash
# Terminal A:
./attack_atomic
# Terminal B:
bash run_trials.sh ./vulp_least 300 task3a
```

**Observed duration, attempts, before/after hash and account presence:** [INSERT]

**Observed write to the permitted ordinary-user file:** [INSERT]

**[INSERT S12: modified code, concurrent trial summary and normal-function control.]**

**Conclusion supported by my run:** [INSERT measured observation.] If the symlink resolves to the protected target, the open no longer has root write privileges. A finite unsuccessful attack trial is supporting evidence; the privilege analysis explains why this target write is prevented by the change.

## 10. Task 3.B — Ubuntu symlink protection

The original vulnerable `vulp` binary was tested with `fs.protected_symlinks=1` and `fs.protected_regular=0`. This isolates the symlink protection as the changed control.

```bash
sudo sysctl -w fs.protected_symlinks=1
sudo sysctl -w fs.protected_regular=0
# Terminal A:
./attack_atomic
# Terminal B:
bash run_trials.sh ./vulp 300 task3b
```

**Observed duration, attempts, errors, hashes and account presence:** [INSERT]

**[INSERT S13: control value, original victim, trial result and denied open.]**

With the protection enabled, a symlink may be followed if it is outside a sticky world-writable directory, if its owner's UID matches the follower's filesystem UID, or if its owner matches the containing directory's owner. In this experiment the symlink is owned by `seed`, while the privileged follower and `/tmp` directory are root-owned. The privileged traversal is therefore denied.

This is a context-specific defence against unsafe symlink following, not a universal race-condition solution. It does not make separate pathname checks and uses atomic and does not address every directory context or shared-state race.

## 11. Consolidated results

Fill this table from the recorded runs, not from the predicted results.

| Task | Victim | Symlink / regular settings | Expected behaviour | Actual result and evidence |
|---|---|---|---|---|
| 1 | Manual validation | 0 / 0 | Determine whether proposed login record works | [INSERT] |
| 2.A | `vulp_slow` | 0 / 0 | Manual switch can cause privileged append | [INSERT] |
| 2.B | `vulp` | 0 / 0 | Probabilistic exploitation; naive attacker may stall | [INSERT] |
| 2.C | `vulp` | 0 / 0 | Atomic switching removes attacker-side gap | [INSERT] |
| 3.A | `vulp_least` | 0 / 0 | Protected target not writable by reduced-privilege open | [INSERT] |
| 3.B | `vulp` | 1 / 0 | Privileged symlink traversal blocked in this context | [INSERT] |

## 12. Impact and recommended countermeasures

The intended impact is an unauthorised append to an account database, leading to a login with UID 0. **My demonstrated impact was [INSERT exactly what your evidence establishes].** This illustrates how a local implementation flaw can undermine authentication and access-control assumptions.

Recommended countermeasures:

* **Least privilege:** carry out user-directed file operations without unnecessary root privileges; check failure paths.
* **Secure file handling:** open the intended object once and work through its descriptor, with appropriate validation of the opened object rather than trusting an earlier pathname check.
* **Proper permissions:** protect trusted directories and remove unnecessary Set-UID executables. Target-file permissions alone do not stop a privileged confused deputy.
* **Atomic operations:** combine security-relevant creation/check behaviour where possible, such as exclusive creation, rather than checking a name and later acting on it.
* **Safe temporary files:** use `mkstemp()` and retain its descriptor, preferably in a private directory, instead of predictable names in a shared writable directory.
* **OS hardening:** keep symlink protections enabled as defence in depth, while fixing the application design.

Task 2.C also demonstrates that atomicity can improve an attack: swapping the links atomically fixes the attacker's error without making the victim safe. Therefore, a defence must address the correct security boundary.

## 13. Cleanup

**Actions actually completed:** [INSERT stopped processes; restored original password file; removed test links; restored original sysctl values; removed Set-UID from lab binaries.]

**[INSERT S14: cleanup verification.]**

**Evidence and source backup location:** [INSERT]

## 14. Conclusion

[INSERT a short evidence-led conclusion: which attacks succeeded, which countermeasure outcomes were observed, and any unresolved issue.]

The central lesson is that checking permission on an attacker-changeable pathname does not make a later privileged use of that pathname safe. Correct privilege handling and secure object-based file operations are needed, with operating-system protection providing an additional layer.

## 15. References and attribution

1. Lecturer topic allocation text, `text from division from lec.txt`, supplied course material.
2. Group allocation, `ISSD presentation division .pdf`, Member 5 row.
3. Wenliang Du / SEED Labs, *Race-Condition Vulnerability Lab*: https://seedsecuritylabs.org/Labs_20.04/Software/Race_Condition/
4. Official task PDF: https://seedsecuritylabs.org/Labs_20.04/Files/Race_Condition/Race_Condition.pdf
5. SEED VM setup: https://seedsecuritylabs.org/labsetup.html
6. SEED VirtualBox manual: https://github.com/seed-labs/seed-labs/blob/master/manuals/vm/seedvm-manual.md
7. Linux kernel sysctl filesystem documentation: https://www.kernel.org/doc/html/latest/admin-guide/sysctl/fs.html

Guide references checked on 23 September 2026. My access / experiment date: [INSERT]. The vulnerable-program pattern and task structure are adapted from SEED Labs, Wenliang Du, under CC BY-NC-SA 4.0. [INSERT acknowledgement of assistance as required by course policy.]

## Appendix A — submitted files

* [ ] `vulp.c`, with explanation of all variants and final changes.
* [ ] `attack_naive.c` and `attack_atomic.c`.
* [ ] `build.sh`, `run_trials.sh`, and actual lab `input.txt`.
* [ ] Trial summary logs, with unique labels for retries.
* [ ] Screenshots S01–S14; S10 only if observed; S15 optional.
* [ ] Completed report and presentation segment.

## Appendix B — short demo reference

Presentation order and actual rehearsed timing: [INSERT].

Location of recorded no-delay attack evidence: [INSERT].

Demo fallback if a live race does not finish: [INSERT the real evidence you will show and how you will identify it as recorded].
