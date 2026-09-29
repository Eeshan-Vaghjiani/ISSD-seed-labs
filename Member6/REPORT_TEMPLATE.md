# ISSD — Dirty COW Attack Lab report

**TEMPLATE: explanations are drafted; insert your own measurements, screenshots and observations. No experiment result is preclaimed.**

| Field | Details |
|---|---|
| Name / registration number | [INSERT] |
| Course / class / group | ISSD — [INSERT] |
| Assigned role | Member 6 — Dirty COW Attack Lab |
| Lecturer | [INSERT] |
| Experiment date(s) | [INSERT] |
| Submission date | [INSERT] |

## 1. Aim and scope

The aim is to understand and reproduce the historical Linux Dirty COW vulnerability, CVE-2016-5195, in the prescribed SEED VM. The official tasks are to modify a dummy file not writable by an ordinary user and to modify a test account's UID to demonstrate root privilege. My group division also requires explanation of copy-on-write, important commands/code, environment/attack/result screenshots, countermeasures and a short live demonstration.

## 2. Background and security model

Copy-on-write allows pages to be shared until modification requires a private copy. A private file mapping must not allow changes to its private page to alter the backing file. Dirty COW violated this boundary in affected kernels through a race involving COW handling and memory operations.

The attack opens its target read-only and creates a private read-only mapping. One worker repeatedly writes to its own mapped memory through `/proc/self/mem`, while another repeatedly applies `MADV_DONTNEED` to the mapping. The vulnerable kernel may incorrectly allow a write to affect the backing file rather than only the private copy.

```text
Normal COW:   private write -> private page changes -> file unchanged
Dirty COW:    memory write races mapping discard -> vulnerable COW handling
              -> backing file changes despite ordinary file permissions
```

This is a **local kernel privilege-escalation vulnerability**, not a remote attack and not an application-level symlink TOCTOU bug. No deliberately installed root-owned Set-UID victim is required. Restrictive permissions on the target are part of the evidence: they demonstrate the protection the kernel flaw undermines.

## 3. Environment and research-based choice

The official Dirty COW page is located under a `Labs_20.04` URL, but explicitly specifies the **SEED Ubuntu 12.04 VM**. Its historical manual describes a 32-bit guest with kernel 3.5.0-37-generic. The SEED Ubuntu 16.04 and 20.04 environments contain the fix and are not the vulnerable demonstration environment.

| Item | Actual value |
|---|---|
| Host architecture / OS | [INSERT] |
| VirtualBox version | [INSERT] |
| SEED image filename and download source | [INSERT] |
| Guest release (`lsb_release -a`) | [INSERT] |
| Running kernel (`uname -r`) | [INSERT] |
| Kernel package version | [INSERT] |
| Guest architecture (`uname -m`) | [INSERT] |
| RAM / virtual CPUs | [INSERT] |
| GCC version | [INSERT] |
| Ordinary user and numeric UID | [INSERT] |
| Guest working directory/filesystem | [INSERT] |
| Clean snapshot name | [INSERT] |
| Prepared normal-charlie snapshot | [INSERT] |

Kernel vulnerability is assessed using the actual package family and vendor information, not merely the OS release or a simplistic comparison with a single version number. For example, the Ubuntu advisory's fixed version 3.2.0-115.157 applies to a particular Ubuntu 12.04 kernel stream and is not a universal threshold for every kernel family.

**[INSERT M6-S01 — VM setup and disk.]**

**[INSERT M6-S02 — actual guest identity, release, kernel and compiler.]**

Preparation performed: [INSERT file-transfer method, snapshot and any tool installation/issues].

## 4. Code and build

Important compilation commands:

```bash
gcc -std=gnu99 -Wall -Wextra -O2 -pthread cow_attack.c -o cow_attack
gcc -std=gnu99 -Wall -Wextra -O2 cow_control.c -o cow_control
```

The main attack operations are:

```c
open(path, O_RDONLY);
mmap(NULL, mapping_size, PROT_READ, MAP_PRIVATE, fd, 0);
/* Separate concurrent worker operations: */
pwrite(mem_fd, replacement, replacement_size, memory_address);
madvise(mapping, mapping_size, MADV_DONTNEED);
```

The complete submitted code checks return values. `memory_address` is a **virtual address inside this process**, not an offset directly into the protected file. `/proc/self/mem` refers to the attacker's own process memory. The two workers race kernel operations; the program is not granted ordinary write permission to the target.

This pack's adaptation of SEED's example uses bounded pattern searching, checked setup operations, correct-width address conversion, fixed task modes, same-length UID replacement and a shell wrapper that limits duration. It uses `pwrite()` in place of the original separate `lseek()`/`write()` pair while preserving the same memory-write mechanism. It does not use the helper's observation loop as a substitute for explaining the race.

**[INSERT M6-S03 — build and readable main/write/madvise excerpts.]**

My modifications to the supplied adaptation: [INSERT, or state none].

