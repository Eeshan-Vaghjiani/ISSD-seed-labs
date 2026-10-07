# Member 6 — execution checkpoint audit

Status date: **7 October 2026**. **Assignment incomplete: host reboot blocks first VM boot.** Preparation is recorded below; experimental success is not claimed.

Final pre-boot configuration/source/media checks passed and are retained in [PREPARATION_VERIFICATION.md](PREPARATION_VERIFICATION.md). The final data CD is attached; its frozen inputs match the repository files.

## CHECKPOINT | STATUS | EVIDENCE | VERIFICATION

| CHECKPOINT | STATUS | EVIDENCE | VERIFICATION |
|---|---|---|---|
| Repository audit | **Complete** | [Audit](REPOSITORY_AUDIT.md), `evidence/host/repository-audit-20261007.json` | All 616 original tracked files inventoried; applicable format/syntax/integrity checks passed; complete M6 requirements read |
| Arch diagnosis | **Complete; manual reboot needed** | `evidence/host/host-inventory-20261007.json` | Running 7.2.8, installed headers/VirtualBox module for 7.2.9; `/dev/vboxdrv` absent |
| Official image | **Verified and extracted** | [Host setup](ARCH_HOST_SETUP.md), host media provenance | Exact official MD5, local SHA-256 and all-entry ZIP CRC; split disk descriptor + 41 extents |
| Offline transfer | **Prepared** | `evidence/host/transfer-20261007-final.json` | Source/reference/guide data CD; every input checked against ISO bytes; guest copy still pending |
| Clean snapshot | **Complete** | `evidence/host/vm-setup-20261007T181036Z.log` | `M6-clean-SEED12`, UUID `7ecb8a4e-7430-497d-8772-fe3317d43b30`, before first boot |
| **M6-S01** | **VM configured; screenshot pending** | Actual VM setup log; `M6-S01-*.png` not yet collected | Correct profile/resources/disk chain; needs readable host settings capture |
| **M6-S02** | **Blocked — unobserved** | No environment PNG/log from guest yet | Need actual release/kernel/package/architecture/UID/GCC after boot |
| **M6-S03** | **Prepared; guest build pending** | Original source manifest; host syntax/guard checks only | Need native guest transfer, real `bash build.sh`, ordinary ELF32 modes, code capture |
| **M6-S04** | **Not executed** | No dummy baseline evidence | Need exact root:root 0644 file, denied direct write, actual hash |
| **M6-S05** | **Not executed** | No control evidence | Need actual private output versus unchanged backing-file read/hash |
| **M6-S06** | **Not executed** | No actual trial log/capture | Need original bounded ordinary-user dummy race and real summary |
| **M6-S07** | **Not executed** | No Task 1 result | Need exact whole-file replacement, actual live read/hash and unchanged ownership/mode |
| **M6-S08** | **Not executed** | No charlie baseline/login/backup record | Need actual original UID/login and one-time post-adduser backup; prepared snapshot pending |
| **M6-S09** | **Not executed** | No account trial/diff | Need same-length UID-only change, full comparison and actual runtime |
| **M6-S10** | **Not executed** | No privilege proof | Need real fresh non-sudo `su - charlie` → `id -u` = 0 |
| **M6-S11** | **Not executed** | No restoration proof | Need exact normal file and fresh original-nonzero-UID login; end old root shells |
| **M6-S12** | **Optional — not performed; discussion only** | Countermeasure theory in existing report/plan | No empirical patched-VM outcome claimed |
| **M6-S13** | **Not executed** | No post-experiment cleanup proof | Need stopped processes/shells, normal baseline, absent `/zzz`, organised/exported artifacts |
| Report | **Structure/concepts prepared; actual findings pending** | Existing `REPORT_TEMPLATE.md`, [results ledger](submission/RESULTS.md) | Final report must be populated only from guest evidence |
| Presentation | **Notes/command sheet prepared; findings deck/rehearsal pending** | Existing plan, `submission/SLIDE_NOTES.md`, `submission/LIVE_COMMANDS.md` | Six-slide evidence order/Q&A prepared; no recorded demo or spoken rehearsal yet |

## TASK 1

* **Status:** not executed.
* **ACTUAL:** no `/zzz` baseline, control output, race result or trial duration has been observed in the VM.
* **Evidence:** none for S04–S07 yet; collection/verification helpers are prepared.
* **Remaining:** pass S02/S03, establish baseline, run control and supplied bounded race, inspect exact backing file/metadata, retain all trials and screenshots.

## TASK 2

* **Status:** not executed.
* **ACTUAL:** charlie's UID and login state are unobserved; no account attack or restoration has run.
* **Evidence:** none for S08–S11 yet.
* **Remaining:** create/test normal account, preserve baseline once, take prepared snapshot, run UID-only experiment, authenticate without sudo for numeric privilege proof, exit all privileged shells and verify restoration.

## ENVIRONMENT

* **VM:** `ISSD-Member6-SEED12`, registered and powered off, UUID `242db196-83e1-4b7a-9f0b-e399d6f8b9dc`.
* **Architecture:** configured x86 / 32-bit; **actual guest `uname -m` not yet observed**.
* **Kernel:** required historical `3.5.0-37-generic`; **actual guest running kernel/package not yet observed**.
* **Resources:** 2048 MB, 2 CPUs, VMSVGA 64 MB, 3D off; NAT cable disconnected; separate disk/snapshot chain.
* **Current host blocker:** driver built for installed 7.2.9 while 7.2.8 is still running. [Manual reboot and exact checks](ARCH_HOST_SETUP.md#1-what-is-actually-installed).

## Next manual handoff

1. Save host work and manually reboot; send `uname -r`, `dkms status`, `modinfo -F vermagic vboxdrv`, `ls -l /dev/vboxdrv`, and `VBoxManage list vms`.
2. After driver readiness, start the named VM and log in. Send actual S02 outputs before experiments.
3. Password entry, required screen positioning/captures and any root-shell exits remain explicit manual gates. The agent can continue automation and evidence review after these inputs.
4. Confirm course identity/deadline/format/speaking allowance with the group. Complete a timed rehearsal and the course upload after the practical and documents are finished.

The snapshot is a verified **pre-execution rollback point**, not substitute evidence for S11/S13 cleanup. No assignment-complete claim is warranted at this checkpoint.
