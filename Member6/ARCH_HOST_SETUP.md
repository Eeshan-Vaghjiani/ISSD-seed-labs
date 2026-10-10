# Member 6 — Arch Linux and the configured VirtualBox VM

**Completed fresh run — 9 October 2026:** both tasks, non-sudo UID-0 proof, exact restoration and cleanup are verified. The VM is powered off normally; its cable is disconnected and both snapshots are retained. Use [submission/LIVE_PREPARATION.md](submission/LIVE_PREPARATION.md) for the next rehearsal. The reboot/installation instructions below are historical setup and need not be repeated for this prepared VM.

**Update — 8 October 2026:** the required Arch reboot was completed, VirtualBox started the guest, and actual guest environment/build checks passed. For the requested new Opus session use [OPENCODE_HANDOFF.md](OPENCODE_HANDOFF.md). The sections below retain the earlier setup/diagnosis and reproducible host instructions; their pre-reboot table is historical. The original start-to-finish guide remains the experiment specification.

## 1. What is actually installed

| Item | Observed on 7 October 2026 |
|---|---|
| Host | Arch Linux, x86-64; AMD Ryzen 5 5625U, AMD-V, 12 logical CPUs |
| RAM | About 15 GiB total; about 4.7 GiB available at initial inspection |
| Running kernel | `7.2.8-arch1-2` |
| Installed kernel / headers | `linux 7.2.9.arch1-1`, matching `linux-headers` |
| VirtualBox | `virtualbox 7.2.20-1`, CLI `7.2.20r175154` |
| Driver package | `virtualbox-host-dkms 7.2.20-1`; `dkms 3.4.4-1` |
| DKMS result | `vboxhost/7.2.20_OSE, 7.2.9-arch1-1, x86_64: installed` |
| Current driver | Not loaded; current-kernel `modinfo vboxdrv` fails; no `/dev/vboxdrv` |

**No package installation is required based on these observations.** The installed driver has the installed kernel's vermagic, not the currently running kernel's. The generic VirtualBox suggestion to run `/sbin/vboxconfig` is not the remedy indicated by this Arch DKMS inventory.

### MANUAL ACTION REQUIRED — HOST: reboot

1. **Where:** Arch desktop/terminal, outside the VM.
2. Save all open work. This will end the current desktop/tool session.
3. **HOST ACTION — exact command, run yourself when ready:**

   ```bash
   systemctl reboot
   ```

4. Log back in and open a host terminal in the repository. Run these read-only checks:

   ```bash
   cd /home/DHB/Downloads/ISSP/ISSD-seed-labs
   uname -r
   dkms status
   modinfo -F vermagic vboxdrv
   ls -l /dev/vboxdrv
   VBoxManage list vms
   ```

5. **Expected:** the running kernel should be `7.2.9-arch1-1`; driver vermagic should match; the VM list should contain `ISSD-Member6-SEED12`. Module/device presence must be checked, not assumed.
6. **Send back:** all five command outputs after `cd`, and any error. Then the agent can verify boot readiness and continue the actual guest session.

If the kernel is correct and `modinfo` works but `/dev/vboxdrv` is absent, loading the already-installed driver is the next conditional operation:

**HOST ACTION — only in that verified state:**

```bash
sudo modprobe vboxdrv
ls -l /dev/vboxdrv
```

Enter the **Arch** sudo password directly in your host terminal if prompted; send only command output/errors. This loads the installed VirtualBox driver. If it fails, preserve the exact error for diagnosis. No forced module loading, kernel reinstall, boot-configuration edits or host group changes are part of this procedure.

## 2. Verified official image

