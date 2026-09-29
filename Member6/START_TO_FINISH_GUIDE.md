# Member 6 — complete Dirty COW lab guide

**Start here.** This guide covers your Member 6 allocation and the two official SEED Dirty COW tasks, from installing the VM to reporting and presenting your results.

**Important:** use the **SEED Ubuntu 12.04 32-bit image**, not Member 5's Ubuntu 20.04 VM. Dirty COW is a kernel bug fixed in 2016. Disabling Member 5's symlink controls on a patched kernel does not bring it back.

All commands below run **inside the Ubuntu 12.04 VM**, except blocks explicitly marked **Windows PowerShell**. `[INSERT ...]` means a placeholder for your evidence; do not type it into a terminal. Execute this on your disposable SEED VM: it deliberately modifies protected guest files.

## 1. Your exact scope

| Member 6 division requirement | Where this guide covers it | What you produce |
|---|---|---|
| Set up and perform Dirty COW | Sections 3–9 | Correct old VM, dummy-file and account experiments |
| Explain Dirty COW and copy-on-write | Section 2 | Definition, diagram and normal-COW control |
| Show modification of protected/read-only data | Sections 6–9 | Ordinary write denied; race-induced content change |
| Follow lab procedure and document commands | Sections 4–10 | Commands, source excerpts, logs and report |
| Screenshots of environment, attack and final result | M6-S01–M6-S13 checkpoints | Named evidence files |
| Explain result and why system was vulnerable | Sections 2, 8, 9 and 11 | Kernel race, not application Set-UID behaviour |
| Discuss patching, updates, local access and monitoring | Section 11 | Countermeasure table and optional comparison |
| Short live demonstration | Section 14 and presentation plan | Rehearsed dummy-file demo plus real UID evidence |

The official lab consists of **Task 1: Modify a Dummy Read-Only File** and **Task 2: Modify the Password File to Gain the Root Privilege**. It has no separate Task 3 countermeasure experiment. This guide includes the division's required defence discussion, a simple COW control, and an optional patched-VM test for stronger explanation.

Your course files are in `../Member5/course-materials/`. They do not specify the deadline, slide count, report format, rubric or personal speaking time. Confirm and fill these:

* Submission deadline and upload location: [INSERT]
* Individual report or combined group report: [INSERT]
* Required format / file name: [INSERT]
* Presentation date and personal allowance: [INSERT]
* Additional lecturer/LMS instructions: [INSERT]

## 2. Understand what you will demonstrate

### 2.1 Copy-on-write, normally

Copy-on-write (COW) lets the operating system share a physical memory page until a process needs to modify its private view. The kernel then gives the writer a private copy. For a `MAP_PRIVATE` file mapping, changes to that private copy must not become writes to the underlying file.

```text
Normal operation
Backing file page <--- process's private file mapping initially refers here
                            |
                      private write
                            v
                    private copied page changes
                    backing file remains unchanged
```

A direct C assignment into a `PROT_READ` mapping normally faults. The SEED attack instead writes through `/proc/self/mem`, the interface to **its own process memory**, while racing kernel COW handling. It does not open `/etc/passwd` for writing in the normal way.

### 2.2 Dirty COW — CVE-2016-5195

Dirty COW is a local privilege-escalation vulnerability in historical Linux kernel handling of private read-only mappings. The flaw lets an unprivileged local process cause changes to a file it can read but cannot normally write.

The attack has three threads of execution:

1. **Main thread:** open the target `O_RDONLY`, map it `PROT_READ | MAP_PRIVATE` (these are separate arguments to `mmap`, not one bitmask), locate the intended bytes, and create two worker threads.
2. **Writer thread:** repeatedly write replacement bytes through `/proc/self/mem` at the virtual address of those mapped bytes.
3. **Discard thread:** repeatedly call `madvise(mapping, size, MADV_DONTNEED)` to discard the private mapping's current page state and cause refault/repopulation.

```text
Writer thread                           Discard thread
------------                            --------------
Requests a write to private mapping      MADV_DONTNEED on the mapping
Kernel handles COW / page lookup         Mapping state changes concurrently
        \                               /
         ---- vulnerable kernel race ---
                |
                v
        backing file page can be changed
        despite lack of file write permission
```

This diagram is a high-level explanation, not a line-by-line kernel execution trace. Neither “a private mapping exists” nor “madvise runs” alone implies a vulnerability. The kernel must mishandle their concurrent interaction with the memory write. The fixed kernel preserves the required COW semantics.