## 5. Task 1 — dummy file

### 5.1 Starting permissions and denied normal write

I created the root-owned `/zzz` file with mode 0644 and initial content `111111222222333333`. Mode 0644 permits the owner to write and ordinary users to read. The target is “read-only” relative to the ordinary attacker, not necessarily a read-only-mounted filesystem.

```bash
sudo sh -c 'printf "111111222222333333\n" > /zzz'
sudo chown root:root /zzz
sudo chmod 0644 /zzz
echo 99999 > /zzz
cat /zzz
ls -l /zzz
```

Actual ordinary write result and starting hash: [INSERT].

**[INSERT M6-S04 — permissions, direct write denied and unchanged file.]**

### 5.2 Normal copy-on-write control

The additional `cow_control` demonstration opens the file read-only but maps it with `PROT_READ | PROT_WRITE` and `MAP_PRIVATE`. It writes only to its private mapping. This differs from the exploit's read-only mapping and `/proc/self/mem` write path and is used to explain normal COW semantics.

```bash
./cow_control
cat /zzz
sha256sum /zzz
```

Actual private-memory output: [INSERT].

Actual file output and hash: [INSERT].

**[INSERT M6-S05 — private content changed while backing file stayed unchanged.]**

Interpretation linked to my output: [INSERT].

### 5.3 Race execution

```bash
id
bash run_trial.sh dummy 30 task1-run1
cat logs/task1-run1-summary.txt
cat /zzz
ls -l /zzz
```

| Run label | Runtime limit | Actual elapsed time | Actual full file result | Errors / notes |
|---|---|---|---|---|
| [INSERT] | [INSERT] | [INSERT] | [INSERT] | [INSERT] |
| [INSERT retry if any] | [INSERT] | [INSERT] | [INSERT] | [INSERT] |

**[INSERT M6-S06 — ordinary-user attack execution and summary.]**

**[INSERT M6-S07 — exact before/after change and unchanged restrictive permissions.]**

Expected complete result: `111111******333333`. My observed result: [INSERT].

The wrapper's elapsed time measures wall time, not the exact number of kernel race attempts. It stops on a detected file change or timeout. I checked the actual full content because a changed hash alone could represent a partial or unintended change.

### 5.4 Why this result matters

[INSERT an evidence-led explanation: ordinary write denied, normal private copy did not change file, race produced or failed to produce exact backing-file change, relationship to the vulnerable kernel.]

Reset between attempts was performed by [INSERT]. Administrator writes used for setup/reset are distinguished from the ordinary-user attack.

## 6. Task 2 — account UID modification

### 6.1 Create a normal account and back up

I used the new lab account `charlie` rather than modifying `seed`. The seven password-file fields are username, password reference, UID, GID, comment, home and shell. The `x` password field refers to the existing shadow entry; no password hash was overwritten in this task.

```bash
sudo adduser charlie
grep '^charlie:' /etc/passwd
su - charlie
id
exit
```

Original complete charlie record: [INSERT].

Original numeric UID/GID and pre-attack login result: [INSERT].

The original example uses UID 1001, but my actual UID was [INSERT]. The restorable `/etc/passwd` baseline was captured **after** charlie was created with this normal UID, using [INSERT path and commands].

**[INSERT M6-S08 — ordinary account, nonzero UID and baseline evidence.]**

### 6.2 Perform the overwrite

```bash
id
bash run_trial.sh passwd 30 task2-run1
grep '^charlie:' /etc/passwd
diff -u logs/task2-run1-before.txt logs/task2-run1-after.txt
```

The program identifies charlie's exact record and replaces only the UID digits with the same count of zeroes. For a four-digit UID, `1001` becomes `0000`. This preserves file length and separators. Replacing the text with a single zero without shifting the remaining bytes would be incorrect for an in-place overwrite.

| Run label | Limit / actual seconds | Before UID | After UID | Other differences / errors |
|---|---|---|---|---|
| [INSERT] | [INSERT] | [INSERT] | [INSERT] | [INSERT] |

**[INSERT M6-S09 — run summary and full exact diff.]**

### 6.3 Verify new login privileges

```bash
su - charlie
id
id -u
whoami
```

Actual output: [INSERT].

**[INSERT M6-S10 — non-sudo login followed by numeric UID proof.]**

UID 0 gives root privileges regardless of the account name. `whoami` may resolve UID 0 to `root` even after `su - charlie`. Charlie's GID may remain unchanged. Modifying the database does not automatically change the credentials of the already-running seed shell; a new login applies the new account UID.

Conclusion warranted by my evidence: [INSERT whether protected-file modification and root privilege were both demonstrated, or which remains unresolved].

### 6.4 Restore normal identity

I stopped the attack, exited all root/charlie shells, restored the post-adduser normal-account baseline and verified a fresh ordinary-charlie login. Actual commands and result: [INSERT].

**[INSERT M6-S11 — restoration and new nonzero-UID login.]**

