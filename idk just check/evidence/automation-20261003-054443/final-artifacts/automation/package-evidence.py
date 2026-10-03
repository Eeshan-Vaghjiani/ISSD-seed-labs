#!/usr/bin/env python3
"""Index preserved originals and package the completed, reviewed evidence session."""
import datetime as dt
import difflib
import hashlib
import json
from pathlib import Path
import re
import shutil
import tarfile

BASE = Path('/home/seed/issd-member5')
EVIDENCE = BASE / 'evidence'
STATE = json.loads((BASE / 'automation/desktop-state.json').read_text())
SESSION = STATE['session']
DETAILS = Path(STATE['evidence'])

NOTES = {
    'S06-task2a-timing': 'Pre-existing user capture; delayed Task 2.A. Retained unchanged.',
    'S07-task2a-result': 'Pre-existing user capture; delayed Task 2.A login. Retained unchanged.',
    'S08-task2b-trial': 'Real retry-1 failure captured immediately after startup. Both processes had already ended; not a live-running screenshot.',
    'S08c-task2b-supplemental-failure': 'Supplemental capture run: actual File exists error, 2-attempt interruption, root-owned regular XYZ, sticky /tmp and unchanged target. Preserved before cleanup.',
    'S09-task2b-result': 'Real full-record/login/UID-0 result. Supplementary original: root shell changed the B header title.',
    'S09b-task2b-result-titled': 'Both terminal titles restored; genuine UID-0 output. An early custom root prompt used a literal dollar sign; id establishes identity.',
    'S09c-task2b-verified-return-to-seed': '**Preferred Task 2.B result:** measured retry-2 summary, full record, non-sudo su, UID 0, exit and seed UID 1000.',
    'S10-task2b-sticky-bit': 'Initial pre-reset preservation capture. Original kept; /tmp mode scrolled above the frame, so use S10b too.',
    'S10b-task2b-sticky-bit': '**Preferred original-failure checkpoint:** real diagnostic unlink error, root-owned regular XYZ, mode-1777 /tmp, preserved original-log context.',
    'S10c-task2b-retry1-file-exists': '**Preferred new failure:** actual File exists error in retry 1, root ownership/mode and measured interruption count.',
    'S11a-task2c-atomic-trial': 'Atomic-exchange source/method, initialization, and actual one-attempt file-change summary. Captured after the fast trial ended.',
    'S11b-task2c-atomic-result': '**Preferred Task 2.C result:** atomic method, measured summary, complete record, non-sudo su and actual UID 0.',
    'S12a-task3a-running': 'Genuine concurrent least-privilege trial, initial settings 0/0, seed identity and privilege-drop excerpt.',
    'S12b-task3a-300-second-result': '**Preferred Task 3.A trial:** full 300-second summary, attempts, actual last denied open, unchanged hash and stopped attacker.',
    'S12c-task3a-code-and-controls': 'Fix/source excerpt, stable target denial and permitted-file operation. Original trace shows the no-final-newline output adjacent to a trace line.',
    'S12d-task3a-readable-control-result': '**Preferred Task 3.A controls:** privilege-drop/open/write/restore excerpt, denied protected write, clean hash, readable allowed-file contents and settings 0/0.',
    'S13a-task3b-running': 'Genuine concurrent original-vulp trial, initialized atomic attacker, seed identity, settings 1/0 and Set-UID victim permissions.',
    'S13b-task3b-300-second-result': '**Preferred Task 3.B trial:** full 300-second actual summary, unchanged hash and stopped attacker.',
    'S13c-task3b-symlink-protection': '**Preferred Task 3.B controls:** original victim, seed-owned stable link under sticky /tmp, actual denied open, clean target and settings 1/0.',
    'S14-cleanup': '**Cleanup:** actual baseline restore/comparison, no test account, removed Set-UID and lab paths, stopped processes, selected final 1/2 policy.',
    'S14b-cleanup-summary': '**Preferred compact cleanup:** visible final identity, protections, original-baseline comparison and 0755 victims.',
    'S15-deliverables': 'Actual evidence/source/log inventory and results summary in the visible evidence terminals.',
}


