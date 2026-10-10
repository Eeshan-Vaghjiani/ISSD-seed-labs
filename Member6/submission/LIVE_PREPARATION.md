# Live preparation — Member 6 — ISSD

The verified practical is complete. This guide prepares a **future short dummy-file demonstration** using the existing VM and real recorded Task 2 evidence. A spoken rehearsal and its duration have not been measured.

## 1. What is already ready

* VM **ISSD-Member6-SEED12**, UUID **242db196-83e1-4b7a-9f0b-e399d6f8b9dc**, is powered off normally after cleanup and verified export.
* Guest is Ubuntu 12.04.2, i686/32-bit, kernel **3.5.0-37-generic**, package **3.5.0-37.58~precise1 / linux-lts-quantal**, GCC 4.6.3.
* Native workspace is **/home/seed/issd-member6/lab-files**. Both compiled programs remain seed-owned 0755 ELF32, with original source hashes.
* Charlie is an ordinary **UID 1001 / GID 1002** account. The protected post-creation baseline remains **/root/issd-member6-passwd.normal**.
* `/zzz` was removed; a future demo must prepare it again. The network cable is disconnected.
* Snapshots **M6-clean-SEED12** and **M6-charlie-normal-ready** are retained. The prepared snapshot includes the original dummy and normal charlie; the latest cleaned state has the dummy absent.

The input/output shares need not be mounted to run the demo. The programs execute on native ext4. Opening this document directory on the host does not place the host terminal inside the guest.

## 2. Open the VM and presentation

**MANUAL ACTION REQUIRED — VIRTUALBOX / HOST**

In VirtualBox Manager select **ISSD-Member6-SEED12 → Start**. The equivalent host command is:

```bash
VBoxManage startvm 242db196-83e1-4b7a-9f0b-e399d6f8b9dc --type gui
```

Expected: the historical Ubuntu guest login screen. Log in as **seed** directly in the VM and open **Ctrl+Alt+T**. Keep passwords out of documents/chat. Use Part 0 of `LIVE_DEMO.md` for environment, source, baseline and target preparation.

On the host open `MAIN_PRESENTATION.pptx` or its PDF, `LIVE_COMMANDS.pdf`, and the genuine fallback images/video. Confirm the projector can display the terminal text. A normal solid terminal background and readable font are sufficient. Explain the meaning of the output as it appears; leave long diagnostic traces in logs.

## 3. Presentation route

| Main slide | What to do | Provisional time |
|---|---|---|
| 1 — Dirty COW | Define local kernel race and protected-file impact | 40 s |
| 2 — COW and workers | Explain private isolation, process-memory write and discard | 50 s |
| 3 — Environment/protection | State measured kernel/identity and denied ordinary write | 45 s |
| 4 — Live dummy | Switch to the prepared guest; control → bounded race → full result | 90 s |
| 5 — Recorded account impact | Exact UID-only change and genuine non-sudo UID-0 evidence | 50 s |
| 6 — Defences and conclusion | Four required themes; exact restoration and cleanup | 60 s |

This totals about **5 minutes 35 seconds before extra switching**, following the repository's suggested 5–7-minute slot. It is a plan, not a measured spoken duration. Course allowance is unconfirmed. Slides 7–10 are backup evidence/reference slides. A full fallback-video playback needs additional time; use the static S10 proof for the shorter route.

## 4. Rehearse once with genuine output

1. Follow `LIVE_DEMO.md` Part 0, with a unique recording and trial label.
2. Explain COW before running the control. State the baseline owner/mode and seed's numeric identity.
3. Execute Part 1 at speaking pace. Check the full backing file, retained mode and verifier result. Preserve a timeout/partial/error honestly if it occurs.
4. Switch to recorded Task 2 using Part 2. Clearly say that it was recorded on 9 October.
5. Explain why a fresh login is necessary and why file restoration does not revoke old process credentials.
6. Complete Part 3 cleanup, close/export the transcript, and record your actual spoken time.

A further account exploit is not required for the short classroom route; the completed account trial, failed/successful authentication, exact restoration and cleanup are already evidenced. The classroom live target is the identified dummy.

## 5. Recorded evidence to keep open

| Claim | File |
|---|---|
| Correct environment | evidence/M6-S02-environment.png and b |
| Normal write denied | evidence/M6-S04-dummy-baseline.png |
| Normal private COW | evidence/M6-S05-normal-cow.png |
| Exact dummy result | evidence/M6-S07-task1-result.png |
| Original ordinary charlie | evidence/M6-S08-charlie-baseline.png |
| Exact UID-only diff | evidence/M6-S09-b-task2-uid-change.png |
| Fresh non-sudo UID 0 | evidence/M6-S10-task2-root-proof.png |
| New ordinary login after restore | evidence/M6-S11-account-restored.png |
| Final cleanup | evidence/M6-S13-cleanup.png |
| Native recorded fallback | video/TASK2_FALLBACK.mp4; read video/README.md for edit boundaries |

The native uncut WebM recordings and original capture sidecars remain in the fresh evidence folder. The playable fallback uses explicitly labelled excerpts. It does not reconstruct terminal text.

## 6. Recover a missing helper or damaged session

If the workspace/helper is missing, first check the VM name, `pwd`, and the native directory. The main prepared VM already contains the helpers. Do not interpret a host checkout or shared folder as that native workspace. Use the existing `Member6/VM_SESSION_GUIDE.md` transfer procedure if recovery is genuinely needed; preserve unfamiliar existing data before copying.

If an unexpected account-file change or privileged shell is found, stop the demonstration and preserve the actual output. Use the documented normal backup/restoration sequence only for identified lab state. Do not blindly restore over unrelated new accounts. Snapshot recovery is a last-resort complete VM-state rollback.

**MANUAL ACTION REQUIRED — VIRTUALBOX / HOST, only for needed recovery**

1. Verify all useful guest evidence has been exported and checked on the host.
2. Shut the guest down normally; confirm **Powered Off**.
3. VirtualBox Manager → **ISSD-Member6-SEED12 → Snapshots → M6-charlie-normal-ready → Restore**. Read the restore dialog and preserve any desired current state.
4. Boot, authenticate as seed, then repeat Part 0. Expected: ordinary charlie UID 1001, the matching protected backup, original dummy and no attacker. Confirm these rather than assuming the snapshot name proves them.

## 7. Human handoff

The user approved **Member 6 — ISSD** as the document identity. Confirm any required personal/class/group/lecturer details, submission deadline/channel, file format and speaking allowance with the course. Review the final report/deck, rehearse the transitions, and upload/present through the required channel. No course submission or oral delivery has occurred automatically.

Source/task attribution: **Wenliang Du / SEED Labs, CC BY-NC-SA 4.0**. See the report for the GPT-6 Astra/OpenCode assistance disclosure.