| Item | Value |
|---|---|
| SEED page | <https://seedsecuritylabs.org/labsetup.html>, **Ubuntu 12.04 VM** section |
| Official linked source | <https://seed.nyc3.cdn.digitaloceanspaces.com/SEEDUbuntu12.04.zip> |
| Reused local archive | `/home/DHB/Downloads/SEEDUbuntu12.04.zip` |
| Bytes | `2311129278` |
| Published and observed MD5 | `6ec9c429a2f4a9163530ada20f0621dc` |
| Observed SHA-256 | `e324e3d32a916763504b51eab0d4031ab7ea56b94deff43372019c77d29d0cb8` |
| ZIP CRC test | Every entry passed |
| Extracted size | `6690191275` bytes, about 6.7 GB |
| Extracted directory | `/home/DHB/VirtualBox VMs/ISSD-Member6-media/SEEDUbuntu12.04/` |
| Base disk to attach | **`SEEDUbuntu12.04.vmdk`** |
| Extents | **41** files, `SEEDUbuntu12.04-s001.vmdk` through `-s041.vmdk` |

MD5 here compares the download with SEED's published legacy checksum. The SHA-256 records this local artifact. Keep the descriptor and every extent together. The `.vmx` is VMware metadata and the `-sNNN.vmdk` files are disk parts; choose the unsuffixed descriptor when attaching the disk.

The host extraction used:

```bash
unzip -n /home/DHB/Downloads/SEEDUbuntu12.04.zip -d "/home/DHB/VirtualBox VMs/ISSD-Member6-media"
```

The archive contains an existing disk, **not an OVA appliance or Ubuntu installer ISO**. The prepared `M6PACK` optical image is only a data-transfer CD containing repository files and official lab references.

Current transfer CD: `/home/DHB/VirtualBox VMs/ISSD-Member6-media/M6-transfer-20261007-final.iso`. Its input hashes and ISO-byte checks are recorded in `evidence/host/transfer-20261007-final.json`. The earlier initial bundle is retained for provenance. The data CD contains the original guide/checklist as well as this Arch companion, the session guide and supplemental checks.

## 3. Actual VM configuration and why

VM: **`ISSD-Member6-SEED12`**. UUID: **`242db196-83e1-4b7a-9f0b-e399d6f8b9dc`**.

| VirtualBox menu/path | Setting / expected value | Reason / what to see |
|---|---|---|
| Select VM → **Settings → General → Basic** | Ubuntu 12.04 LTS (32-bit), name above | Matches historical SEED guest; the guest release still requires S02 proof |
| **System → Motherboard** | Base Memory **2048 MB**, I/O APIC on; EFI off | Within repository's 1–2 GB recommendation; legacy BIOS matches image |
| **System → Processor** | **2 CPUs**, PAE/NX on | Allows concurrent worker scheduling; 32-bit guest support |
| **Display → Screen** | **VMSVGA**, **64 MB**, **3D disabled**, one screen | Repository starting settings; basic old-desktop compatibility |
| **Storage** | `M6-SCSI`, **LsiLogic**, attached existing disk chain | Matches `ddb.adapterType = "lsilogic"` in the supplied descriptor |
| **Storage** | `M6-IDE`, optical data CD | Offline transfer if old Guest Additions cannot mount a share |
| **System → Boot Order** | Hard Disk first, Optical second; no floppy/network boot | Boots the preinstalled disk rather than trying to install an OS |
| **Network → Adapter 1** | Enabled, **NAT**, Intel PRO/1000 MT Desktop | Repository's simple network mode; no bridge or host network setup |
| **Network → Adapter 1 → Advanced** | **Cable Connected unchecked**; port-forward table empty | No downloads are needed for first transfer; experiments are local/offline |
| **General → Advanced** | Shared Clipboard **Host to Guest**; Drag and Drop **Disabled** | Command pasting if old Guest Additions support it |
| **Shared Folders** | `M6pack` → repository's `Member6`, **Read-only**, Auto-mount off | Input transfer only; manually copy to native guest storage |
| **Shared Folders** | `M6export` → `Member6/evidence/incoming`, writable, Auto-mount off | Narrow output destination for actual evidence after collection |
| **Audio / USB** | Disabled | Not needed for this local lab; PS/2 keyboard/mouse available |

