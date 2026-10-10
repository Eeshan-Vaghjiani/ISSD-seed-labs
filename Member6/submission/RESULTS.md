# Member 6 — expected, actual, explanation

Experiment date: **9 October 2026**. **Both official tasks, fresh non-sudo UID-0 authentication, exact restoration and final cleanup are complete and verified.** The [fresh-run record](../evidence/incoming/opus-fresh-20261008/README.md) contains the checkpoint table; the [image review](../evidence/incoming/opus-fresh-20261008/EVIDENCE_REVIEW.md) records actual observations. The VM was shut down normally after the final export was verified. The directory name ending `20261008` is the user's requested destination, not the experiment date.

## Environment record

| Field | ACTUAL established so far | Evidence |
|---|---|---|
| Host | Arch Linux x86-64; running `7.2.9-arch1-1`, ordinary DHB UID 1000 | Fresh `provenance/host-preflight-20261009T193659Z.json` |
| Installed VirtualBox | 7.2.20r175154; module vermagic matches running kernel | Same fresh host preflight |
| VM | `ISSD-Member6-SEED12`, UUID `242db196-83e1-4b7a-9f0b-e399d6f8b9dc`; **powered off normally after cleanup/export** | Fresh capture sidecars; `provenance/final-powered-off-state.json` |
| Configured profile | Ubuntu 12.04 32-bit, 2048 MB, 2 CPUs | Fresh host preflight; **not** running guest output |
| Network | NAT cable disconnected for offline lab | Fresh `provenance/network-disconnect-20261009T193746Z.json` |
| Image | Verified local official-checksum `SEEDUbuntu12.04.zip` | Host media provenance |
| Clean snapshot | `M6-clean-SEED12`, UUID `7ecb8a4e-7430-497d-8772-fe3317d43b30` | Requeried in fresh host preflight |
| Supplied sources | All four host/guest hashes match; LF source content | Fresh S03 and `provenance/native-source-prebuild-20261009.png` |
| Actual guest release | Ubuntu 12.04.2 LTS / precise | `M6-S02-environment.png` |
| Actual guest architecture | i686; `getconf LONG_BIT` = 32 | Same fresh S02 |
| Actual guest kernel/package | `3.5.0-37-generic`; `3.5.0-37.58~precise1`; `i386 linux-lts-quantal` | Fresh S02 and S02b |
| Actual guest compiler | GCC 4.6.3, Ubuntu/Linaro package `4.6.3-1ubuntu5` | Fresh S02 |
| Ordinary guest identity | seed UID/GID 1000 | Fresh S02/S03 |
| Workspace | `/home/seed/issd-member6/lab-files`, native ext4; seed-owned 0700 directory | Fresh S02b and native-source diagnostic |
| Guest build | `bash build.sh` returned 0; both binaries seed-owned 0755 ELF32 | Fresh S03; b/c source views |
| Compatibility checks | Guest guard and Python 2.7.3 verifier parse returned 0; timeout returned 124 | `provenance/pretrial-state-20261009.png` |
| Transfer shares | M6pack read-only; M6export writable during export. M6pack explicitly unmounted; normal shutdown closed remaining mounts | Mount records, S13, `provenance/final-powered-off-state.json` |
| Prepared normal-charlie snapshot | `M6-charlie-normal-ready`, UUID `0d3457ab-f5ce-4606-8bee-1842809ca831` | Powered-off snapshot creation record; normal login/backup/reset verified first |

Fresh paths above are relative to `../evidence/incoming/opus-fresh-20261008/`. The initial inspection found `/zzz` and charlie absent. The dummy was created for Task 1; charlie was subsequently created with UID **1001**, GID **1002**. Its ordinary login was verified before preserving `/root/issd-member6-passwd.normal`. The protected backup was compared byte-for-byte before the powered-off prepared snapshot. Both native transcripts are now closed, exported and hash-verified. Their original bytes, including authentication failures and terminal control sequences, are retained under `logs/`.

