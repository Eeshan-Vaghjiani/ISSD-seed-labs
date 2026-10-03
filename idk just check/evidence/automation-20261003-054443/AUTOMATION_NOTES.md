# Member 5 visible-desktop automation — 3 October 2026

Session ID: `20261003-054443`. All timestamps are the guest's clock (`-04:00`).

## Documents and starting state

The repository's `Member5/START_TO_FINISH_GUIDE.md`, `Member5/evidence/SCREENSHOT_CHECKLIST.md`, `Member5/VERIFICATION.md`, and both repository/working copies of all five original C/shell sources were read. `Member5/evidence/EVIDENCE_REVIEW.md` was absent in this checkout and in the working tree; the user explicitly chose to proceed with the available documents. The working C/shell files initially matched the repository byte for byte.

The controller and both evidence shells run as `seed`, UID/EUID 1000. The initial process inventory found **no running monitor, attacker, victim, or su session**. The old monitor was therefore already gone; this session did not claim to have interrupted it.

`/tmp` was root-owned, mode 1777. The existing `/tmp/XYZ` was a **regular file owned by root, group seed, mode 0664**, size 3,381,664 bytes, inode 4593750. This confirms the ownership/sticky-directory condition that prevents seed from unlinking it. The file's writable group does not grant permission to delete its directory entry in sticky `/tmp`.

Before the first reset, `pre-reset-task2b/` received verbatim copies of both original trial logs, the file contents, and original pathname metadata. The original log filenames were retained in `lab-files/logs/` too. Contents copied as seed have seed ownership; `original-metadata.txt` records the actual original ownership.

* Original log: `task2b-20261003-052529-summary.txt`.
* Last progress line: **76,000 attempts / 227 seconds**.
* The log has no completion/interruption line. Its **final attempt total and final elapsed time are unknown**.
* Original last-output log: empty, preserved as such.
* Original XYZ content SHA-256: `ebf805e5910024c5ca35498b116fabdba704d2020a3fa06301909f19662eacc5`.
* The original `File exists` message was user-reported; the old terminal was no longer open. A clearly labelled, bounded diagnostic retry produced a real `Operation not permitted` error before reset. The new retry 1 subsequently produced a real `File exists` error as well. These are recorded as separate observations, not a reconstruction of the lost terminal.

## Desktop and capture method

Initial environment: `DISPLAY=:0`, `XDG_SESSION_TYPE=x11`, `XAUTHORITY=/run/user/1000/gdm/Xauthority`. `gnome-terminal` and `gnome-screenshot` were available; `wmctrl` and `xdotool` were absent. Installed Python GI/Wnck, GTK/GDK, X11 and XTest libraries supplied window placement, focus and paste/keyboard control. No additional package installation was required.

`automation/desktop.py` created two actual GNOME terminal windows titled **A — Attacker** and **B — Victim and results**. A separate terminal profile uses a readable 12-point monospace font, high-contrast colors, and unlimited scrollback. The controller requested 1920×1200; VirtualBox's desktop resizing settled at **1920×967**, which is the actual captured image size. Original desktop/profile/window settings are retained in `automation/desktop-state.json`.

The main captures use `gnome-screenshot` on the **actual whole desktop**. Two supplemental S08 burst frames use GDK to read the actual root-window pixels directly, also without image alteration. The control/OpenCode window and file manager are minimized before capture, and the evidence terminals are placed side by side. PNGs are kept unedited with unique timestamped names in the parent evidence directory. No output is manufactured, composited, redrawn, cropped, or substituted. The image-read tool was used to inspect actual captures for legibility, titles, framing, and visible commands/results. Additional captures supplement poor framing or transient root-shell titles; originals are retained.

The GNOME root login initially changed B's client-side title. Its interactive prompt/title was adjusted while displaying real `id` output; this was a display setting, not a change of user identity. One early title-adjustment command used a literal `$` in a UID-0 prompt; the actual UID is established by `id`, not prompt punctuation. The later atomic-login capture uses Bash's UID-dependent prompt escape correctly.

`terminal-A.typescript` and `terminal-B.typescript` are full output-only `script -qef` recordings; `.timing` files retain replay timing. Commands and program errors are included. Scrollback was not cleared. Hidden password input is not recorded. `automation/desktop-actions.jsonl` lists automated commands, window operations, captures, dimensions and screenshot SHA-256 digests.

## Automated experiment operations

