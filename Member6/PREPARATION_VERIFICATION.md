# Member 6 — preparation verification record

Checked on **7 October 2026**. **Preparation passed; actual guest execution remains blocked by the host reboot prerequisite.** This is not a completed experimental report.

## Retained records

| Record | What was actually checked |
|---|---|
| [Repository inventory](evidence/host/repository-audit-20261007.json) | All 616 initial tracked files and applicable format/syntax checks; 19 M5 original-image selections, 24 exact crop derivatives, seven trial/summary consistency checks; no errors |
| [Host inventory](evidence/host/host-inventory-20261007.json) | Actual Arch kernel/package/module state and VirtualBox version; driver mismatch and absent `/dev/vboxdrv` |
| [VM setup trace](evidence/host/vm-setup-20261007T181036Z.log) | Exact successful creation/configuration/attachment commands and powered-off clean snapshot |
| [Final transfer provenance](evidence/host/transfer-20261007-final.json) | Official ZIP MD5/SHA-256/all-entry CRC; real PDF/source ZIP; every frozen source/reference/guide file compared with its ISO bytes |
| [Final pre-boot verification](evidence/host/preparation-verification-20261007.json) | Saved profile/resources/display/network, read-only/writable share scopes, real base/differencing disk relationship, all 41 extents, final data-CD attachment/hash, source manifest and helper syntax |

## Additional checks actually performed

* All four supplied lab files are byte-identical to baseline commit `2906f262d2f9364dc8dddd3ec69a9087b4b413de`; no lab executable was built on Arch.
* The three existing Member 6 DOCX files passed formatting-aware paragraph/table-cell comparison with their Markdown sources. Literal stars in target strings and nested inline backticks were preserved in that comparison. This is a text check, not a claim of visual pagination review.
* In-memory comparator checks confirmed complete dummy replacement, UID-only equal-width replacement, and rejection of zero-UID, duplicate or malformed charlie baselines. These are helper-unit checks, not generated VM evidence.
* Actual invocations of the guest environment/copy/cleanup guards on this Arch host exited with `STOP: expected the 32-bit SEED guest; actual architecture=x86_64.` The live-file verifier likewise rejected the host before live-target access.
* All Member 6 Markdown fences/local file links checked clean at final preparation review. `git diff --check` passed. Tracked changes are confined to Member 6.
* The final check found **zero M6-S screenshot PNGs**. Therefore no guest evidence checkpoint has been marked as a collected screenshot.

## Exact reproducible pre-boot check

Read-only, from the repository on the host:

```bash
python Member6/tools/verify-preparation.py
```

This checker expects the **current pre-first-boot powered-off state**. It is not the guest environment checker and should not be used to claim later experiment or cleanup completion. Use `automation/check-environment.sh` inside the verified guest and the checkpoint-by-checkpoint capture plan after boot.

## Unverified work

Guest boot/release/kernel package, old-runtime helper compatibility, C compilation, normal COW, Task 1, Task 2, real login privileges, account restoration, final cleanup, evidence export, final experimental report/PPTX, oral rehearsal and course submission remain unverified/unperformed as appropriate. The optional patched comparison is explicitly discussion-only. See [EXECUTION_STATUS.md](EXECUTION_STATUS.md) for every checkpoint and [ARCH_HOST_SETUP.md](ARCH_HOST_SETUP.md) for the immediate manual action.