## Experiment ledger

| Experiment | EXPECTED | ACTUAL | EXPLANATION / next verification |
|---|---|---|---|
| Dummy baseline/direct write | Root:root 0644, original 19 bytes; ordinary write denied | Exact `111111222222333333\n` created; seed redirection denied with exit 1; fresh content/hash unchanged | S04 confirms normal file permissions prevent the direct write |
| Normal COW | Private view changes; fresh file/hash unchanged | Private memory `111111******333333\n`; backing file remains original; saved-hash check passes and full baseline `cmp` returns 0 | S05 and `logs/fresh-control-01.txt`; writable private mapping/direct memcpy stays private, unlike the exploit's read-only mapping and process-memory path |
| Task 1 Dirty COW | Full `111111******333333\n` backing-file replacement possible in prescribed vulnerable guest | **EXACT SUCCESS**, `fresh-t1-01`; 30-second limit, 0 integer elapsed seconds; root:root 0644 and 19-byte length retained | S06/S07, actual before/after copies, live verifier and independent offline artifact check agree; no race-attempt count was measured |
| Charlie normal baseline | New nonzero UID, working normal login, post-adduser backup preserved | Fresh login returned UID 1001 / GID 1002 and whoami charlie; protected full baseline matched | S08 and S08b; only root was in the saved numeric UID-0 list; prepared snapshot taken powered off |
| Task 2 UID overwrite | Only original UID digits become same-width zeroes | **EXACT SUCCESS**, `fresh-t2-01`: `1001` → `0000`; all other file bytes unchanged | S09/S09b; live and offline full-file checks; root:root 0644 and 2040 bytes retained |
| Task 2 actual privilege | Fresh non-sudo `su - charlie` gives numeric UID 0 if successful | First authentication failed; second succeeded: `uid=0(root) gid=1002(charlie) groups=0(root),1002(charlie)`; `id -u` = 0; `whoami` = root | S10 and native transcript. Failure cause was not established. No second exploit was needed; password entry remained interactive |
| Account restoration | Full normal file restored; new charlie login gets original nonzero UID | Proof shell PID 3392 exited and was absent; full file/hash restored; fresh non-sudo login returned UID 1001, whoami charlie; exited to seed | S10b, S11/S11b, restored full copy/metadata and final offline export check |
| Patched comparison | Valid dummy trial leaves file unchanged, interpreted with fixed package evidence | **NOT PERFORMED — DISCUSSION ONLY (OPTIONAL)** | No measured patched-VM result claimed |
| Final cleanup | No attacker/test privileged shell; exact normal account state; `/zzz` removed; exports retained | Checker returned 0: no attacker/wrapper/control/su/root shell, original UID-0 list `root:0`, `/zzz` absent, binaries ordinary 0755 | S13, `logs/fresh-cleanup-01.txt`; closed final archive verified on host; VM powered off normally |

## Trial measurements

| Run label | Mode | Limit | Actual integer elapsed seconds | Outcome | Errors | Evidence |
|---|---|---|---|---|---|---|
| `fresh-t1-01` | dummy | 30 s | **0** | Exact full replacement; live file equals saved after-copy; owner/mode/length retained | No error output in the three-line program log | S06/S07; `logs/fresh-t1-01-*`; `provenance/fresh-t1-01-offline-check.json` |
| `fresh-t2-01` | passwd | 30 s | **0** | Exact UID-field-only replacement; live file equals saved after-copy; owner/mode/length retained | No error output in the three-line program log; later authentication failure recorded separately | S09/S09b; `logs/fresh-t2-01-*`; `provenance/fresh-t2-01-offline-check.json` |

The run began at **2026-10-09 13:28:48 -0700** (20:28:48 UTC). It stopped after detecting a content change. `Elapsed: 0s` is the supplied wrapper's integer wall-time result, **not zero execution time**. No finer runtime or kernel-level attempt count was measured. This was the first and only Task 1 attack trial in this fresh session; no retries were needed.

