# Member 6 evidence checklist

**Completed fresh run — 9 October 2026.** Checked items below are supported by the genuine images and matching logs in [incoming/opus-fresh-20261008/](incoming/opus-fresh-20261008/README.md). See its [image review](incoming/opus-fresh-20261008/EVIDENCE_REVIEW.md) for the exact observations and complementary captures. The timing/requirements columns remain the capture specification for a future run.

| Done | Filename | When | Required evidence |
|---|---|---|---|
| [x] | `M6-S01-vm-setup.png` | After VM configuration | Separate SEED12 VM, 32-bit type, RAM/CPU and disk; includes c/d host views |
| [x] | `M6-S02-environment.png` | First guest checks | Ordinary UID, Ubuntu release, actual kernel/package, architecture, GCC; includes b |
| [x] | `M6-S03-code-build.png` | After compiling | Successful build, normal executable mode and readable thread/mapping code; includes b/c |
| [x] | `M6-S04-dummy-baseline.png` | Before dummy attack | Root-owned mode 0644 file, starting content and ordinary write denied |
| [x] | `M6-S05-normal-cow.png` | Normal control | Private mapping changed, fresh backing-file read/hash unchanged |
| [x] | `M6-S06-task1-running.png` | During/after first bounded trial | Actual command, ordinary identity, mapping details, summary; captured after completion |
| [x] | `M6-S07-task1-result.png` | After Task 1 success | Exact full replacement with original restrictive ownership/mode |
| [x] | `M6-S08-charlie-baseline.png` | Before account attack | Original charlie record, nonzero UID, normal login and backed-up baseline; includes b |
| [x] | `M6-S09-task2-uid-change.png` | After account trial | Exact diff changing only same-length UID digits, actual runtime; includes b |
| [x] | `M6-S10-task2-root-proof.png` | Fresh charlie login | Non-sudo `su - charlie`, `id` and `id -u` = 0; b confirms proof-shell exit |
| [x] | `M6-S11-account-restored.png` | After reset | Original normal UID restored and new login has nonzero UID; includes b |
| Not performed | `M6-S12-patched-comparison.png` — no image claimed | Optional separate patched VM | Discussion only; no patched measurement |
| [x] | `M6-S13-cleanup.png` | End of session | Stopped attack, exited root sessions, normal lab account, removed dummy; final export verified |

## Caption template

**Figure [NUMBER] — [TASK].** I executed `[COMMAND]` as `[USER/UID]` on `[VM/KERNEL]`. The output showed `[ACTUAL OBSERVATION]`. This demonstrates `[SPECIFIC CONCLUSION]` because `[EXPLANATION]`.

Save accompanying unique-labelled summary/program logs, before/after diffs and final code. Actual file hashes and a fresh file read matter more than a successful memory-write return value. Do not include guest shadow-file contents or passwords in evidence. Optional comparison not run? Mark it not performed rather than leaving an ambiguous success claim.