### 2.3 Difference from Member 5

| Aspect | Member 5 | Member 6 |
|---|---|---|
| Bug location | Deliberately vulnerable application | Historical Linux kernel memory management |
| Main mechanism | Symlink swap between `access()` and `fopen()` | Memory-write/COW/discard race |
| Required image | SEED Ubuntu 20.04 | SEED Ubuntu 12.04, vulnerable kernel |
| Root-owned Set-UID victim installed? | Yes | **No** |
| Key defence | Secure file operations, least privilege, symlink protection | Fixed kernel booted and maintained |
| Account experiment | Append a UID-0 record | Change existing `charlie` UID digits in place |

## 3. Install the right VM on Windows

### 3.1 Downloads and requirements

* Install **Oracle VirtualBox for Windows hosts** from https://www.virtualbox.org/wiki/Downloads if Member 5 has not already installed it.
* Open https://seedsecuritylabs.org/labsetup.html and scroll to **Ubuntu 12.04 VM**.
* Download **`SEEDUbuntu12.04.zip`** from the official linked mirror: https://seed.nyc3.cdn.digitaloceanspaces.com/SEEDUbuntu12.04.zip
* Read the historical VM manual: https://seedsecuritylabs.org/Labs_12.04/Ubuntu12_04_VM_Manual.pdf
* Official task sheet: https://seedsecuritylabs.org/Labs_20.04/Files/Dirty_COW/Dirty_COW.pdf
* Official source ZIP: https://seedsecuritylabs.org/Labs_20.04/Files/Dirty_COW/Labsetup.zip

Use an Intel/AMD Windows host with hardware virtualisation enabled. In Task Manager → Performance → CPU check **Virtualisation: Enabled**. Enable VT-x/AMD-V/SVM through manufacturer UEFI instructions if necessary.

Suggested allocation: **1–2 GB RAM and 2 virtual CPUs** for this old guest, within your host's capacity. The historical image manual specifies 1024 MB RAM and a virtual disk maximum of 80 GB. Actual host storage consumption depends on image format and snapshots; allow space for the ZIP, extracted disk and snapshot growth, not just the compressed download. This is a 32-bit guest even on a 64-bit Windows host.

The old manual's original kernel is **3.5.0-37-generic**. Record `uname -r` rather than assume your downloaded or previously updated image has that kernel. Ubuntu's advisory lists fixes by kernel package family: for example, Ubuntu 12.04's `linux` 3.2 stream was fixed at **3.2.0-115.157**. That version must not be treated as a universal comparison threshold for all 3.5/3.13/HWE kernels. Vendor backports mean version family and package status matter.

### 3.2 Create the VM

1. Extract `SEEDUbuntu12.04.zip` into a permanent Windows folder such as `D:\VMs\SEEDUbuntu12.04`.
2. Optional **Windows PowerShell** transfer-integrity comparison:

```powershell
Get-FileHash "$env:USERPROFILE\Downloads\SEEDUbuntu12.04.zip" -Algorithm MD5
```

The download page publishes **`6ec9c429a2f4a9163530ada20f0621dc`**. Use this to detect a changed/corrupt download, not as a modern authenticity guarantee. Download through the official HTTPS-linked source.

3. In VirtualBox, choose **New**; name it `ISSD-Member6-SEED12`; select Linux → **Ubuntu (32-bit)**. Skip unattended installation/ISO selection: this is a preinstalled disk.
4. Choose **Use existing virtual hard disk** and select the extracted virtual disk. Inspect the archive's actual extension: attach its `.vmdk` or `.vdi` through Storage if the wizard differs. A `.vbox` is a VM configuration, not a disk; an `.ova`, if provided, uses Import Appliance. Do not replace the prebuilt disk with an empty one.
5. Set RAM/CPU as above. Start with the Linux guest graphics default (commonly VMSVGA), 64 MB video RAM and 3D acceleration off. Old Guest Additions may not match modern VirtualBox; use a basic display without 3D if needed. Do not assume the historical screenshot menus match your host version.
6. Use NAT only if downloads are needed; no port forwarding or bridged networking is needed. After file transfer, disconnect the virtual network cable for the experiments. The lab is local and the image intentionally contains an obsolete kernel.
7. Boot and log in as **`seed`**, password **`dees`**. This password also works for `sudo`. The manual documents a separate root password `seedubuntu`; root login is not needed for executing the attack.
8. Take a clean snapshot **`M6-clean-SEED12`** before changing target files or accounts. A snapshot is your complete rollback, including account/group/shadow changes.

