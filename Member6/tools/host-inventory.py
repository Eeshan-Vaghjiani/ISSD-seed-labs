#!/usr/bin/env python3
"""Read-only Arch/VirtualBox inventory; optionally save raw output as HOST evidence."""
from pathlib import Path
import argparse
import datetime as dt
import json
import platform
import shlex
import shutil
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='New JSON record; refuses overwrites')
    args = parser.parse_args()
    commands = [
        ['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], ['uname', '-r'], ['uname', '-m'], ['id'],
        ['pacman', '-Q', 'virtualbox', 'virtualbox-host-dkms', 'linux', 'linux-headers', 'dkms'],
        ['dkms', 'status'], ['modinfo', 'vboxdrv'],
        ['VBoxManage', '--version'], ['VBoxManage', 'list', 'vms'],
        ['VBoxManage', 'list', 'runningvms'],
    ]
    record = {'scope': 'ARCH HOST ONLY; not SEED guest evidence',
              'recorded_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
              'kernel': platform.release(), 'architecture': platform.machine(),
              'os_release': Path('/etc/os-release').read_text(), 'commands': [],
              'module_trees': sorted(p.name for p in Path('/usr/lib/modules').iterdir()),
              'vboxdrv_device_exists': Path('/dev/vboxdrv').exists(),
              'vboxdrv_loaded': Path('/sys/module/vboxdrv').exists(),
              'free_disk_bytes': shutil.disk_usage(Path.home()).free}
    print(record['scope'])
    for command in commands:
        print('\n+ ' + shlex.join(command), flush=True)
        try:
            result = subprocess.run(command, text=True, capture_output=True, timeout=30)
            item = {'command': command, 'exit_code': result.returncode,
                    'stdout': result.stdout, 'stderr': result.stderr}
        except (OSError, subprocess.TimeoutExpired) as error:
            item = {'command': command, 'exit_code': None, 'error': str(error)}
        record['commands'].append(item)
        print(item.get('stdout', ''), end='')
        print(item.get('stderr', ''), end='')
        print('Exit:', item['exit_code'])
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x') as stream:
            json.dump(record, stream, indent=2)
            stream.write('\n')
        print('Saved host record:', args.output)


if __name__ == '__main__':
    main()
