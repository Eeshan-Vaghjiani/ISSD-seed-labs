# Member 6 — exact capture plan and proof requirements

Companion to the authoritative [SCREENSHOT_CHECKLIST.md](SCREENSHOT_CHECKLIST.md). **No M6 screenshot has been collected yet.** Host inventory and VM configuration logs are in `host/`; they are not guest experiment screenshots.

## Capture method

**MANUAL ACTION REQUIRED — VM:** put the real command and its actual output on screen; enlarge text using the terminal's **View → Zoom In** (usually Ctrl+Shift+Plus). Keep enough prompt/window context to identify the VM. If the screen is too dense, use complementary images rather than hiding a relevant failure.

**MANUAL ACTION REQUIRED — VIRTUALBOX (HOST), S01:** open the actual settings views described in [ARCH_HOST_SETUP.md](../ARCH_HOST_SETUP.md#3-actual-vm-configuration-and-why), then use Spectacle to save the window/region as PNG.

For **S02–S13**, the agent can save the real guest framebuffer when the required output is visible. Exact **HOST ACTION** example:

```bash
python Member6/tools/capture-vm.py M6-S02-environment.png
```

This uses `VBoxManage controlvm ISSD-Member6-SEED12 screenshotpng ...`; it does not render text into an image. It saves a separate `.capture.json` with command, VM metadata, host timestamps and SHA-256. Each capture must still be visually reviewed. A framebuffer image does not include the host VirtualBox settings window, so it cannot substitute for S01.

If the agent cannot capture, **MANUAL ACTION REQUIRED — HOST:** use Spectacle on the visible VM window, save the exact filename under `Member6/evidence/`, and send the image. No annotations, output replacement, compositing or success reconstruction. Keep originals. Suggested suffix convention: `M6-S03-a-code-build.png`, `M6-S03-b-code-build.png`.

## Every checkpoint

Commands below are **VM commands** except S01. Execute the full corresponding [VM session step](../VM_SESSION_GUIDE.md), including prerequisites and password/stop gates.

| ID / filename | Required real commands or visible state | Why it proves the checkpoint | Capture / send-back |
|---|---|---|---|
| **S01** `M6-S01-vm-setup.png` | HOST VirtualBox: name `ISSD-Member6-SEED12`; Ubuntu 12.04 32-bit; RAM 2048 MB; 2 CPUs; existing SEED disk or its verified snapshot-parent chain. Supplement Storage and Snapshots views. | Establishes the separate configured VM and disk/resources. Does not establish the running guest kernel. | **Manual host capture required**; a/b/c views if needed. Send settings images. |
| **S02** `M6-S02-environment.png` | `whoami`; `id`; `lsb_release -a`; `uname -r`; `uname -m`; `gcc --version`; `command -v ...`; `dpkg-query -W "linux-image-$(uname -r)"`. Use the complete Step 1 command list. | Proves actual ordinary identity, release, architecture, running kernel/package and compiler availability. | Agent framebuffer capture after user login/commands, or manual PNG. Send all output too. |
| **S03** `M6-S03-code-build.png` | `sha256sum -c SOURCE_SHA256SUMS`; `bash build.sh`; `ls -l cow_attack cow_control`; code lines 31–61 and 100–152 from `cow_attack.c`. | Establishes original source, real build, ordinary executable modes, `MAP_PRIVATE` read-only mapping and both workers. | a/b/c recommended for readable code and build. Guest build remains mandatory. |
| **S04** `M6-S04-dummy-baseline.png` | `id`; `cat /zzz`; `ls -l /zzz`; `echo 99999 > /zzz`; fresh `cat /zzz`; `sha256sum /zzz`. Include the actual denied redirection. | Shows normal seed cannot write root:root 0644 and the starting file remains exact. | Capture before control/race. Send actual baseline hash. |
| **S05** `M6-S05-normal-cow.png` | `./cow_control`; `cat /zzz`; `sha256sum -c ../provenance/dummy-normal.sha256`. | Distinguishes changed private memory from an unchanged freshly read backing file/hash. | Capture control labels and fresh file verification together. |
| **S06** `M6-S06-task1-running.png` | `id`; invocation of `trial-with-evidence.sh dummy 30 task1-run1`, its visible `bash run_trial.sh ...`, mapping details, real summary/program output. | Establishes the actual ordinary-user trial and its measured outcome. Repository permits during **or immediately after** the trial. | Capture actual state; if afterward, caption as completed run. Optional `pgrep -x cow_attack` plus `ps` for live PIDs only if actually observed. |
| **S07** `M6-S07-task1-result.png` | `diff -u logs/task1-run1-before.txt logs/task1-run1-after.txt`; `cat /zzz`; `ls -l /zzz`; actual elapsed summary; `verify-trial.py ... --live`. | Exact full backing-file replacement, current restrictive ownership/mode, matching saved/live hash. Partial change is not complete success. | Capture after exact success; preserve failed/partial runs separately with unique labels and captions. |
| **S08** `M6-S08-charlie-baseline.png` | Original `grep '^charlie:' /etc/passwd`; `id charlie`; actual `su - charlie` → `id`/`id -u` → `exit` → seed `id`; root backup listing and `sudo cmp` after creation. | Proves actual original nonzero UID, usable password/login, return to seed, and a correct post-adduser restorable baseline. | **Manual password entry required.** Usually a/b for login and backup. Send original record/UID; never send password or shadow data. |
| **S09** `M6-S09-task2-uid-change.png` | Ordinary `id`; actual supplied account trial; labelled runtime summary; full before/after diff; exact-file verification. | Shows only the intended same-width charlie UID digits changed; no substitution of a manually edited file. | Capture summary and full relevant diff, a/b if needed. |
| **S10** `M6-S10-task2-root-proof.png` | Preceding **non-sudo `su - charlie`** plus actual `id`, `id -u`, `whoami`. Include proof shell PID if collected. | Numeric UID 0 from a new authenticated session verifies privilege; changed text/hash alone does not. | **Manual password entry and shell exit required.** Agent/manual capture while the genuine proof remains visible. |
| **S11** `M6-S11-account-restored.png` | Stopped attacker; seed `id`; actual backup restoration/comparison; original charlie record; fresh non-sudo charlie `id -u` nonzero; exit back to seed. | Establishes exact normal file restoration and credentials assigned to a new login. Prior privileged shells must also end. | **Manual password and exit required.** Send complete restored identity sequence. |
| **S12** `M6-S12-patched-comparison.png` | Optional separate patched VM's actual release/kernel/package, valid build/baseline/trial, no setup error and unchanged dummy file/hash. | Supports only the observed finite negative trial, interpreted with vendor patch evidence. | **Not performed; discussion only** currently. Omit the image if unperformed. |
| **S13** `M6-S13-cleanup.png` | `check-cleanup.sh`: no attacker/su/privileged shell; exact normal passwd hash/record; original UID-0 list; `/zzz` absent; normal binaries; native workspace and file inventory. | Verifies the recorded post-experiment state and reproducibility prerequisites. This cannot be replaced by the pre-lab snapshot. | Capture after actual cleanup; a/b for inventory. User supplies any sudo prompt input. |

## Provenance and review

For each selected image retain: original filename, SHA-256, capture method, related run label/log paths, actual visible observation, and a caption explaining the conclusion. For example:

> **Figure — S07, Task 1.** The ordinary-user trial `[actual label]` produced `[actual complete/partial/unchanged result]` after `[actual integer seconds]`. The fresh file read and metadata show `[observed properties]`. Therefore `[warranted conclusion]`.

Replace these slots only after viewing the image and matching its logs. Keep **EXPECTED**, **ACTUAL**, **EXPLANATION** separate in [the results record](../submission/RESULTS.md). A screenshot filename's presence is not a completed checkpoint. The final checkpoint table is [EXECUTION_STATUS.md](../EXECUTION_STATUS.md).
