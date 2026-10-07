#!/usr/bin/env python3
"""Send public commands slowly to the already-visible Member 6 guest terminal.

The operator must first verify the terminal/prompt. Passwords are entered by
the user, never passed to this helper. This records input actions, not claimed
execution results; inspect actual guest output after every operation.
"""
from pathlib import Path
import argparse
import datetime as dt
import json
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
VM = 'ISSD-Member6-SEED12'
UUID = '242db196-83e1-4b7a-9f0b-e399d6f8b9dc'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--command', required=True)
    args = parser.parse_args()
    if not args.command or not args.command.isascii() or any(ord(c) < 32 for c in args.command):
        parser.error('Supply one ASCII command line without control characters')
    info = subprocess.check_output(['VBoxManage', 'showvminfo', VM, '--machinereadable'], text=True)
    if 'VMState="running"' not in info or 'UUID="' + UUID + '"' not in info:
        parser.error('The expected Member 6 VM is not running')
    log = ROOT / 'evidence/host/console-actions.jsonl'
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    # Release modifiers from earlier GUI shortcuts before beginning a command.
    subprocess.run(['VBoxManage', 'controlvm', VM, 'keyboardputscancode',
                    '9d', 'b8', 'aa', 'b6'], check=True)
    time.sleep(0.3)  # GUI input pacing, not waiting for an exploit/process result.
    # Ctrl+U clears stray, unexecuted readline input. It does not clear output
    # or history. Use only at the normal shell prompt verified by the operator.
    subprocess.run(['VBoxManage', 'controlvm', VM, 'keyboardputscancode',
                    '1d', '16', '96', '9d'], check=True)
    time.sleep(0.2)
    for offset in range(0, len(args.command), 8):
        subprocess.run(['VBoxManage', 'controlvm', VM, 'keyboardputstring',
                        args.command[offset:offset + 8]], check=True)
        time.sleep(0.12)
    subprocess.run(['VBoxManage', 'controlvm', VM, 'keyboardputscancode', '1c', '9c'], check=True)
    record = {'started_utc': started, 'sent_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
              'vm': VM, 'uuid': UUID, 'command': args.command,
              'input_method': 'Ctrl+U at verified prompt; VBoxManage keyboardputstring, chunks of 8, 120ms pacing',
              'execution_result': 'not inferred from successful input delivery'}
    with log.open('a') as stream:
        stream.write(json.dumps(record) + '\n')
    print('Sent to the verified VM terminal:', args.command)
    print('Check real guest output; action log:', log)


if __name__ == '__main__':
    main()
