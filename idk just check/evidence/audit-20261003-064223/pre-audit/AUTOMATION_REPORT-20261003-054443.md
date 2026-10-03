# Member 5 — remaining experiment results

Completed in the user's disposable SEED VM on 2026-10-03T06:30:42.672730-04:00 as **seed (UID 1000)**, using two visible, separately titled GNOME terminals. Task 1 and the delayed Task 2.A were completed previously; this session preserved their existing evidence and automated the remaining work.

## Measured outcomes

Every new trial had a 300-second monitor limit and its own label. Attacker processes had a separate 330-second bound. Short unsuccessful/changed-file trials ended early and retained their actual totals.

| Trial | Victim | Attempts | Monitor elapsed | Runner wall time | Observation |
|---|---|---:|---:|---:|---|
| Task 2.B retry 1 | `./vulp` | 9 | 0 s | 0.532873 s | File-exists/sticky-bit failure; no target change |
| Task 2.B retry 2 | `./vulp` | 20 | 1 s | 0.865370 s | Exact record + non-sudo login + UID 0 verified |
| Task 2.C | `./vulp` | 1 | 0 s | 0.272765 s | Exact record + non-sudo login + UID 0 verified |
| Task 3.A | `./vulp_least` | 9,455 | 300 s | 299.996265 s | No success observed; target hash unchanged |
| Task 3.B | `./vulp` | 9,177 | 300 s | 299.564373 s | No success observed; target hash unchanged |
| Task 2.B extra S08 capture | `./vulp` | 2 | 0 s | 0.378590 s | File-exists/sticky-bit failure; no target change |

The monitor uses Bash's integer `SECONDS`; a reported 0 seconds does not mean zero execution time. Runner wall time uses a monotonic clock around the monitor process, including startup and exit handling. It is not the duration of the TOCTOU instruction window.

### Existing Task 2.B failure

The pre-existing log ends at **76,000 attempts / 227 seconds**, without a final summary. Final totals for that earlier run are **unknown**. No experiment processes remained when automation began. `/tmp/XYZ` was a root-owned regular file, mode 0664, group seed, under root-owned sticky mode-1777 `/tmp`. Both original logs, metadata, and a hash-verified copy of the file were preserved before resetting. A labelled diagnostic retry produced an actual unlink `Operation not permitted`; the subsequent new retry 1 also produced the actual symlink `File exists` error. No original lost terminal output was reconstructed.

### Verified no-delay exploitation

Both Task 2.B retry 2 and Task 2.C used the original no-delay **`./vulp`**, launched as seed. Attackers and monitors were stopped before record inspection/login. Each run produced exactly this complete seven-field record:

```text
test:U6aMy0wojraho:0:0:test:/root:/bin/bash
```

Each was then tested with **non-sudo `su - test`**, followed by actual `id` and `whoami`:

```text
uid=0(root) gid=0(root) groups=0(root)
root
```

These login results, not the changed hash alone, establish root access in these lab runs. Both root shells were exited and seed identity was checked before the next reset/trial. Comparing the preserved post-attack files against the final clean baseline also confirms that each change was exactly `baseline + newline + validated record`.

The naive attacker can leave `/tmp/XYZ` missing between `unlink()` and `symlink()`. A victim that already passed `access()` can then create a root-owned regular file with `fopen(..., "a+")`; the sticky directory prevents seed from unlinking it. The initialized atomic attacker uses `renameat2(..., RENAME_EXCHANGE)` to exchange two existing links without that missing-name interval. This improves the attacker while leaving the victim's separate check/use resolutions vulnerable.

### Defence controls

* **Task 3.A:** `vulp_least`, atomic attacker, `protected_symlinks=0` and `protected_regular=0`. The bounded concurrent trial above left the target hash unchanged. With the attacker stopped, a stable `/etc/passwd` link produced `No permission`, exit 1. A stable link to seed's `allowed.txt` successfully appended `normal-operation`, demonstrating permitted functionality. The effective privilege is dropped before both `access()` and `fopen()` and stays dropped through the write/close.
* **Task 3.B:** original `vulp`, atomic attacker, `protected_symlinks=1`, `protected_regular=0`. The concurrent trial above left the target hash unchanged. With the attacker stopped, a stable seed-owned `/dev/null` link in sticky root-owned `/tmp` caused `Open failed: Permission denied`, exit 1. Thus the original real-user check could pass while the root-effective symlink follow was blocked.

Describe these finite measurements as **“no success observed in N attempts over T seconds.”** The privilege boundary/kernel rule supplies the causal explanation; the finite trials alone are not universal proof of impossibility.

## Cleanup

All experiment and su processes were checked stopped. `/etc/passwd` was restored using `/root/issd-member5-passwd.original`, compared with that backup, and matched its recorded clean SHA-256:

```text
b2386623b8c504aa933d9c519b96158bd55e5e6eb4ae75183d5abf9e5a191d67
```

There is no test record, `/tmp/XYZ` and `/tmp/ABC` are absent, and all three victim binaries are root-owned **0755**, with Set-UID removed.

The user explicitly selected final runtime settings **`fs.protected_symlinks=1`, `fs.protected_regular=2`**, matching the installed policy. These are an explicit post-lab choice, **not verified original runtime values**. The original `sysctl-before.txt` still records 0/0 and was preserved unchanged. The original password-file backup was retained.

## Evidence and provenance

* [Detailed automation/human-interaction notes](automation-20261003-054443/AUTOMATION_NOTES.md)
* [Separately verified login observations](automation-20261003-054443/verified-logins.json)
* [Exact post-attack append comparison](automation-20261003-054443/exact-append-check.json)
* `automation-20261003-054443/terminal-A.typescript`, `terminal-B.typescript` and `.timing`: full actual terminal recordings.
* `automation-20261003-054443/pre-reset-task2b/`: original failure preservation.
* `automation-20261003-054443/source-before/`: original unmodified source/helpers.
* `automation-20261003-054443/final-artifacts/`: copied final sources, monitoring/control helpers, all logs, settings and automation action records.
* [Screenshot index](CAPTURE_INDEX-20261003-054443.md): original PNG filenames, preferred figures, real framing/timing qualifications.

Commands, process coordination, records inspection, root-shell identity commands, resets, controls, screenshots, and result collection were automated. Authentication input was **not** automated or embedded in scripts. No terminal was cleared and no screenshot/output was manufactured. The monitor-only edits preserve interrupted counts and prevent label overwrites; the race/defence C programs and binaries were unchanged until final Set-UID removal.

The missing `Member5/evidence/EVIDENCE_REVIEW.md` was disclosed and the user chose the available guide/checklist instead. The first fast naive S08 capture shows the completed failed trial. A later supplemental bounded run attempted two faster GDK whole-desktop frames and failed after 2 attempts; the original frames show startup/failure, with zero frames verified to have both experiment processes live throughout capture. S09 contains the genuine successful run and verified login. A strictly simultaneous-live S08 frame remains uncollected; it would require capturing a higher-frame-rate original desktop recording before a future reset/trial and selecting a real live frame. All originals, including supplementary framing/title/burst captures, are retained.
