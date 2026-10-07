# Member 6 — expected, actual, explanation

Record date: **7 October 2026**. **No guest experiment has run.** The cause is the host's running-kernel/VirtualBox-module mismatch; see `../ARCH_HOST_SETUP.md` and the raw host inventory.

## Environment record

| Field | ACTUAL established so far | Evidence |
|---|---|---|
| Host | Arch Linux x86-64; running `7.2.8-arch1-2` | `../evidence/host/host-inventory-20261007.json` |
| Installed VirtualBox | 7.2.20r175154 | Same host inventory |
| VM | `ISSD-Member6-SEED12`, UUID `242db196-83e1-4b7a-9f0b-e399d6f8b9dc` | VM setup log |
| Configured profile | Ubuntu 12.04 32-bit, 2048 MB, 2 CPUs | VM setup log; **not** running guest output |
| Image | Verified local official-checksum `SEEDUbuntu12.04.zip` | Host media provenance |
| Clean snapshot | `M6-clean-SEED12`, UUID `7ecb8a4e-7430-497d-8772-fe3317d43b30` | VM setup/snapshot log |
| Actual guest release | **Not observed — first boot pending** | S02 missing |
| Actual guest architecture | **Not observed**; required 32-bit | S02 missing |
| Actual guest kernel/package | **Not observed**; historical expected kernel `3.5.0-37-generic` | S02 missing |
| Actual guest GCC/UID/filesystem | **Not observed** | S02/S03 missing |
| Prepared normal-charlie snapshot | **Not created yet** | S08 pending |

## Experiment ledger

| Experiment | EXPECTED | ACTUAL | EXPLANATION / next verification |
|---|---|---|---|
| Dummy baseline/direct write | Root:root 0644, original 19 bytes; ordinary write denied | **NOT EXECUTED** | Need S04 and actual baseline hash |
| Normal COW | Private view changes; fresh file/hash unchanged | **NOT EXECUTED** | Need S05; distinguish writable private control from read-only exploit mapping |
| Task 1 Dirty COW | Full `111111******333333\n` backing-file replacement possible in prescribed vulnerable guest | **NOT EXECUTED** | Need actual labelled trial, full byte diff, current hash/mode, S06/S07 |
| Charlie normal baseline | New nonzero UID, working normal login, post-adduser backup preserved | **NOT EXECUTED** | Need S08; record assigned UID rather than assuming 1001 |
| Task 2 UID overwrite | Only original UID digits become same-width zeroes | **NOT EXECUTED** | Need S09, full-file comparison and unchanged metadata |
| Task 2 actual privilege | Fresh non-sudo `su - charlie` gives numeric UID 0 if successful | **NOT EXECUTED** | Need actual authenticated S10 output; text/hash alone insufficient |
| Account restoration | Full normal file restored; new charlie login gets original nonzero UID | **NOT EXECUTED** | Need S11 and proof prior UID-0 shells ended |
| Patched comparison | Valid dummy trial leaves file unchanged, interpreted with fixed package evidence | **NOT PERFORMED — DISCUSSION ONLY (OPTIONAL)** | No measured patched-VM result claimed |
| Final cleanup | No attacker/test privileged shell; exact normal account state; `/zzz` removed; exports retained | **NOT EXECUTED** | Need S13 and host-verified export after the actual lab |

## Trial measurements

**No trial labels, elapsed times, hashes or original charlie UID have yet been measured in the VM.** Add one row per actual attempt after its logs arrive, including failures. Preserve the original summary/program/before/after files. A missing final summary remains incomplete; do not infer its runtime from expectations.

Required columns when real trials exist: `run label | mode | limit | actual integer elapsed seconds | before hash | after hash | exact/partial/unchanged | errors | screenshot paths | explanation`.

## Report completion map

Use `../REPORT_TEMPLATE.md` §§1–2 and §4 for the prepared concepts; tie §§3, 5–6, 8–9 to the observations above after execution. §7 must cover all four allocation countermeasures even if S12 is unperformed. Add factual image captions, code provenance and assistance attribution in §10. The final conclusion must state exactly which protected-file and privilege results the VM output establishes.
