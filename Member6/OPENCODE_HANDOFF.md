# OpenCode / Opus 5.5 fresh-run handoff

Prepared **8 October 2026** after the user stopped the previous orchestration and requested a fresh, cleaner screenshot set.

**Superseded by the completed fresh run on 9 October 2026.** Both tasks, fresh non-sudo UID-0 proof, exact restoration, cleanup and verified export are complete. The VM is powered off normally. Use [the current checkpoint record](evidence/incoming/opus-fresh-20261008/README.md) and [submission package](submission/README.md). This historical handoff preserves the original model-selection and installation context; the actual fresh-run assistance was GPT-6 Astra through OpenCode.

## Installation answer

The required guest reported **i686, 32-bit Ubuntu 12.04.2**. The official current OpenCode V2 installer accepts **linux-x64** and **linux-arm64**; it has no supported Linux i686 target. Connecting the internet or installing curl does not remove this architecture restriction. The npm package also selects a native platform binary.

Use the existing OpenCode installation on **Arch** to run the model and control the required guest. Keep the original guest kernel/architecture for the assignment. There is no supported native V2 installation command for this SEED VM.

Sources checked: [V2 installation/platform list](https://opencode.ai/v2/docs/), [V2 installer](https://opencode.ai/v2/install), [V2 CLI](https://opencode.ai/v2/docs/cli), [provider/model selection](https://opencode.ai/v2/docs/cli/providers), [V2 keybindings](https://opencode.ai/v2/docs/cli/keybinds).

## MANUAL ACTION REQUIRED — HOST / OpenCode

1. Open an **Arch terminal**, not the Ubuntu VM terminal.
2. **HOST ACTION — start the already-installed client:**

   ```bash
   opencode /home/DHB/Downloads/ISSP/ISSD-seed-labs
   ```

3. Create a fresh session: with default V2 bindings, press **Ctrl+X**, release, then **N**. Alternatively use **Ctrl+P → Create a new session** (search for “new session”). Custom keybindings can differ.
4. Enter `/models`; choose **GitHub Copilot → Claude Opus 5.5**. The provider/model ID was confirmed as `github-copilot/claude-opus-5.5`. Verify the model selection in the UI before submitting.
5. Paste:

   ```text
   Read Member6/OPUS_5_5_FRESH_RUN_PROMPT.md completely and follow it. Start the fresh Member 6 run, save new genuine screenshots in the specified fresh shared directory, and continue through verified experiments, cleanup, report and presentation. Your tools start on Arch; execute every lab operation inside the named SEED VM.
   ```

6. Expected: the new Opus session reads the repository and verifies VM access. Respond to its explicit manual-action requests with outputs/screenshots, not passwords. It should stop on an actual environment or control-channel problem rather than run guest commands on the host.

## Fresh shared destination

* **Host:** `/home/DHB/Downloads/ISSP/ISSD-seed-labs/Member6/evidence/incoming/opus-fresh-20261008/`
* **Guest, while M6export is mounted:** `/home/seed/m6-export/opus-fresh-20261008/`
* **Input share:** `M6pack` at `/home/seed/m6-transfer`, read-only.
* **Execution directory:** `/home/seed/issd-member6/lab-files`, native ext4.

The fresh destination was created empty for new captures. Earlier images/logs are previous-session records and are not fresh evidence. Save outputs to the share; execute the lab on native guest storage.

## Previous work — avoid repeating completed installation

On 7 October the previous agent:

* Audited all 616 original tracked repository files and read the full Member 6 specification, source, shared allocation and relevant Member 5 work.
* Verified the official `SEEDUbuntu12.04.zip`, extracted its split VMDK, configured `ISSD-Member6-SEED12` and took `M6-clean-SEED12`.
* Resolved the Arch driver mismatch by the user's reboot into the already-installed `7.2.9-arch1-1` kernel. VirtualBox 7.2.20 then started the guest successfully.
* Observed Ubuntu **12.04.2**, **i686**, kernel **3.5.0-37-generic**, package **3.5.0-37.58~precise1**, source **linux-lts-quantal**, GCC **4.6.3**, seed UID/GID **1000** and native **ext4**.
* Copied the four supplied files with matching SHA-256 values and built seed-owned **0755 ELF32** binaries. Python 2.7.3 parsed the verifier; the timeout check returned 124.
* Collected earlier S02/S03 screenshots and logs. One S02 image is a failed input attempt; it is not successful environment proof.

**The previous agent did not create `/zzz` or charlie, run the normal-COW control, run either Dirty COW task, verify a root login or perform post-experiment cleanup.** The user may have changed/reset the VM since then: inspect the actual current state. No earlier screenshot may be relabelled as a fresh run.

Useful previous records are `evidence/incoming/M6-S02-environment.log`, `M6-preflight-extra.log`, `M6-transfer-native.log` and `M6-S03-build.log`, plus the host preparation records. The source hash manifest is `lab-files/SOURCE_SHA256SUMS`.

## Control-channel lessons

* VirtualBox's guest framebuffer capture worked. S01 still needs the actual host settings UI.
* The guest's old VBoxControl 4.2.16 could not access guest properties as ordinary seed. Do not treat that error as a Dirty COW result.
* Shared-folder mounts worked with the documented read-only input and writable export scopes.
* Fast keyboard input initially lost a prefix, and a later stray `-` caused `-test` to fail. `tools/guest-console.py` uses paced chunks and Ctrl+U at a verified normal prompt. Confirm focus/prompt and inspect actual output; successful input delivery is not successful execution.
* `tools/capture-vm.py` defaults to the older top-level evidence directory. For the fresh run, use the direct VBoxManage screenshot command with the fresh absolute output path, or explicitly adapt the helper's output-directory option while preserving originals.
* The user wants plain, readable terminal output. Keep `set -x`, JSON verification dumps and explanatory scaffolding out of screenshots, while retaining real detailed logs separately.

## If curl itself is still missing

The earlier `Could not resolve` message was a network/DNS failure. Later, NAT was connected and the guest reported **10.0.2.15**. The user has now confirmed internet access. Do not repeat network setup merely because the old error remains in a pasted transcript.

If apt now returns **404 / unavailable Precise packages**, its old Ubuntu mirror configuration is a separate problem. These steps install curl only; they do not make OpenCode support i686.

### MANUAL ACTION REQUIRED — VM, only if curl is still needed

1. In the **Ubuntu VM** terminal, verify DNS and inspect the active sources:

   ```bash
   getent hosts old-releases.ubuntu.com
   grep -E '^deb ' /etc/apt/sources.list
   ```

2. If DNS works and the standard Ubuntu **precise** entries still use the retired archive/security mirrors, back up without overwriting an earlier backup, then edit:

   ```bash
   sudo cp -an /etc/apt/sources.list /etc/apt/sources.list.m6-before-curl
   sudo nano /etc/apt/sources.list
   ```

   Change the relevant official Precise entries to:

   ```text
   deb http://old-releases.ubuntu.com/ubuntu/ precise main restricted universe multiverse
   deb http://old-releases.ubuntu.com/ubuntu/ precise-updates main restricted universe multiverse
   deb http://old-releases.ubuntu.com/ubuntu/ precise-security main restricted universe multiverse
   ```

   Preserve unrelated configuration. In nano, save with **Ctrl+O**, **Enter**, and exit with **Ctrl+X**.

3. Refresh metadata and install only the requested utility:

   ```bash
   sudo apt-get update
   sudo apt-get install --no-install-recommends curl
   curl --version
   ```

4. Expected: curl is available if the package transactions succeed. This is not a full system/kernel upgrade. If DNS, signatures or package installation still fail, send the exact error; preserve signature validation.
5. Continue the lab with OpenCode on Arch. Its official native installer still cannot run a Linux x64/ARM64 binary on this i686 guest.