**M6-S01 — screenshot now:** VirtualBox VM name, RAM/CPU, guest type and attached disk. Save `M6-S01-vm-setup.png` (use a/b suffixes for multiple screens).

No Docker, Kali, WSL installation, paid tools, Set-UID victim or `fs.protected_symlinks=0` change is required. Containers share a host kernel; an Ubuntu 12.04 container on a patched host does not supply a vulnerable Ubuntu 12.04 kernel.

## 4. Guest checks, tools and file transfer

Open an Ubuntu terminal with Ctrl+Alt+T:

```bash
whoami
id
lsb_release -a
uname -r
uname -m
gcc --version
command -v gcc bash timeout unzip wget nano
dpkg-query -W "linux-image-$(uname -r)"
```

Expected: `seed`, nonzero UID, Ubuntu 12.04, a 32-bit architecture such as `i686`, and the intended old kernel. A VM's OS release string alone does not establish vulnerability.

**M6-S02 — screenshot now:** identity, guest release, running kernel/package and compiler. Save `M6-S02-environment.png`. Record actual values in the report.

### 4.1 Tools

The SEED image should already have GCC and the needed development tools. Pthreads are part of the C/POSIX environment; `-pthread` enables the compiler/linker settings. Check before installing anything.

If a required tool is missing and the image's repositories still work:

```bash
sudo apt-get update
sudo apt-get install build-essential unzip wget nano
```

Ubuntu 12.04 is end-of-life, so archive repositories/TLS can fail. Do not run a full upgrade on the vulnerable demonstration image or change it to Ubuntu 20.04 to solve a tool issue. If normal precise repositories return 404, back up `/etc/apt/sources.list`, inspect it with `nano`, and use the Ubuntu old-releases archive for the matching **precise** release only. Example archive lines are:

```text
deb http://old-releases.ubuntu.com/ubuntu/ precise main restricted universe multiverse
deb http://old-releases.ubuntu.com/ubuntu/ precise-updates main restricted universe multiverse
deb http://old-releases.ubuntu.com/ubuntu/ precise-security main restricted universe multiverse
```

Archive package signatures must still be validated; do not bypass signature verification to make an unexplained error disappear. Prefer the original prebuilt image with its compiler present. If old guest HTTPS fails, download the PDF/ZIP on Windows and transfer them instead of disabling TLS verification globally.

### 4.2 Copy the pack to native guest storage

In VirtualBox Settings → Shared Folders, add this Windows **`Member6`** folder as a read-only share named **`M6pack`**. Boot the guest, then:

```bash
mkdir -p ~/m6-transfer ~/issd-member6/lab-files ~/issd-member6/reference ~/issd-member6/evidence
sudo mount -t vboxsf M6pack ~/m6-transfer
cp -R ~/m6-transfer/lab-files/. ~/issd-member6/lab-files/
cd ~/issd-member6/lab-files
chmod 700 ~/issd-member6 ~/issd-member6/lab-files
sed -i 's/\r$//' *.sh *.c
pwd
df -T .
ls -l
```

Work at **`/home/seed/issd-member6/lab-files`** on the guest Linux filesystem. The official lab says not to unzip or run the lab from a host-shared folder. Use the share only for copying.

If the old Guest Additions cannot mount `vboxsf`, copy the files through a USB drive or a temporary file-transfer method, or paste each source file into `nano` in the guest. Do not make upgrading the vulnerable kernel a prerequisite for shared-folder convenience.

### 4.3 Download/read the official lab materials

If guest HTTPS works:

```bash
cd ~/issd-member6/reference
wget -O Dirty_COW.pdf https://seedsecuritylabs.org/Labs_20.04/Files/Dirty_COW/Dirty_COW.pdf
wget -O Labsetup.zip https://seedsecuritylabs.org/Labs_20.04/Files/Dirty_COW/Labsetup.zip
unzip -l Labsetup.zip
unzip Labsetup.zip
find . -name cow_attack.c -print
```

Otherwise download these on Windows, copy them into this guest `reference` folder, and execute the `unzip` commands there. Inspect the original source at the path printed by `find`. Keep it separate from this pack's explained adaptation.

## 5. Build and understand which file runs

```bash
cd ~/issd-member6/lab-files
bash build.sh
nl -ba cow_attack.c
```

The important compilation commands are:

```bash
gcc -std=gnu99 -Wall -Wextra -O2 -pthread cow_attack.c -o cow_attack
gcc -std=gnu99 -Wall -Wextra -O2 cow_control.c -o cow_control
```

**Do not use `sudo ./cow_attack`, change it to root-owned Set-UID, or chmod the target writable.** Dirty COW is demonstrated by an ordinary program exploiting the kernel. Administrator privileges are only used to create the lab targets and reset them.

| File / command | Purpose |
|---|---|
| `cow_control.c` → `./cow_control` | Normal private-copy control; changes process memory but not `/zzz` |
| `cow_attack.c` → `./cow_attack dummy` | Task 1; `/zzz`, `222222` → `******` |
| `./cow_attack passwd 1001` | Task 2 direct invocation example; use charlie's actual UID, not an assumed 1001 |
| `bash run_trial.sh dummy 30 task1-run1` | Recommended Task 1 run, automatically limited to 30 seconds |
| `bash run_trial.sh passwd 30 task2-run1` | Recommended Task 2 run; reads actual charlie UID before starting |
| `logs/<label>-summary.txt` | Identity, kernel, hashes, runtime and change status |
| `logs/<label>-program.txt` | Program output/errors |
| `logs/<label>-before.txt`, `-after.txt` | Target copies for exact diff; in Task 2 these contain the guest's public account records |

The helper polls the file hash about every 0.2 seconds and stops the process on a detected change or timeout. The attacker has two threads in one process; stopping that process stops both. It records wall time, **not a kernel-level count of race attempts**. A change may be partial, so always inspect the full result.

Adaptation details to mention in your report:

* Fixed task modes, rather than a generic arbitrary-target exploit.
* A bounded `memmem()` search instead of assuming a mapped file is NUL-terminated for `strstr()`.
* `/proc/self/mem` writes via `pwrite()` instead of separate `lseek()` and `write()`; the private memory address is still the destination.
* `_FILE_OFFSET_BITS=64` and `uintptr_t` conversion so a 32-bit virtual address is not sign-truncated into a file offset.
* Checked setup errors and target/UID validation.
* The wrapper bounds the upstream infinite race loops and logs observable outcomes.

**M6-S03 — screenshot now:** build output, ordinary ownership/mode and key COW/write/madvise code excerpts. Save `M6-S03-code-build.png`, with suffixes for readable code sections.

## 6. Task 1 preparation — root-owned dummy file

First check that `/zzz` is not an unrelated existing file:

```bash
ls -l /zzz
```

On a clean VM it should be absent. If it exists from an earlier attempt, inspect/reset that known lab file; preserve it if its origin is unknown. Create the official dummy target:

```bash
sudo sh -c 'printf "111111222222333333\n" > /zzz'
sudo chown root:root /zzz
sudo chmod 0644 /zzz
cat /zzz
ls -l /zzz
echo 99999 > /zzz
cat /zzz
sha256sum /zzz
```

The ordinary `echo` redirection must fail with **Permission denied**, and the original content must remain. Mode 0644 means root can write, while normal users can only read; this is not a read-only-mounted filesystem.

**M6-S04 — screenshot now:** root ownership, mode, starting content, denied ordinary write and unchanged content. Save `M6-S04-dummy-baseline.png`.

### 6.1 Normal-COW control (explanatory addition)

```bash
./cow_control
cat /zzz
sha256sum /zzz
```

Expected private memory: `111111******333333`; expected backing file: `111111222222333333`. The control deliberately uses **`PROT_READ | PROT_WRITE` and `MAP_PRIVATE`** to demonstrate normal COW through a direct memory write. The attack uses a **read-only mapping and `/proc/self/mem`** instead. Explain this distinction rather than calling the control a byte-for-byte version of the exploit without its second thread.

**M6-S05 — screenshot now:** different private-memory and file content, unchanged file hash. Save `M6-S05-normal-cow.png`.

## 7. Task 1 — run the dummy-file race

In a terminal at `~/issd-member6/lab-files`:

```bash
id
bash run_trial.sh dummy 30 task1-run1
cat logs/task1-run1-summary.txt
cat /zzz
ls -l /zzz
```

If you want to see the worker process while it runs, use a second terminal:

```bash
pgrep -a -x cow_attack
```

**M6-S06 — screenshot while running or immediately after:** ordinary identity, invocation, memory-mapping details and actual summary. Save `M6-S06-task1-running.png`.

Check the precise outcome:

```bash
diff -u logs/task1-run1-before.txt logs/task1-run1-after.txt
cat /zzz
```

