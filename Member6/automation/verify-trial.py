#!/usr/bin/env python
"""Read actual trial artifacts; optionally compare with the stopped live guest.

Python 2.7 / 3 compatible for the historical SEED VM. Offline mode reads ONLY
the supplied log prefix, so it is also usable on Arch after exporting evidence.
This program does not execute an attack, modify a target, or authenticate.
"""
from __future__ import print_function
import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys


def load(path):
    with open(path, 'rb') as stream:
        return stream.read()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def one(pattern, data, description):
    matches = re.findall(pattern, data, re.M)
    if len(matches) != 1:
        raise ValueError('Expected exactly one ' + description)
    return matches[0]


def expected_change(mode, before):
    if mode == 'dummy':
        if before != b'111111222222333333\n':
            raise ValueError('Dummy before-copy is not the complete prescribed baseline')
        return b'111111******333333\n', {'before_content': before.decode('ascii')}
    uid = one(br'^charlie:x:([0-9]+):[^\n]*$', before, 'normal charlie record')
    record = one(br'^(charlie:[^\n]*)$', before, 'charlie record').split(b':')
    if len(record) != 7 or int(uid) == 0:
        raise ValueError('Charlie baseline must have seven fields and a nonzero UID')
    match = re.search(br'^charlie:x:([0-9]+):', before, re.M)
    start, end = match.span(1)
    expected = before[:start] + b'0' * len(uid) + before[end:]
    return expected, {'before_uid_text': uid.decode('ascii'),
                      'before_uid_numeric': int(uid), 'uid_byte_width': len(uid)}


def metadata(path):
    text = load(path).decode('ascii').strip()
    fields = text.split(':')
    if len(fields) != 4:
        raise ValueError('Invalid stat metadata: ' + path)
    uid, gid, mode, size = fields
    return [int(uid), int(gid), int(mode, 8), int(size)]


def audit(mode, prefix, live=False):
    if live:
        here = os.path.dirname(os.path.abspath(__file__))
        guard = os.path.join(here, 'guest-guard.sh')
        # All live-target access follows the guest guard, including reads.
        subprocess.check_call(['bash', '-c', 'source "$1"; m6_require_guest', 'm6', guard])
        subprocess.check_call(['bash', '-c', 'source "$1"; m6_no_attacker', 'm6', guard])
    before = load(prefix + '-before.txt')
    after = load(prefix + '-after.txt')
    summary = load(prefix + '-summary.txt').decode('utf-8')
    program = load(prefix + '-program.txt').decode('utf-8')
    expected, details = expected_change(mode, before)
    target = '/zzz' if mode == 'dummy' else '/etc/passwd'
    logged_before = one(r'^Before: ([0-9a-f]{64})  ' + re.escape(target) + r'$', summary, 'before hash')
    logged_after = one(r'^After: ([0-9a-f]{64})  ' + re.escape(target) + r'$', summary, 'after hash')
    if logged_before != sha(before) or logged_after != sha(after):
        raise ValueError('Saved copies disagree with summary hashes')
    kernel = one(r'^Kernel: (.+)$', summary, 'kernel')
    if kernel != '3.5.0-37-generic':
        raise ValueError('This verifier expects the prescribed vulnerable-guest trial, not a different kernel')
    identity = one(r'^Identity: (.+)$', summary, 'identity')
    ruid, euid = one(r'^RUID=(\d+) EUID=(\d+) target=' + re.escape(target) +
                    r' file-byte-offset=\d+ length=\d+$', program, 'program identity')
    if int(ruid) == 0 or ruid != euid or not identity.startswith('uid=' + ruid + '(seed) '):
        raise ValueError('Ordinary seed real/effective identity was not established')
    elapsed = int(one(r'^Elapsed: (\d+)s$', summary, 'elapsed time'))
    limit = int(one(r'^Limit: (\d+)s$', summary, 'runtime limit'))
    changed = before != after
    if one(r'^Change detected: (yes|no)$', summary, 'change status') != ('yes' if changed else 'no'):
        raise ValueError('Summary change status disagrees with file copies')
    pre = metadata(prefix + '-metadata-before.txt')
    post = metadata(prefix + '-metadata-after.txt')
    if pre != [0, 0, 0o644, len(before)] or post != [0, 0, 0o644, len(after)]:
        raise ValueError('Target ownership, mode or recorded size is inconsistent')
    healthy_output = (len(program.splitlines()) == 3 and
                      program.splitlines()[1] ==
                      'O_RDONLY + PROT_READ + MAP_PRIVATE; racing memory writes and MADV_DONTNEED.' and
                      program.splitlines()[2] ==
                      'Run bounded trials with run_trial.sh; Ctrl+C stops a direct run.')
    exact = after == expected
    result = {'mode': mode, 'prefix': prefix, 'kernel_from_summary': kernel,
              'identity_from_summary': identity, 'ruid': int(ruid), 'euid': int(euid),
              'EXPECTED': ('Complete six-byte dummy replacement' if mode == 'dummy' else
                           'Only charlie UID digits become same-width zeroes'),
              'ACTUAL': 'exact-change' if exact else 'unchanged' if not changed else 'partial-or-unexpected-change',
              'EXPLANATION': 'Compared entire before/after byte sequences, hashes and root:root 0644 metadata.',
              'before_sha256': sha(before), 'after_sha256': sha(after),
              'file_length_unchanged': len(before) == len(after),
              'limit_seconds': limit, 'elapsed_integer_seconds': elapsed,
              'kernel_race_attempt_count': None,
              'program_has_only_expected_initialization_lines': healthy_output,
              'program_output': program, 'live_file_checked': False,
              'login_verified': False, 'baseline_details': details}
    if mode == 'dummy':
        result['actual_file_content'] = after.decode('ascii', 'replace')
    else:
        result['actual_charlie_records'] = [line.decode('ascii', 'replace') for line in after.splitlines()
                                             if line.startswith(b'charlie:')]
        result['EXPLANATION'] += ' A fresh non-sudo su/id session is still required for privilege proof.'
    if live:
        current = load(target)
        st = os.lstat(target)
        if not stat.S_ISREG(st.st_mode) or [st.st_uid, st.st_gid, stat.S_IMODE(st.st_mode)] != [0, 0, 0o644]:
            raise ValueError('Live target is not a root:root 0644 regular file')
        if os.access(target, os.W_OK) or current != after:
            raise ValueError('Live file is writable by caller or differs from the saved after-copy')
        result['live_file_checked'] = True
        result['live_sha256'] = sha(current)
    if not healthy_output:
        result['EXPLANATION'] += ' Additional/unexpected program output requires error review.'
    return result, 0 if exact and healthy_output else 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('dummy', 'passwd'))
    parser.add_argument('prefix', help='Path ending in the original unique trial label')
    parser.add_argument('--live', action='store_true', help='Guard and read the actual stopped SEED guest target')
    args = parser.parse_args()
    try:
        result, code = audit(args.mode, args.prefix, args.live)
        print(json.dumps(result, indent=2, sort_keys=True))
        return code
    except (IOError, OSError, ValueError, subprocess.CalledProcessError) as error:
        print('INCOMPLETE OR INVALID EVIDENCE: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
