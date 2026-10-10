# Member 6 — execution helpers

Both tasks, restoration and cleanup were completed on **9 October 2026**. Use [the verified results](../submission/RESULTS.md) for that run and [the preparation guide](../submission/LIVE_PREPARATION.md) for a future rehearsal. These helpers supplement the supplied four lab files. `SOURCE_SHA256SUMS` identifies those originals at repository commit `2906f262d2f9364dc8dddd3ec69a9087b4b413de`.

| Helper | Purpose | Invocation / effects |
|---|---|---|
| `guest-guard.sh` | Shared environment/process checks | Source-only functions; rejects Arch, another release/kernel, root, or shared-folder execution |
| `check-environment.sh` | Print real identity/release/kernel/package/tool output | Read-only; run before experiments; review package provenance too |
| `prepare-workspace.sh` | Copy the pack from `M6pack` or the data CD | Creates a new `/home/seed/issd-member6`; refuses an existing workspace; does not build |
| `trial-with-evidence.sh` | Add stat metadata and a transcript around the supplied trial | Calls the **unchanged** `bash run_trial.sh MODE SECONDS LABEL` inside the guarded guest |
| `verify-trial.py` | Compare complete file bytes, hashes, metadata and actual logs | Offline mode reads the supplied log prefix only; `--live` first guards the guest, checks stopped processes, and reads the actual backing file |
| `check-cleanup.sh` | Check the post-restoration state | Read-only, including `sudo cmp` of the root-held baseline; does not restore/remove files or authenticate |
| `export-evidence.sh` | Archive existing source, logs, provenance and captures | Creates a uniquely named guest export; excludes root's backup, shadow/key files and binaries |

## Trial command

Inside the verified guest, as `seed`:

```bash
cd ~/issd-member6/lab-files
bash ../automation/trial-with-evidence.sh dummy 30 task1-run1
```

The corresponding account command is used only after S08's normal login, one-time backup, provenance hashes and prepared snapshot:

```bash
bash ../automation/trial-with-evidence.sh passwd 30 task2-run1
```

The wrapper's extra files are `<label>-metadata-before.txt`, `-metadata-after.txt`, and `-session.txt`; the supplied helper still produces its own `-summary.txt`, `-program.txt`, `-before.txt` and `-after.txt`. A nonzero return or `partial-or-unexpected-change` requires inspection. A changed hash is never sufficient for a privilege claim.

`verify-trial.py` returns 0 for an exact expected file change with consistent artifacts and ordinary identity, 2 for an observed unchanged/partial/error-bearing result, and 1 for incomplete/inconsistent evidence. It **always leaves `login_verified` false**: S10 requires a separate actual `su - charlie` → `id` → `id -u` session. It does not convert expected bytes into an actual-result file.

After exporting, an Arch-side read-only artifact check is:

```bash
python Member6/automation/verify-trial.py dummy /path/to/export/lab-files/logs/task1-run1
```

Omit `--live` on the host. The ordinary prescribed-guest verifier intentionally does not classify a different kernel's optional patched test; review S12 separately using its actual package/advisory and run logs.

## Compatibility and validation status

The shell helpers target Bash 4.x and use `pgrep -x` plus `ps`, avoiding reliance on newer `pgrep -a`. The verifier uses Python 2.7/3-compatible syntax. Host syntax checks, in-memory comparator checks, and rejection of the actual Arch host passed on 7 October 2026. In the **9 October fresh guest run**, the guard, environment/build checks, Python 2.7 whole-file verifier, cleanup checker and export helper were exercised successfully. The supplied `run_trial.sh` was invoked directly and visibly for each task, with metadata and detailed verification recorded separately. The alternative `trial-with-evidence.sh` route shown above is not the invocation claimed for those two fresh trials. See the retained transcripts and final-export records in `../evidence/incoming/opus-fresh-20261008/`.

Authentication stays interactive. Enter passwords only at the VM's password prompts. The report should disclose that these helpers assist collection/verification, while the supplied C programs perform the experiment.