Expected successful file result: **`111111******333333`**, with root ownership/mode still intact. A successful memory-write syscall or changed private mapping alone is not sufficient; a fresh file read must show the changed backing file.

**M6-S07 — screenshot result:** full before/after change, unchanged restrictive mode and elapsed time. Save `M6-S07-task1-result.png`.

Record actual outcome and run duration. The official sheet says a few seconds can suffice; there is no guaranteed duration. If it times out, review errors, actual kernel and environment, then use a new label such as `task1-run2`. If the file changed partially, stop first, record it, reset and rerun. Do not label a partial replacement as the requested complete result.

### 7.1 Reset the dummy target between attempts/rehearsals

Wait for the wrapper to return or press Ctrl+C. Confirm no attacker remains:

```bash
pgrep -a -x cow_attack
```

No output is expected. If it is still running, stop it from its terminal; for a verified lingering lab PID, use `kill -TERM <PID>`, substituting the PID shown. Then recreate the known lab file:

```bash
sudo sh -c 'printf "111111222222333333\n" > /zzz'
sudo chown root:root /zzz
sudo chmod 0644 /zzz
cat /zzz
```

This is administrator-assisted **reset**, not evidence of attack success. Never reset while the race is still running.

## 8. Task 2 preparation — ordinary account and restorable baseline

The official task modifies **charlie**, not `seed`, so that the account used for other labs remains intact. A Unix password-file record has seven fields:

```text
username:password-reference:UID:GID:comment:home:shell
charlie:x:1001:1001:,,,:/home/charlie:/bin/bash
```

`1001` is only the example. Your guest may assign a different UID/GID. The UID field grants root privilege when its numeric value is 0; the username or shell prompt does not grant it. The password stays in `/etc/shadow` and is not changed in this task.

### 8.1 Create and check charlie

```bash
getent passwd charlie
```

On a clean VM there should be no result. If the account already exists, inspect why; do not overwrite or delete an unrelated account. For this lab's new account:

```bash
sudo adduser charlie
```

Choose a **lab-only password** and remember it for `su`; no need to put it in the report. Press Enter for optional name/phone fields and confirm. Check:

```bash
grep '^charlie:' /etc/passwd
id charlie
su - charlie
id
exit
id
```

The first `su` verifies that charlie is a **normal nonzero-UID account** and that you know its password. The final `exit` returns to `seed`; do not stay in charlie's shell for the setup steps.

**M6-S08 — screenshot now:** charlie's original full record, ordinary UID, verified login and return to seed. Save `M6-S08-charlie-baseline.png`.

### 8.2 Back up AFTER creating charlie

The Task 2 baseline must include charlie with its normal UID. Save it once, after the account has been created:

```bash
sudo test ! -e /root/issd-member6-passwd.normal && sudo cp -a /etc/passwd /root/issd-member6-passwd.normal
sudo ls -l /root/issd-member6-passwd.normal
sudo cmp /etc/passwd /root/issd-member6-passwd.normal
sha256sum /etc/passwd
ls -l /etc/passwd
test -w /etc/passwd && echo 'Unexpected: writable' || echo 'seed cannot write /etc/passwd'
```

Do not overwrite an existing baseline after an attack; it may be your only good backup. Keep `/etc/shadow` out of screenshots and the repository. Do not make unrelated account changes during the task because restoring this backup replaces the entire password file.

Make a snapshot **`M6-charlie-normal-ready`**, with normal UID, compiled binaries and no attacker running. This provides repeatable starting conditions. Export evidence to Windows before restoring snapshots, since guest files roll back too.

## 9. Task 2 — race to replace the UID digits

Run as ordinary `seed`:

```bash
cd ~/issd-member6/lab-files
id
bash run_trial.sh passwd 30 task2-run1
cat logs/task2-run1-summary.txt
grep '^charlie:' /etc/passwd
diff -u logs/task2-run1-before.txt logs/task2-run1-after.txt
```

The wrapper reads charlie's current UID from `/etc/passwd` and passes it to the C program. The program matches the exact `charlie:x:<UID>:` prefix at the start of a record and replaces **only the UID digits** with the same number of zero characters.

Example:

```text
Before: charlie:x:1001:1001:,,,:/home/charlie:/bin/bash
After:  charlie:x:0000:1001:,,,:/home/charlie:/bin/bash
```

The length is unchanged. Do not replace `1001` with a single `0` in an in-place overwrite: that does not shift the remaining bytes and would leave unwanted digits. Equally, a broad search for `1001` could hit a GID or another account. Matching the account prefix and writing only the intended field avoids that ambiguity.