* Read-only initial user, process, filesystem, desktop, source-comparison and binary-symbol checks.
* Creation/placement of evidence terminals and output transcripts.
* Preservation and hashing of the existing failure logs and root-owned file before reset.
* A bounded pre-reset diagnostic attacker retry as seed, visibly labelled as a new diagnostic.
* Visible execution of the guide's administrative reset/setup commands. `sudo` is used for password-file restoration/comparison, removing lab paths, sysctl setup/readback and final removal of Set-UID. These sysctl nodes are mode 0600 in this VM, so configuration readback also requires sudo.
* Launching both attackers and all victim-monitor trials **as seed, without sudo**. The victims' EUID change is their installed Set-UID behavior. The root-owned `vulp` binary has `access` and `fopen` symbols and no imported `sleep`; all Tasks 2.B/2.C runs use that binary. The C sources and binaries were not modified or rebuilt in this session.
* Waiting for actual attacker initialization messages, confirming live PID/start-time identity and seed-owned symlink initialization, checking the clean password-file hash, then starting the monitor.
* Unique trial labels, 300-second monitor limits, 330-second attacker limits, and a bounded outer watchdog. If an attacker exits, the monitor is asked to finish its in-flight invocation and stop; the failure and remaining file state are preserved. When a monitor ends, its attacker is stopped and checked before results are presented.
* Inspecting the exact full account record after hash changes, including one exact matching record, seven fields, UID/GID 0, home `/root` and shell `/bin/bash`. The tested input is 43 characters. A changed hash alone is never designated root access.
* Entering the **non-sudo `su - test` command**, checking the resulting shell with actual `id`/`whoami`, capturing evidence, exiting the root login, and running `id` as seed before the next reset/trial.
* Capturing and visually reviewing the real checkpoint screenshots; retaining originals and logs.
* Running the Task 3.A protected-target/allowed-file controls and the Task 3.B stable `/dev/null`-link control as seed, with the attackers stopped. Their commands, actual errors, exit statuses and baseline-hash checks are saved in distinct `*-controls.txt` files.
* Final process/login-shell checks, password-file restoration and comparison, removal of both lab paths and Set-UID bits, and readback of the user-selected 1/2 policy. These completed successfully; the full output is in `logs/cleanup-20261003-054443.txt`.
* Copying nine pre-existing repository PNGs unchanged into `prior-user-captures/`, retaining their source paths and hashes in a copy manifest. These are prior user captures, not newly automated captures.
* Generating the final report/table from the actual saved JSON/terminal/control records, comparing both successful post-attack account files to the clean baseline plus the exact record, collecting sources/logs, and preparing a checksummed evidence archive.

## Human interaction

The user confirmed proceeding without the missing review document. The user was asked to enter the Task 2.B login password directly in B and confirmed that its shell was open. Both login sessions reached real shells through non-sudo `su`; **no password or empty-password keystroke was supplied by automation**. Task 2.C had already reached its login shell before another password question was needed. Only real terminal input was used for authentication; no password was placed in scripts or chat.

`sudo -v` completed without asking for a password in this session. Any sudo command that needs a password remains an ordinary interactive terminal command.

For cleanup the user explicitly selected **symlinks=1, regular=2**, matching the installed `protect-links.conf` policy. This is an explicit post-lab choice, **not a claim to have established the VM's original runtime settings**. `sysctl-before.txt` remains the original saved 0/0 file.

## Monitor instrumentation and measurement limits

The original `run_trials.sh` is saved in `source-before/`. The working helper was minimally changed to refuse labels whose logs already exist and to retain actual attempt/elapsed counts when interrupted. Its signal handler lets an in-flight invocation finish; invocations are counted before launch. The check/use race in the victim is unchanged.

`lab_runner.py` only coordinates processes and records their real output. Each `*-result.json` contains a monotonic runner wall time as well as the monitor's integer `SECONDS` measurement. A monitor value of 0 seconds means sub-second timer resolution, not zero execution time. The runner wall time includes monitor process startup and exit handling; it is not a measurement of the vulnerable instruction window. Racing and screenshot/monitor overhead can influence scheduling; the counts describe these runs only.

Result JSON `login_verified: false` is the state **at monitor completion**, before a login is attempted. The separate verified-login report and actual terminal transcript/screenshots supply the later login evidence. A successful hash signal is not retroactively substituted for a login test.

## Evidence limits

Task 1 and delayed Task 2.A were already completed by the user and were not rerun. Their existing captures were retained. The new no-delay naive runs ended rapidly: the S08 capture taken immediately after starting retry 1 shows its **completed failure**, not two still-running processes. S09 supplies the genuine successful retry's full command/result/login chain. This capture timing is documented rather than calling a stopped process a live attack. The long defence trials have genuine running-state captures.

After completing the two defence trials, one additional uniquely labelled no-delay run (`task2b-capture-20261003-054443`) attempted faster S08 capture with both controls reset to 0/0. It again produced a genuine File-exists/root-owned-regular-file failure: **2 attempts, monitor 0 seconds, runner wall 0.378590 seconds**, no target change. Its 88-byte root-owned XYZ file was saved before final reset. The two unedited GDK frames show startup and failure; PID/start-time checks before/after each returned **zero frames verified with both experiment processes live throughout the capture**. The capture filenames express their intended checkpoint, not a claim of live-state verification. Both frames and the result image were retained and visually inspected. If a strictly simultaneous-live S08 image is required, the remaining evidence action is a higher-frame-rate desktop recording started before a future properly reset bounded trial, preserving that original recording and selecting an actual live frame. No further race run is left running in this session.

The original `run_trials.sh` is preserved. A later runner-only addition records its monitor PID/start time for the supplemental capture checks; that does not change either C program or insert a victim delay. The main defence/success runs predate that capture-only addition.

Finite defence runs support statements of the form **“no success observed in N attempts over T seconds.”** The privilege-drop and kernel pathname-following rules explain why the protected write is blocked; finite trial counts alone are not a universal proof.