def main():
    report = EVIDENCE / ('AUTOMATION_REPORT-' + SESSION + '.md')
    if not report.exists():
        raise RuntimeError('Create the completed and checked report first')
    events = [json.loads(line) for line in (BASE / 'automation/desktop-actions.jsonl').read_text().splitlines()]
    captures = {Path(event['file']).name: event for event in events if event['action'] == 'original-screenshot'}
    rows = []
    for image in sorted(EVIDENCE.glob('*.png')):
        stem = re.sub(r'-\d{8}-\d{6}(?:-\d{6})?\.png$', '', image.name)
        event = captures.get(image.name)
        mode = 'Automated desktop capture' if event else 'Pre-existing user capture'
        digest = hashlib.sha256(image.read_bytes()).hexdigest()
        if event and digest != event['sha256']:
            raise RuntimeError('Original screenshot changed: ' + image.name)
        note = NOTES.get(stem, 'Retained original; consult its actual image and capture action record.')
        if stem == 'S08b-task2b-live-frame':
            if event and event.get('both_experiment_processes_live'):
                note = '**Live Task 2.B frame:** both attacker and monitor PID/start-time identities were live immediately before and after this real desktop capture. Supplemental run; see its actual final log for outcome.'
            else:
                note = 'Original fast-capture frame during supplemental startup/termination; not designated proof that both processes were still running.'
        rows.append('| [{}]({}) | {} | {} |'.format(image.name, image.name, mode, note))
    index = EVIDENCE / ('CAPTURE_INDEX-' + SESSION + '.md')
    index.write_text('''# Member 5 — original screenshot index

All listed PNGs are preserved originals. New captures were taken automatically from the actual visible desktop, then inspected with the image-read tool. The control window was minimized; no image was edited or output manufactured. Supplementary captures address framing/title issues without removing originals. Names alone are not proof of outcome: the notes identify what each image actually shows.

| Original image | Provenance | Use / framing note |
|---|---|---|
''' + '\n'.join(rows) + '''

The `prior-user-captures/` folder, if present, contains additional unchanged copies of repository screenshots. `copy-manifest.json` records their original paths and hashes; copying a prior screenshot does not make its capture automated.

Full commands/results and timing are retained in the session's `.typescript`/`.timing` logs. Full PNG hashes, capture dimensions and window geometry/minimization metadata are in `automation/desktop-actions.jsonl` and its final-artifact copy.
''')

    # Refresh the final copy after the last screenshot and history flush.
    artifact = DETAILS / 'final-artifacts'
    for path in (BASE / 'automation').iterdir():
        if path.is_file():
            shutil.copy2(path, artifact / 'automation' / path.name)
    original = (DETAILS / 'source-before/run_trials.sh').read_text().splitlines(True)
    changed = (BASE / 'lab-files/run_trials.sh').read_text().splitlines(True)
    (DETAILS / 'monitor-changes.diff').write_text(''.join(difflib.unified_diff(
        original, changed, fromfile='original/run_trials.sh', tofile='working/run_trials.sh')))

    manifest = EVIDENCE / ('SHA256SUMS-' + SESSION + '.txt')
    entries = []
    for path in sorted(EVIDENCE.rglob('*')):
        if path.is_file() and path != manifest:
            entries.append(hashlib.sha256(path.read_bytes()).hexdigest() + '  ' + str(path.relative_to(EVIDENCE)))
    manifest.write_text('\n'.join(entries) + '\n')
    exports = BASE / 'exports'
    exports.mkdir(mode=0o700, exist_ok=True)
    archive = exports / ('member5-evidence-' + SESSION + '.tar.gz')
    if archive.exists():
        raise RuntimeError('Archive already exists; refusing to replace it')
    with tarfile.open(archive, 'w:gz') as bundle:
        bundle.add(EVIDENCE, arcname='member5-evidence-' + SESSION)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (exports / (archive.name + '.sha256')).write_text(digest + '  ' + archive.name + '\n')
    print(index)
    print(manifest)
    print(archive)
    print('Archive SHA-256: ' + digest)
    print('Packaged at ' + dt.datetime.now().astimezone().isoformat())


if __name__ == '__main__':
    main()
