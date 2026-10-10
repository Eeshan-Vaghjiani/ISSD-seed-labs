#!/usr/bin/env python3
"""Save an unaltered VirtualBox guest framebuffer and capture provenance.

Show the real command/output in the guest first. This tool cannot create or
reconstruct terminal output. S01 is a separate host VirtualBox-settings capture.
"""
from pathlib import Path
import argparse
import datetime as dt
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
VM = 'ISSD-Member6-SEED12'
UUID = '242db196-83e1-4b7a-9f0b-e399d6f8b9dc'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('filename', help='M6-S02-environment.png, or a checkpoint/suffix filename')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'evidence',
                        help='Existing host directory for this fresh capture and its provenance')
    args = parser.parse_args()
    if not re.fullmatch(r'M6-S(?:0[2-9]|1[0-3])-[a-z0-9-]+\.png', args.filename):
        parser.error('Use an M6-S02 through M6-S13 PNG filename; use a new suffix for another capture')
    output_dir = args.output_dir.resolve()
    if not output_dir.is_dir():
        parser.error('The capture output directory must already exist')
    destination = output_dir / args.filename
    provenance = destination.with_suffix('.capture.json')
    if destination.exists() or provenance.exists():
        parser.error('Existing capture: preserve it and choose a fresh a/b/c suffix')
    info = subprocess.run(['VBoxManage', 'showvminfo', VM, '--machinereadable'],
                          text=True, capture_output=True, check=True)
    if 'UUID="' + UUID + '"' not in info.stdout.splitlines():
        parser.error('The named VM does not have the required Member 6 UUID')
    if 'VMState="running"' not in info.stdout.splitlines():
        parser.error('The named VM is not running; there is no live guest framebuffer to capture')
    command = ['VBoxManage', 'controlvm', UUID, 'screenshotpng', str(destination)]
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    result = subprocess.run(command, text=True, capture_output=True, check=True)
    data = destination.read_bytes()
    if not data.startswith(b'\x89PNG\r\n\x1a\n'):
        raise RuntimeError('VirtualBox output is not a PNG; inspect the retained file')
    record = {'source': 'VirtualBox screenshotpng: actual guest framebuffer, unedited',
              'vm': VM, 'uuid': UUID, 'command': command, 'started_utc': started,
              'ended_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
              'filename': destination.name, 'sha256': hashlib.sha256(data).hexdigest(),
              'stdout': result.stdout, 'stderr': result.stderr,
              'vminfo_at_capture': info.stdout, 'content_reviewed': False}
    with provenance.open('x') as stream:
        json.dump(record, stream, indent=2)
        stream.write('\n')
    print('Captured actual framebuffer:', destination)
    print('SHA-256:', record['sha256'])
    print('Review readability and command/result context before marking the checkpoint complete.')


if __name__ == '__main__':
    main()
