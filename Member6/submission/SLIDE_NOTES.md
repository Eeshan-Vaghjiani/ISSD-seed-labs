# Member 6 — speaker notes and evidence order

**Preparation only; results slides await real VM evidence.** This follows the six slides in `../PRESENTATION_PLAN.md`, rather than substituting another tutorial or Member 5's results. Use `LIVE_COMMANDS.md` for terminal transitions.

| Slide / order | Evidence to insert after verification | Short explanation to say |
|---|---|---|
| 1. Dirty COW, before the demo | CVE-2016-5195 and the assignment's kernel/application distinction | “Copy-on-write should keep a process's private changes separate from the original file. Dirty COW is a historical local kernel race that can break that boundary.” |
| 2. Normal COW and the race | Diagram from the existing guide; readable S03 worker/mapping excerpts; S05 control | “The main thread opens the file read-only and maps it privately. One worker writes its own `/proc/self/mem`; the other discards mapping state with `MADV_DONTNEED`. Their concurrent kernel handling is the critical race.” |
| 3. Correct environment and protection | S01/S02; S04 denied ordinary write | “The website category says 20.04, but the lab explicitly requires the old 32-bit 12.04 image. These guest commands establish the actual kernel and user. The target is already protected by normal file permissions.” Use the actual S02 package value, currently unobserved. |
| 4. Live dummy demonstration | Actual live terminal; real S07 as fallback once collected | “First the ordinary write is denied. The normal control changes only its private view. Next I run the repository's bounded race and check the file itself.” Then describe exactly what the new run shows. |
| 5. Recorded account impact | S08 original UID; S09 exact diff; S10 login; S11 restoration | “The field width is preserved and only charlie's UID digits change. The meaningful privilege proof is a new non-sudo login followed by numeric UID output. The restored account is tested with another new login.” State the observed values only after verification. |
| 6. Countermeasures and takeaway | S13; S12 only if really performed | “The primary defence is a fixed kernel that is actually booted. Keep supported systems updated, limit unnecessary local code execution, and monitor account integrity and privileged sessions. Monitoring supports detection; it does not repair COW.” |

Suggested timing from the repository: 40/50/45/90/50/60 seconds, adjusted to the group. Setup, passwords and display switching also consume time. The short dummy demonstration is live; the fuller account experiment is normally shown as genuine recorded evidence.

## Concepts to explain accurately

* **COW / MAP_PRIVATE:** private writes should update a private page, not the backing file.
* **Read-only mapping:** a normal direct write through a `PROT_READ` pointer would fault. The control deliberately uses a writable private mapping; the exploit uses another memory-access path.
* **`/proc/self/mem`:** the calling process's own address space. The `pwrite` offset is a virtual address, not a protected-file offset.
* **`MADV_DONTNEED`:** discards relevant page state so later access can refault/repopulate; this alone is not the privilege bypass.
* **Race:** outcome depends on concurrent interleaving in affected kernel COW handling. Repetition does not supply a guaranteed success time.
* **Normal direct writing:** target owner/mode denies ordinary seed; setup/reset sudo commands are separate administrative actions.
* **UID 0:** the numeric identity supplies root authority even if the name or GID differs. Updating the account file does not change existing processes' credentials.
* **Patched behaviour:** correct COW handling preserves the backing file; a finite failed attempt needs valid setup and vendor package evidence, not just a timeout.

## Likely lecturer questions

| Question | Concise answer |
|---|---|
| Why use 12.04 when the URL says 20.04? | The official task specifies the separate historical 32-bit SEED 12.04 guest; the directory name is not the runtime requirement. |
| Is every 12.04 kernel vulnerable? | No. Inspect the running kernel and package family; distribution backports matter. |
| Why does `MAP_PRIVATE` normally keep the file intact? | Changes belong to a private copy rather than being propagated to the mapped backing file. |
| Why not use ordinary file writes? | Seed lacks write permission; the exploit races the kernel's memory/COW path instead. |
| Is the control identical except for one missing thread? | No. It uses a writable private mapping and direct memory writes; the exploit mapping is read-only and uses `/proc/self/mem`. |
| What is special about `pwrite` here? | It writes the process-memory interface at a virtual address in one call; it replaces the upstream seek/write pair. |
| Why do both workers repeat? | The vulnerable interleaving is timing-dependent, so repeated concurrent operations create opportunities; runtime is not a guarantee. |
| Why `0000` instead of `0`? | Same-width in-place overwrite preserves separators/other fields; a one-byte replacement would leave old digits. Actual width follows the measured UID. |
| Did a changed hash prove root? | No. Full file/record verification and a fresh non-sudo `su - charlie` followed by numeric UID 0 are separate requirements. |
| Why might `whoami` print root? | UID 0 may resolve to the first account named root; numeric UID is the privilege evidence. |
| Does restoring passwd revoke old root shells? | No. Existing processes retain credentials; those shells must be exited and a new login checked. |
| Does Member 5's symlink defence fix this? | No. Member 5 races pathname operations in an application; this bug is in kernel COW handling. |
| Can a short timeout prove a kernel fixed? | No. It is a finite observation, interpreted with error-free setup and package/advisory evidence. |
| How does it connect to authentication? | A write-protection failure can undermine the account database that login trusts, without needing to crack charlie's password. |

## Completion gate for the final deck

Insert only reviewed originals or explicitly identified readability crops, preserve failure qualifications, replace pending guest fields from S02, and fill trial durations from their labelled logs. Keep source attribution to **Wenliang Du / SEED Labs, CC BY-NC-SA 4.0**, plus the actual assistance disclosure. The existing preparation outline and these notes are ready; an evidence-based final PPTX and timed rehearsal remain pending.
