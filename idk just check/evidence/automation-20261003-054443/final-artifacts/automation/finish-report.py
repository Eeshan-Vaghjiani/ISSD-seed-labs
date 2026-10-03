#!/usr/bin/env python3
"""Build a run report from actual completed logs plus separately reviewed logins.

Run after both defence controls and final cleanup. It performs no experiment
or privileged operation and refuses incomplete/contradictory run data.
"""
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import shutil

BASE = Path('/home/seed/issd-member5')
LAB = BASE / 'lab-files'
EVIDENCE = BASE / 'evidence'
STATE = json.loads((BASE / 'automation/desktop-state.json').read_text())
SESSION = STATE['session']
DETAILS = Path(STATE['evidence'])


def main():
    logins = json.loads((DETAILS / 'verified-logins.json').read_text())
    labels = [('Task 2.B retry 1', 'task2b-retry1-'),
              ('Task 2.B retry 2', 'task2b-retry2-'),
              ('Task 2.C', 'task2c-'), ('Task 3.A', 'task3a-'), ('Task 3.B', 'task3b-')]
    if (LAB / 'logs' / ('task2b-capture-' + SESSION + '-result.json')).exists():
        labels.append(('Task 2.B extra S08 capture', 'task2b-capture-'))
    rows = []
    results = {}
    for title, prefix in labels:
        label = prefix + SESSION
        data = json.loads((LAB / 'logs' / (label + '-result.json')).read_text())
        if data['attempts'] is None or data['monitor_elapsed_seconds'] is None:
            raise RuntimeError('Missing measured totals for ' + label)
        if not data['attacker_confirmed_stopped']:
            raise RuntimeError('Attacker stop was not verified')
        if title.startswith('Task 3.'):
            if data['changed'] or data['monitor_elapsed_seconds'] < 300:
                raise RuntimeError('Defence trial needs review: ' + label)
            outcome = 'No success observed; target hash unchanged'
        elif data['changed']:
            if title == 'Task 2.B extra S08 capture' and not logins.get(label, {}).get('verified'):
                outcome = 'Exact record inspected; no separate login/root claim for this supplemental run'
            elif not logins.get(label, {}).get('verified'):
                raise RuntimeError('Changed hash without separately verified login')
            else:
                outcome = 'Exact record + non-sudo login + UID 0 verified'
        else:
            outcome = 'File-exists/sticky-bit failure; no target change'
        rows.append('| {} | `{}` | {:,} | {} s | {:.6f} s | {} |'.format(
            title, data['victim'], data['attempts'], data['monitor_elapsed_seconds'],
            data['runner_wall_seconds'], outcome))
        results[label] = data

    control_a = (LAB / 'logs' / ('task3a-' + SESSION + '-controls.txt')).read_text()
    control_b = (LAB / 'logs' / ('task3b-' + SESSION + '-controls.txt')).read_text()
    allowed = (LAB / 'logs' / ('task3a-' + SESSION + '-allowed-after.txt')).read_bytes()
    if 'Static protected-target exit=1' not in control_a or 'No permission' not in control_a:
        raise RuntimeError('Review the least-privilege static control')
    if allowed != b'ordinary writable file\n\nnormal-operation':
        raise RuntimeError('Review the permitted-file write')
    if 'Static symlink-follow exit=1' not in control_b or 'Open failed: Permission denied' not in control_b:
        raise RuntimeError('Review the symlink-protection static control')

    baseline = Path('/etc/passwd').read_bytes()
    expected_hash = (BASE / 'passwd-before.sha256').read_text().split()[0]
    if hashlib.sha256(baseline).hexdigest() != expected_hash:
        raise RuntimeError('Final password-file baseline does not match')
    if any(line.startswith(b'test:') for line in baseline.splitlines()):
        raise RuntimeError('Test account remains')
    for name in ('vulp', 'vulp_slow', 'vulp_least'):
        if (LAB / name).stat().st_mode & 0o4000:
            raise RuntimeError('Set-UID still present: ' + name)
    for name in ('/tmp/XYZ', '/tmp/ABC'):
        if Path(name).exists() or Path(name).is_symlink():
            raise RuntimeError('Lab path remains: ' + name)
    append_check = {}
    record = (LAB / 'input.txt').read_bytes().rstrip(b'\n')
    for label in logins:
        after = (LAB / 'logs' / (label + '-passwd-after.txt')).read_bytes()
        append_check[label] = after == baseline + b'\n' + record
        if not append_check[label]:
            raise RuntimeError('Account database changed beyond the exact expected append')
    (DETAILS / 'exact-append-check.json').write_text(json.dumps(append_check, indent=2) + '\n')

    artifact_dir = DETAILS / 'final-artifacts'
    artifact_dir.mkdir(exist_ok=True)
    for folder in ('source', 'automation', 'logs'):
        (artifact_dir / folder).mkdir(exist_ok=True)
    for path in LAB.iterdir():
        if path.suffix in ('.c', '.sh') or path.name == 'input.txt':
            shutil.copy2(path, artifact_dir / 'source' / path.name)
    for path in (BASE / 'automation').iterdir():
        if path.is_file():
            shutil.copy2(path, artifact_dir / 'automation' / path.name)
    for path in (LAB / 'logs').iterdir():
        if path.is_file():
            shutil.copy2(path, artifact_dir / 'logs' / path.name)
    for name in ('sysctl-before.txt', 'passwd-before.sha256'):
        shutil.copy2(BASE / name, artifact_dir / name)
    shutil.copy2('/home/seed/Desktop/files/ISSD-seed-labs/Member5/README.md',
                 artifact_dir / 'README.md')

    report = EVIDENCE / ('AUTOMATION_REPORT-' + SESSION + '.md')
    text = '''# Member 5 — remaining experiment results

Completed in the user's disposable SEED VM on {date} as **seed (UID 1000)**, using two visible, separately titled GNOME terminals. Task 1 and the delayed Task 2.A were completed previously; this session preserved their existing evidence and automated the remaining work.

## Measured outcomes

Every new trial had a 300-second monitor limit and its own label. Attacker processes had a separate 330-second bound. Short unsuccessful/changed-file trials ended early and retained their actual totals.

| Trial | Victim | Attempts | Monitor elapsed | Runner wall time | Observation |
|---|---|---:|---:|---:|---|
{rows}

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
{baseline_hash}
```

There is no test record, `/tmp/XYZ` and `/tmp/ABC` are absent, and all three victim binaries are root-owned **0755**, with Set-UID removed.

The user explicitly selected final runtime settings **`fs.protected_symlinks=1`, `fs.protected_regular=2`**, matching the installed policy. These are an explicit post-lab choice, **not verified original runtime values**. The original `sysctl-before.txt` still records 0/0 and was preserved unchanged. The original password-file backup was retained.

## Evidence and provenance

* [Detailed automation/human-interaction notes](automation-{session}/AUTOMATION_NOTES.md)
* [Separately verified login observations](automation-{session}/verified-logins.json)
* [Exact post-attack append comparison](automation-{session}/exact-append-check.json)
* `automation-{session}/terminal-A.typescript`, `terminal-B.typescript` and `.timing`: full actual terminal recordings.
* `automation-{session}/pre-reset-task2b/`: original failure preservation.
* `automation-{session}/source-before/`: original unmodified source/helpers.
* `automation-{session}/final-artifacts/`: copied final sources, monitoring/control helpers, all logs, settings and automation action records.
* [Screenshot index](CAPTURE_INDEX-{session}.md): original PNG filenames, preferred figures, real framing/timing qualifications.

Commands, process coordination, records inspection, root-shell identity commands, resets, controls, screenshots, and result collection were automated. Authentication input was **not** automated or embedded in scripts. No terminal was cleared and no screenshot/output was manufactured. The monitor-only edits preserve interrupted counts and prevent label overwrites; the race/defence C programs and binaries were unchanged until final Set-UID removal.

The missing `Member5/evidence/EVIDENCE_REVIEW.md` was disclosed and the user chose the available guide/checklist instead. The first fast naive S08 capture shows the completed failed trial. A later supplemental bounded run attempted two faster GDK whole-desktop frames and failed after 2 attempts; the original frames show startup/failure, with zero frames verified to have both experiment processes live throughout capture. S09 contains the genuine successful run and verified login. A strictly simultaneous-live S08 frame remains uncollected; it would require capturing a higher-frame-rate original desktop recording before a future reset/trial and selecting a real live frame. All originals, including supplementary framing/title/burst captures, are retained.
'''.format(date=dt.datetime.now().astimezone().isoformat(), rows='\n'.join(rows),
           baseline_hash=expected_hash, session=SESSION)
    report.write_text(text)
    print(report)
    print('Completed logs, control output, exact append, and final unprivileged binaries checked.')


if __name__ == '__main__':
    main()
