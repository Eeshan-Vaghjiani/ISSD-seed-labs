#!/usr/bin/env python3
"""Inspect the complete real record before a separately verified non-sudo login."""
import hashlib
import os
from pathlib import Path
import subprocess
import sys

lab = Path('/home/seed/issd-member5/lab-files')
if os.getuid() != 1000 or os.geteuid() != 1000:
    sys.exit('Start record inspection from the seed shell.')
print('+ id', flush=True)
subprocess.run(['id'], check=True)
print("+ pgrep -a -x 'attack_naive|attack_atomic|vulp|vulp_slow|vulp_least'", flush=True)
check = subprocess.run(['pgrep', '-a', '-x', 'attack_naive|attack_atomic|vulp|vulp_slow|vulp_least'])
if check.returncode != 1:
    sys.exit('An experiment process remains, or the process check failed.')
print('No attacker/victim processes remain.', flush=True)
expected = (lab / 'input.txt').read_text().rstrip('\n')
data = Path('/etc/passwd').read_bytes()
records = [line for line in data.decode().splitlines() if line.startswith('test:')]
print('+ grep -n "^test:" /etc/passwd', flush=True)
subprocess.run(['grep', '-n', '^test:', '/etc/passwd'], check=True)
if records != [expected]:
    sys.exit('Expected exactly one complete matching test record; inspect manually.')
fields = records[0].split(':')
if len(fields) != 7 or fields[2:4] != ['0', '0'] or fields[5:] != ['/root', '/bin/bash']:
    sys.exit('The complete seven-field UID-0 record was not verified.')
print('Exact input record count: 1; fields: 7; UID=0; GID=0', flush=True)
print('Home=/root; shell=/bin/bash; record length={}'.format(len(records[0])), flush=True)
print('+ getent passwd test', flush=True)
subprocess.run(['getent', 'passwd', 'test'], check=True)
print('SHA-256: ' + hashlib.sha256(data).hexdigest(), flush=True)
print('Record inspection passed. Root login still requires non-sudo su and id.', flush=True)