Restoring `/etc/passwd` does not revoke an already running root process's credentials, so ending the test sessions is part of cleanup.

## 7. Countermeasures

| Measure | How it addresses the threat | Limitations |
|---|---|---|
| Kernel patching | Correct COW handling prevents this historical write-privilege bypass | Confirm the fixed kernel is actually running, not merely installed |
| System updates and supported OS | Maintain vendor fixes and replace obsolete systems | An isolated vulnerable teaching snapshot is not a production deployment model |
| Limit local access / untrusted code | Reduce opportunities to execute a local exploit | Does not repair the kernel; remote compromise may provide a local foothold |
| Monitor escalation and file integrity | Detect new UID-0 identities, account changes and suspicious sessions | Memory-path modifications may not look like ordinary target-file writes in audit records |

Example monitoring queries:

```bash
awk -F: '$3 == 0 {print $1 ":" $3 ":" $7}' /etc/passwd
sha256sum /etc/passwd
sudo tail -n 30 /var/log/auth.log
```

Monitoring output I actually examined: [INSERT, or state discussion only]. Authentication logs may show the login, not the underlying race itself. Standard permissions and removing unrelated Set-UID bits are not substitutes for a kernel fix.

### Optional patched-VM comparison

Status: [PERFORMED / NOT PERFORMED — choose one].

If performed, record:

| Item | Actual observation |
|---|---|
| Patched VM release / kernel / package | [INSERT] |
| Advisory evidence for fix | [INSERT] |
| Dummy baseline and successful compilation | [INSERT] |
| Trial duration / errors / final content | [INSERT] |

**[INSERT M6-S12 if performed; otherwise state not collected.]**

This comparison repeats only the dummy-file attack. An unchanged file during a bounded run is an observation, not universal proof. A setup failure is not equivalent to observing corrected COW behaviour. The vendor advisory and mechanism explain the intended security property.

## 8. Consolidated findings

| Experiment | Expected outcome | Actual outcome | Evidence |
|---|---|---|---|
| Ordinary write to root-owned dummy | Denied | [INSERT] | [INSERT] |
| Normal private COW control | Private memory changes; backing file unchanged | [INSERT] | [INSERT] |
| Dirty COW dummy race | Exact replacement possible on vulnerable kernel | [INSERT] | [INSERT] |
| Charlie UID overwrite | Same-length UID digits become zeroes | [INSERT] | [INSERT] |
| Fresh charlie login | UID 0 if overwrite successful | [INSERT] | [INSERT] |
| Optional patched comparison | Backing file remains unchanged | [INSERT / not performed] | [INSERT] |

Interesting failures, partial writes, retries or environment differences: [INSERT].

## 9. Cleanup and conclusion

Actual cleanup: [INSERT stopped processes, ended privileged sessions, normal UID restored, dummy file removed, optional lab-account deletion or snapshot rollback].

**[INSERT M6-S13 — cleanup.]**

Conclusion: [INSERT a short paragraph tied to actual evidence: completed tasks, verified impact, limitations, and why patching the kernel is the primary defence].

Connection to the authentication presentation: account databases are part of the trust assumptions behind login. A kernel write-protection bypass can alter those assumptions by giving an existing account UID 0 without changing its password.

## 10. References and attribution

1. Lecturer text and group division PDF in `../Member5/course-materials/`, Member 6 row.
2. Wenliang Du / SEED Labs, Dirty COW lab: https://seedsecuritylabs.org/Labs_20.04/Software/Dirty_COW/
3. Official task PDF: https://seedsecuritylabs.org/Labs_20.04/Files/Dirty_COW/Dirty_COW.pdf
4. Original source: https://github.com/seed-labs/seed-labs/blob/master/category-software/Dirty_COW/Labsetup/cow_attack.c
5. VM downloads: https://seedsecuritylabs.org/labsetup.html
6. Historical VM manual: https://seedsecuritylabs.org/Labs_12.04/Ubuntu12_04_VM_Manual.pdf
7. Ubuntu advisory: https://ubuntu.com/security/CVE-2016-5195
8. mmap/madvise manual pages: https://man7.org/linux/man-pages/man2/mmap.2.html and https://man7.org/linux/man-pages/man2/madvise.2.html

Research checked 29 September 2026. My own access/experiment dates: [INSERT]. SEED task/exploit-pattern adaptation attributed to Wenliang Du, CC BY-NC-SA 4.0. Assistance acknowledgement as required by the course: [INSERT].

## Appendix — final deliverables

* [ ] Completed report with captions and actual observations.
* [ ] Final `cow_attack.c`, `cow_control.c`, `build.sh`, `run_trial.sh` and explanation of changes.
* [ ] Actual run logs/diffs and named screenshots.
* [ ] Slide segment and short demo, with saved real-run evidence.
* [ ] All placeholders replaced or explicitly identified as not performed/unresolved.
* [ ] Deadline, report format and group handoff confirmed.
