#!/usr/bin/env python3
"""Read-only pre-boot configuration/source/media verification, with an optional record.

This checks host preparation, not M6 screenshots, guest compilation or results.
"""
from pathlib import Path
import argparse
import ast
import datetime as dt
import hashlib
import json
import platform
import re
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
VM = 'ISSD-Member6-SEED12'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    record = {'scope': 'HOST preparation only; guest experiments remain unexecuted',
              'recorded_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
              'host_kernel': platform.release(), 'checks': [], 'commands': []}

    def command(argv):
        result = subprocess.run(argv, text=True, capture_output=True)
        record['commands'].append({'command': argv, 'exit_code': result.returncode,
                                   'stdout': result.stdout, 'stderr': result.stderr})
        result.check_returncode()
        return result.stdout

    def check(name, passed, actual=None):
        record['checks'].append({'check': name, 'passed': bool(passed), 'actual': actual})
        print(('PASS: ' if passed else 'FAIL: ') + name)

    text = command(['VBoxManage', 'showvminfo', VM, '--machinereadable'])
    values = {}
    for line in text.splitlines():
        match = re.fullmatch(r'("[^"\n]+"|[A-Za-z0-9_-]+)=(.*)', line)
        if match:
            key, value = match.groups()
            try:
                values[key.strip('"')] = json.loads(value)
            except ValueError:
                values[key.strip('"')] = value
    expected = {'name': VM, 'platformArchitecture': 'x86',
                'ostype': 'Ubuntu 12.04 LTS (Precise Pangolin) (32-bit)',
                'memory': 2048, 'cpus': 2, 'vram': 64, 'graphicscontroller': 'vmsvga',
                'accelerate3d': 'off', 'pae': 'on', 'longmode': 'off', 'ioapic': 'on',
                'firmware': 'BIOS', 'boot1': 'disk', 'nic1': 'nat', 'nic2': 'none',
                'cableconnected1': 'off', 'clipboard': 'hosttoguest',
                'draganddrop': 'disabled', 'VMState': 'poweroff',
                'CurrentSnapshotName': 'M6-clean-SEED12'}
    for name, wanted in expected.items():
        check('VM ' + name, values.get(name) == wanted, values.get(name))
    check('No configured NAT port forwarding', not re.search(r'^Forwarding\(', text, re.M))
    command(['VBoxManage', 'snapshot', VM, 'list', '--machinereadable'])
    machine = ET.parse(values['CfgFile']).getroot().find('{http://www.virtualbox.org/}Machine')
    ns = {'v': 'http://www.virtualbox.org/'}
    shares = {p.get('name'): dict(p.attrib) for p in machine.findall('v:Hardware/v:SharedFolders/v:SharedFolder', ns)}
    check('Read-only M6pack share', shares['M6pack']['writable'] == 'false' and
          shares['M6pack']['hostPath'] == str(ROOT), shares['M6pack'])
    check('Dedicated M6export share', shares['M6export']['writable'] == 'true' and
          shares['M6export']['hostPath'] == str(ROOT / 'evidence/incoming'), shares['M6export'])
    base = machine.find('v:MediaRegistry/v:HardDisks/v:HardDisk', ns)
    base_path = Path(base.get('location'))
    children = base.findall('v:HardDisk', ns)
    active_uuid = '{' + values['M6-SCSI-ImageUUID-0-0'] + '}'
    check('Active differencing disk has verified SEED base parent',
          base_path.name == 'SEEDUbuntu12.04.vmdk' and base_path.is_file() and
          any(p.get('uuid') == active_uuid for p in children),
          {'base': str(base_path), 'active_uuid': active_uuid})
    command(['VBoxManage', 'showmediuminfo', 'disk', values['M6-SCSI-ImageUUID-0-0']])
    check('All 41 split base-disk extents present',
          all((base_path.parent / ('SEEDUbuntu12.04-s%03d.vmdk' % i)).is_file() for i in range(1, 42)))
    bundle = json.loads((ROOT / 'evidence/host/transfer-20261007-final.json').read_text())
    iso = Path(bundle['iso'])
    check('Final data CD attached', values.get('M6-IDE-0-0') == str(iso), values.get('M6-IDE-0-0'))
    check('Final ISO SHA-256 matches provenance', sha(iso) == bundle['iso_sha256'], bundle['iso_sha256'])
    changed_inputs = [item['path'] for item in bundle['inputs']
                      if sha(ROOT / item['path']) != item['sha256']]
    check('Every frozen bundle input still matches source', not changed_inputs, changed_inputs)
    for line in (ROOT / 'lab-files/SOURCE_SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ', 1)
        check('Original source ' + name, sha(ROOT / 'lab-files' / name) == digest, digest)
    scripts = sorted(ROOT.rglob('*.sh'))
    for path in scripts:
        command(['bash', '-n', str(path)])
    check('Bash syntax checks', True, len(scripts))
    programs = sorted(ROOT.rglob('*.py'))
    for path in programs:
        ast.parse(path.read_text(), filename=str(path))
    check('Python AST checks (no guest code executed)', True, len(programs))
    screenshots = sorted(p.name for p in (ROOT / 'evidence').glob('M6-S*.png'))
    record['m6_screenshot_files'] = screenshots
    record['guest_runtime_verified'] = False
    record['experiment_result_verified'] = False
    record['vboxdrv_device_exists'] = Path('/dev/vboxdrv').exists()
    print('M6 screenshot files present:', len(screenshots))
    print('Guest/runtime/results verification: pending first boot.')
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x') as stream:
            json.dump(record, stream, indent=2)
            stream.write('\n')
        print('Saved:', args.output)
    return 0 if all(item['passed'] for item in record['checks']) else 1


if __name__ == '__main__':
    raise SystemExit(main())