* Before SHA-256: `7342e673ad4f9a5ea02fe84fa6ab1760d922e3f362c885ef4feda980423b9552`
* After/live SHA-256: `97c0ed6bb0deb556349015713d1c0a86d11e1bf5572a78b087650e814479b47b`
* Before and after metadata: `0:0:644:19` (UID:GID:mode:bytes).
* Program real/effective UID: **1000 / 1000**; target byte offset **6**, replacement length **6**.

The fresh expected-byte comparison `cmp /zzz <(printf '111111******333333\n')` returned 0. The guest verifier reported `ACTUAL: exact-change` and `live_file_checked: true`, after confirming no attacker/wrapper remained. The host offline verifier independently accepted the exported complete copies, metadata and summary/program logs. JSON verification was kept in separate logs rather than displayed in the selected terminal captures.

The target's `ls -l` time still displayed its setup minute (13:19) after the 13:28 attack. The fresh read and content hashes established the change; the displayed timestamp alone would not have done so. The dummy was reset to its verified original content before the prepared snapshot, then removed after Task 2 cleanup.

### Task 2 measurements and exact identity chain

The sole Task 2 exploit began at **2026-10-09 14:17:08 -0700** (21:17:08 UTC). The unchanged wrapper measured **0 integer elapsed seconds** under its 30-second limit. Copy timestamps are not substituted for an independently measured race runtime. No kernel-level attempt count was measured.

```text
Before/restored: charlie:x:1001:1002:,,,:/home/charlie:/bin/bash
After attack:   charlie:x:0000:1002:,,,:/home/charlie:/bin/bash
```

* Before/restored SHA-256: `3edf14347c28c11d3a8816326e14baa3b99b569f1dc33dd15cd7d953c91dc337`
* After/live SHA-256: `99fced9d0853d999474f92617022e78efe7c87b0f63450da264c46bfa9d47cd2`
* Before, after and restored metadata: **`0:0:644:2040`**.
* Program real/effective UID: **1000 / 1000**; target byte offset **2002**, replacement width **4**. Two positions already contained `0`; the operation replaces the entire four-character UID field, not four necessarily different bytes.
* Fresh login after attack: **UID 0**, GID **1002**, whoami **root**. The first `su` returned `Authentication failure`; the successful retry is visible in the same S10 image. Its cause is unknown.
* Proof shell PID **3392** exited before restoration; subsequent `ps` and `pgrep su` returned no matching process with exit 1.
* Fresh login after restoration: **UID 1001**, GID **1002**, whoami **charlie**; final caller **seed UID 1000**.

### Export and cleanup qualifications

`member6-fresh-final-20261009.tar.gz` has SHA-256 **`08fe8d346f51f506a6b205683ead027d031a7d9fca34839045af7595bbb35fa1`**. The host inspected all 46 file entries, compared original source hashes, checked the closed transcript against the native hash, compared the complete restored account file to the pre-attack copy, and verified the cleanup log. See `provenance/final-export-verification.json`.

The first pre-Task 2 transcript lacked a `Script done on` footer. An initial footer-based assertion failed and is documented in `provenance/pre-task2-export-verification.json`. Closure was subsequently established from recorder/process exit and matching native/copied/archive bytes; no footer was added. Final recording closure was verified the same way.

M6pack was explicitly unmounted successfully. After leaving the recording shell, a noninteractive M6export unmount returned password-required and left that share mounted. The verified final archive was already on the host. A normal guest ConsoleKit shutdown followed, and VirtualBox reported `VMState="poweroff"`; this closed remaining guest mounts. No successful explicit M6export unmount is claimed.

## Report completion map

`REPORT.md` follows the ten-section structure in `../REPORT_TEMPLATE.md` and interprets these observations with factual captions, limitations and assistance attribution. All four allocation countermeasures are covered. The cover uses **Member 6 — ISSD**, approved by the user; course identity/deadline/format and speaking allowance remain unconfirmed. A future spoken rehearsal and course upload are human actions.