The full command trace is [evidence/host/vm-setup-20261007T181036Z.log](evidence/host/vm-setup-20261007T181036Z.log). `tools/setup-vm.sh` is the reproducible configuration script and refuses an existing VM/directory.

**After a snapshot, the active disk is a differencing VMDK under `Snapshots/`.** This is expected: its parent is the verified unsuffixed SEED VMDK. Do not replace that live differencing attachment with the base disk. Use the media manager's parent information or `VBoxManage showmediuminfo` to inspect the chain.

### MANUAL ACTION REQUIRED — VIRTUALBOX: inspect/capture S01

1. **HOST:** open VirtualBox Manager; select **ISSD-Member6-SEED12**.
2. Open **Settings → General → Basic**, **System → Motherboard/Processor**, and **Storage**. Compare with the table above. Settings are already applied; inspection is the task.
3. Capture readable views including the VM name, 32-bit type, RAM/CPU and disk. Use complementary `M6-S01-a-vm-setup.png`, `M6-S01-b-vm-setup.png`, etc., if needed.
4. On this KDE Arch desktop, use **Spectacle** (`Print Screen`, or open the Spectacle app), choose the relevant window/region and save PNGs in `/home/DHB/Downloads/ISSP/ISSD-seed-labs/Member6/evidence/`.
5. **What to see:** the actual settings in the table; a snapshot differencing disk is normal. Close Settings with **Cancel** after inspection if no deliberate setting change was made.
6. **Send back:** saved filenames/images. The agent will inspect readability and mark S01 only once the required details are visible.

## 4. Snapshots

The powered-off snapshot **`M6-clean-SEED12`** was taken before the first boot or any lab target/account changes. Snapshot UUID: **`7ecb8a4e-7430-497d-8772-fe3317d43b30`**.

### MANUAL ACTION REQUIRED — VIRTUALBOX: view or create a later snapshot

1. **HOST:** select the VM in VirtualBox Manager.
2. Open **Machine → Tools → Snapshots** (or the VM's tools/menu button → **Snapshots**).
3. You should see **M6-clean-SEED12** and **Current State** below it.
4. After the guest S08 normal-account login/backup/build checks, shut the guest down normally. Select **Current State → Take**; enter **`M6-charlie-normal-ready`**, then click **OK**.
5. Expected: that second snapshot appears under the clean snapshot. Send the snapshot list/capture, then continue Task 2.

Equivalent exact host command, after that verified guest state is powered off:

```bash
VBoxManage snapshot ISSD-Member6-SEED12 take M6-charlie-normal-ready --description "Normal charlie login checked; post-adduser backup, compiled lab and no attack process"
```

**Restoration is a manual recovery operation:** export evidence first; shut down; select the intended snapshot → **Restore**. Report which snapshot was restored. Restoring the initial clean snapshot also removes the guest workspace/account changes and may restore the empty optical drive, so reattach the transfer CD or use `M6pack` again. Preserve evidence outside the VM before this operation.

## 5. First boot

### MANUAL ACTION REQUIRED — VIRTUALBOX

1. **HOST:** only after the post-reboot driver checks pass, select **ISSD-Member6-SEED12 → Start**.
2. Expected: Ubuntu's old login screen. If there is a VirtualBox error, send the full message/details before changing settings.
3. **VM:** select/login as **seed**, password **dees** (the public SEED image's documented login).
4. Do not install offered guest updates. Open a guest terminal with **Ctrl+Alt+T** and follow [VM_SESSION_GUIDE.md](VM_SESSION_GUIDE.md), starting with the actual environment checks.
5. **Send back:** the environment output and S02 image(s). If release, architecture or kernel differs, the experiment stops for diagnosis.

For a black screen, the starting configuration is already 3D-off. Send the observed screen and VM log rather than changing the kernel. Clipboard/shared-folder failures can use the offline data CD route; the vulnerable guest need not be upgraded for transfer convenience.