**M6-S09 — screenshot run and diff:** command, ordinary attacker identity, actual summary and exact record change. Save `M6-S09-task2-uid-change.png`.

### 9.1 Verify actual privilege, not just a changed file

After the wrapper has stopped the attacker, confirm:

```bash
pgrep -a -x cow_attack
grep '^charlie:' /etc/passwd
su - charlie
id
id -u
whoami
```

Enter the password set when creating charlie. `id -u` must print **0**. The username lookup may display `root`, because root and charlie now share UID 0. The GID may still be charlie's normal group ID, which does not negate UID-0 privilege. The existing `seed` process's UID does not automatically change; starting a new charlie login is the verification step.

Do not use `sudo su`, `sudo -i` or a root-run attack as proof. Those use privileges already available for administration rather than proving the account change.

**M6-S10 — screenshot success:** preceding `su - charlie`, then `id` and `id -u`. Save `M6-S10-task2-root-proof.png`. Afterwards type `exit` once and `id` to return to seed.

If UID is not exactly all zeroes, the change was partial. If the record is correct but login fails, inspect the actual error and confirm the pre-attack password test worked. Record failures; do not claim successful privilege escalation solely from a changed hash.

### 9.2 Restore normal account between experiments

Stop all lab attacker processes and exit all UID-0 charlie shells. Ensure no attacker remains before restoring:

```bash
pgrep -a -x cow_attack
id
sudo cp -a /root/issd-member6-passwd.normal /etc/passwd
sudo cmp /etc/passwd /root/issd-member6-passwd.normal && echo 'Normal-account baseline restored'
grep '^charlie:' /etc/passwd
su - charlie
id
id -u
exit
id
```

The new charlie login must now have its original nonzero UID. Restoring a database does not revoke the UID of an already running root shell; that is why you must close those shells too. If the guest is damaged and cannot authenticate, restore the clean/prepared VirtualBox snapshot.

**M6-S11 — screenshot restoration:** original record restored, fresh normal-UID login, no attacker. Save `M6-S11-account-restored.png`.

## 10. What to record and how to explain it

For each run, record **environment → starting state → command → actual output → explanation**. The logs use unique labels and refuse to overwrite an existing summary. Do not reuse `task1-run1` after restoring only the target while keeping the old logs.

| Claim | Necessary evidence |
|---|---|
| Target not ordinarily writable | Ordinary identity, root ownership/mode and denied direct write / write-permission check |
| Normal COW does not change backing file | Control's private-memory result plus fresh file read/hash |
| Dummy-file exploit worked | Full exact replacement in fresh file reads, permissions still restricted |
| UID overwrite worked | Full diff showing only intended charlie UID digits changed |
| Root privilege obtained | Fresh non-sudo `su - charlie` followed by `id -u` = 0 |
| Patched comparison resisted this run | Actual kernel/package information, same dummy experiment, unchanged content, no setup error |

Each attack run's elapsed time is the wrapper's wall-clock measure with polling granularity. It is not a claim that the kernel was attempted exactly N times. Report unsuccessful runs and partial changes honestly.

The official submission guidance requires explanations for important code and surprising observations. Attaching code and screenshots without interpreting them is insufficient.

## 11. Countermeasures required by your division

| Countermeasure | Explanation | Limitation / practical detail |
|---|---|---|
| **Kernel patching** | Install a distribution-supported kernel that fixes CVE-2016-5195 | Installing a package alone does not mean that kernel is running; reboot as needed and verify `uname -r` plus package/advisory status |
| **System updates** | Keep kernel and supported OS packages current; migrate obsolete production systems | Preserve the intentionally vulnerable lab snapshot only for the isolated exercise; production should not remain on this historical image |
| **Limit local access** | Restrict unnecessary shell accounts and execution of untrusted local code; reduce exposure | This bug is local but code execution can follow another compromise; account restriction does not fix COW |
| **Monitor privilege escalation** | Watch unexpected UID-0 accounts, account-file changes and suspicious privileged sessions; maintain trusted integrity baselines | Logs may be incomplete; ordinary file-write auditing may miss writes through a memory-management exploit |
| **Least privilege / hardening** | Reduce the blast radius of local services and remove unnecessary access | Unlike Member 5, merely removing an application Set-UID bit cannot repair a kernel COW bug |

Useful **read-only checks** in the lab:

```bash
awk -F: '$3 == 0 {print $1 ":" $3 ":" $7}' /etc/passwd
sha256sum /etc/passwd
stat /etc/passwd
sudo tail -n 30 /var/log/auth.log
```

The awk numeric comparison also detects a zero-padded UID such as `0000`. The auth log may record `su`/session activity; it is not guaranteed to identify the Dirty COW memory race itself. A trusted before/after integrity comparison is stronger than relying only on file timestamps. Do not claim monitoring is a preventive fix.

### Optional patched-VM comparison

This is an additional control, not a numbered SEED requirement. Use a separate patched Linux VM, such as Member 5's Ubuntu 20.04 VM after its lab cleanup. Compile the Member 6 programs afresh inside that VM, create **only `/zzz`**, and repeat Sections 6–7. No need to create charlie or run the password-file attack there.

```bash
uname -r
dpkg-query -W "linux-image-$(uname -r)"
bash build.sh
bash run_trial.sh dummy 30 patched-dummy-run1
cat /zzz
```

Expected: no backing-file modification. Distinguish a properly running race with no target change from a compile error, missing file or denied `/proc/self/mem` access. A bounded unsuccessful attempt alone does not establish universal immunity; pair it with the vendor's fixed-kernel information and COW explanation. Do not downgrade the kernel to make this comparison “work”.

**M6-S12 — optional screenshot:** patched environment, successful build/run and unchanged dummy file. If not performed, label the report section **not performed; discussion only**. Save `M6-S12-patched-comparison.png` if collected.

## 12. Troubleshooting

| Symptom | Likely cause / action |
|---|---|
| Ubuntu 20.04/16.04 shows no modification | Those SEED images are patched. Use the intended SEED Ubuntu 12.04 vulnerable image for the exploit, not symlink sysctl changes. |
| Ubuntu 12.04 but no effect | Check actual booted kernel and package family; the image may have been updated. A release name alone is insufficient. |
| VirtualBox cannot boot | Check extracted disk attachment, 32-bit guest setting, hardware virtualisation and exact error. |
| `No bootable medium` | An empty disk was attached instead of the prebuilt image, or the extracted disk is missing. |
| Old desktop/shared clipboard fails | Try basic display without 3D. Transfer through a ZIP/USB or paste source; the exploit needs neither fancy graphics nor clipboard integration. |
| HTTPS certificate/TLS error in old guest | Download official files using the Windows host, then transfer. Check guest clock; do not globally bypass certificate verification. |
| apt repository 404 | Ubuntu 12.04 repositories have moved to archives; inspect precise archive configuration as in Section 4. Preserve intended kernel. |
| `pthread_create` undefined at link time | Build with `-pthread`, as in `build.sh`. |
| `memmem` or `pwrite` undeclared | Use the supplied feature macros and Linux GCC; not the host Windows compiler. |
| `$'\r'` or syntax errors in scripts | Run `sed -i 's/\r$//' *.sh *.c` in guest `lab-files`, then `bash build.sh`. |
| `Pattern absent` | Dummy target already modified, charlie UID differs, account has UID 0 already, or baseline not reset. Inspect and restore first. |
| `Target must be ... not writable` | File owner/permissions wrong, target not created, or user has unintended write rights. Restore proper setup; do not weaken target mode. |
| `/proc/self/mem` open/write error | Capture exact errno. Check guest kernel/runtime restrictions and execute directly in the VM. Do not call it a successful defence test solely because setup failed. |
| Changed hash but wrong content | Partial/incorrect modification. Stop, save exact diff, restore baseline and retry with a new label. |
| Full UID change but `su` fails | Confirm password, complete seven-field record, and Task 2 pre-login test. Save error; restore if needed. |
| `whoami` shows root instead of charlie | Expected possible UID-0 name resolution; verify numeric UID. |
| Account looks restored but old shell still root | Credentials of already running processes persist; exit all test root shells and verify a new login. |
| File/session corruption | Stop the process and restore the saved baseline if possible; otherwise restore the VM snapshot. |
| Wrapper reports label already exists | Pick `task1-run2`, `task2-run2`, etc.; keep earlier evidence. |

## 13. Evidence, report and cleanup

Use **Windows Win+Shift+S** to capture the visible guest and save PNGs into this project's `Member6/evidence/`. Saving on the host keeps evidence available even after snapshot rollback. Alternatively copy guest screenshots/logs out before any rollback.

At each M6-S checkpoint:

1. Enlarge terminal text and include the command, output and environment context.
2. Use the suggested filename; a/b/c suffixes are fine for readable multiple captures.
3. Insert into `REPORT_TEMPLATE.docx` with a caption stating action, actual observation and meaning.
4. Record actual runtime and errors. Do not turn predicted outputs into claimed measurements.

Copy out source files, logs and completed notes. A read-only transfer share cannot receive exports; use a separate writable export share or another file-transfer method. Do not upload password/shadow backups or the VM disk to GitHub.

### End-of-session cleanup

1. Stop the attack and confirm no `cow_attack` process remains.
2. Exit all charlie/UID-0 shells and return to seed.
3. Restore the normal-account baseline using Section 9.2 and verify it.
4. Remove `/zzz` only if it is the dummy file you created for this lab.
5. Keep the normal lab account for another rehearsal, or remove the account **after its UID is restored**. Never issue account-removal commands while charlie maps to UID 0.

```bash
pgrep -a -x cow_attack
id
grep '^charlie:' /etc/passwd
sudo cmp /etc/passwd /root/issd-member6-passwd.normal && echo 'Normal UID baseline verified'
sudo rm -f /zzz
awk -F: '$3 == 0 {print $1 ":" $3}' /etc/passwd
```

If finished permanently and charlie was created only for this lab, you may run `sudo deluser --remove-home charlie` **after confirming its original nonzero UID**. That command removes an account and its home; export its evidence first. Do not later restore the post-adduser backup without also recreating the account state. The clean pre-lab snapshot is the simplest full rollback of passwd/shadow/group/home changes.

**M6-S13 — screenshot cleanup:** stopped process, restored ordinary UID or removed lab account, dummy file removed and expected UID-0 list. Save `M6-S13-cleanup.png`.

No sysctl controls or Set-UID permissions were required by this lab, so there are none of those to restore. If you made separate personal changes, document and revert them too.

## 14. Short presentation plan

Use `PRESENTATION_PLAN.md` / `.docx`. Suggested 5–7 minutes, subject to your group's actual allowance:

1. Explain COW and the kernel race before the demo.
2. Show the correct old VM, nonzero user and read-only target.
3. Demonstrate normal COW, then the bounded dummy-file race.
4. Show your recorded Task 2 UID change and real non-sudo root-login evidence.
5. Explain kernel patching, updates, restricted local access and monitoring.

The dummy-file experiment is the shortest, clearest live sequence. Complete Task 2 beforehand; use saved real-run screenshots or a short recording if timing or restoration would exceed your presentation slot. Identify recorded evidence as recorded. Have a clean snapshot and unique run labels ready for rehearsal.

## 15. Completion checklist

* [ ] Correct separate 32-bit SEED Ubuntu 12.04 guest, actual kernel recorded.
* [ ] Original lab task PDF/source obtained and read.
* [ ] Programs built as normal user; no root-run attack or Set-UID installation.
* [ ] Dummy file root-owned with direct ordinary write denied.
* [ ] Normal-COW control explained and documented.
* [ ] Task 1 exact dummy replacement demonstrated and interpreted.
* [ ] Task 2 charlie normal account created and baseline backed up after creation.
* [ ] Actual UID discovered; only same-length UID digits changed.
* [ ] Fresh `su - charlie` proves numeric UID 0 without sudo.
* [ ] Run logs, failures/retries and before/after diffs saved.
* [ ] Kernel mechanism and application-race distinction explained.
* [ ] All four division countermeasure themes discussed.
* [ ] Optional patched comparison labelled performed/not performed accurately.
* [ ] Screenshots placed in report with readable factual captions.
* [ ] Report placeholders replaced with actual evidence or explicit unresolved status.
* [ ] Source citations and assistance acknowledgement included.
* [ ] Demo rehearsed; real saved evidence ready; guest cleaned up.
* [ ] Submission deadline/format confirmed with lecturer/group.

## 16. Research references

Full links and attribution are in `README.md`. The primary references are the lecturer-linked [SEED task sheet](https://seedsecuritylabs.org/Labs_20.04/Files/Dirty_COW/Dirty_COW.pdf), [SEED Ubuntu 12.04 manual](https://seedsecuritylabs.org/Labs_12.04/Ubuntu12_04_VM_Manual.pdf), and [Ubuntu CVE advisory](https://ubuntu.com/security/CVE-2016-5195). The original task source and complete example program were checked as well as the lab landing page, which is essential here because the URL's `20.04` directory is misleading about the required VM.
