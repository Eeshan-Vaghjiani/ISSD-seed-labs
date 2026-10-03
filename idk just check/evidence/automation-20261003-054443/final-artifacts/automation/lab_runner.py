#!/usr/bin/env python3
"""Bounded, coordinated ordinary-user lab runs inside visible evidence terminals.

The supplied C binaries perform the experiment. This helper records commands,
waits for their real initialization output, stops a monitor if its attacker dies,
and terminates the attacker when a trial ends. It never calls sudo or su.
"""
import argparse
import ctypes
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import select
import shlex
import signal
import stat
import subprocess
import sys
import threading
import time

BASE = Path('/home/seed/issd-member5')
LAB = BASE / 'lab-files'
LOGS = LAB / 'logs'


def stamp():
    return dt.datetime.now().astimezone().isoformat()


def write_json(path, value):
    temporary = path.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(value, indent=2) + '\n')
    temporary.replace(path)


def fingerprint(pid):
    try:
        raw = Path('/proc/{}/stat'.format(pid)).read_text()
        fields = raw[raw.rfind(')') + 2:].split()
        if fields[0] == 'Z':
            return None
        return fields[19]  # Linux /proc stat field 22: process start ticks.
    except FileNotFoundError:
        return None


def alive(state):
    return state['start_ticks'] is not None and fingerprint(state['pid']) == state['start_ticks']


def stop_attacker(state):
    if alive(state):
        try:
            os.killpg(state['pid'], signal.SIGTERM)
        except ProcessLookupError:
            pass


def identity(out):
    out('+ id')
    out(subprocess.check_output(['id'], text=True).rstrip())
    out('+ pwd')
    out(str(Path.cwd()))


def logger(path):
    stream = path.open('x', buffering=1)
    def out(text):
        print(text, flush=True)
        stream.write(text + '\n')
    return stream, out


def read_output(process, out, callback=None):
    for line in process.stdout:
        text = line.rstrip('\n')
        out(text)
        if callback:
            callback(text)


def attack(program, limit, label):
    state_path = LOGS / (label + '-attacker-state.json')
    if state_path.exists():
        raise RuntimeError('Existing attacker label; refusing to overwrite')
    stream, out = logger(LOGS / (label + '-attacker.txt'))
    identity(out)
    out('Run: {} | attacker limit: {}s | {}'.format(label, limit, stamp()))
    out('+ ' + shlex.join([program]))
    process = subprocess.Popen([program], stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               text=True, bufsize=1, start_new_session=True)
    state = {'label': label, 'program': program, 'pid': process.pid,
             'start_ticks': fingerprint(process.pid), 'started': stamp(),
             'ruid': os.getuid(), 'euid': os.geteuid(), 'phase': 'starting',
             'limit_seconds': limit}
    write_json(state_path, state)
    expected = 'Atomic switching active' if program == './attack_atomic' else 'Naive switching active'
    def initialized(line):
        if expected in line:
            state['phase'] = 'ready'
            state['initialization_message'] = line
            state['ready_time'] = stamp()
            write_json(state_path, state)
    reader = threading.Thread(target=read_output, args=(process, out, initialized))
    reader.start()
    start = time.monotonic()
    reason = 'process exited or monitor requested stop'
    try:
        code = process.wait(timeout=limit)
    except (subprocess.TimeoutExpired, KeyboardInterrupt) as error:
        reason = 'attacker time limit' if isinstance(error, subprocess.TimeoutExpired) else 'operator interrupt'
        stop_attacker(state)
        code = process.wait(timeout=5)
    finally:
        if process.poll() is None:
            stop_attacker(state)
            process.wait(timeout=5)
        reader.join(timeout=5)
    state.update(phase='exited', returncode=code, ended=stamp(),
                 wall_seconds=round(time.monotonic() - start, 6), reason=reason)
    write_json(state_path, state)
    out('Attacker stopped: returncode={} wall={:.6f}s'.format(code, state['wall_seconds']))
    out('Reason: ' + reason)
    stream.close()


def monitor(victim, duration, label):
    attacker_path = LOGS / (label + '-attacker-state.json')
    attacker = json.loads(attacker_path.read_text())
    if attacker['phase'] != 'ready' or not alive(attacker):
        raise RuntimeError('Attacker has not initialized or has already exited')
    paths = ['/tmp/XYZ']
    if attacker['program'] == './attack_atomic':
        paths.append('/tmp/ABC')
    for name in paths:
        path = Path(name)
        deadline = time.monotonic() + 1
        initialized = False
        while time.monotonic() < deadline and alive(attacker):
            try:
                metadata = path.lstat()
                initialized = stat.S_ISLNK(metadata.st_mode) and metadata.st_uid == os.getuid()
                if initialized:
                    break
            except FileNotFoundError:
                pass  # The naive attack deliberately has a missing-path gap.
            time.sleep(0.001)
        if not initialized:
            raise RuntimeError(name + ' is not an initialized seed-owned symlink')
    clean = (BASE / 'passwd-before.sha256').read_text().split()[0]
    before = hashlib.sha256(Path('/etc/passwd').read_bytes()).hexdigest()
    if before != clean:
        raise RuntimeError('Password file does not match the recorded clean baseline')
    if any((LOGS / (label + suffix)).exists() for suffix in
           ('-summary.txt', '-last-output.txt', '-result.json', '-runner.txt')):
        raise RuntimeError('Existing trial label; refusing to overwrite')
    stream, out = logger(LOGS / (label + '-runner.txt'))
    identity(out)
    out('Initialization confirmed: pid={} {}'.format(attacker['pid'], attacker['initialization_message']))
    out('Seed-owned link(s) confirmed; clean baseline hash matches.')
    command = ['bash', 'run_trials.sh', victim, str(duration), label]
    out('+ ' + shlex.join(command))
    started = stamp()
    start = time.monotonic()
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               text=True, bufsize=1, start_new_session=True)
    write_json(LOGS / (label + '-monitor-state.json'),
               {'label': label, 'program': command, 'pid': process.pid,
                'start_ticks': fingerprint(process.pid), 'phase': 'running',
                'started': started, 'ruid': os.getuid(), 'euid': os.geteuid()})
    reader = threading.Thread(target=read_output, args=(process, out))
    reader.start()
    reason = 'monitor completed'
    try:
        while True:
            try:
                code = process.wait(timeout=0.05)
                break
            except subprocess.TimeoutExpired:
                if not alive(attacker):
                    reason = 'attacker exited; monitor stopped after in-flight attempt'
                    out('Attacker exited; stopping monitor and retaining the failure.')
                    process.send_signal(signal.SIGTERM)
                    code = process.wait(timeout=5)
                    break
                if time.monotonic() - start > duration + 10:
                    reason = 'outer watchdog deadline'
                    process.send_signal(signal.SIGTERM)
                    code = process.wait(timeout=5)
                    break
    except KeyboardInterrupt:
        reason = 'operator interrupt'
        process.send_signal(signal.SIGTERM)
        code = process.wait(timeout=5)
    finally:
        if process.poll() is None:
            process.send_signal(signal.SIGTERM)
            process.wait(timeout=5)
        stop_attacker(attacker)
        reader.join(timeout=5)
    wall = time.monotonic() - start
    # Wait for the actual attack process to be reaped before presenting results.
    deadline = time.monotonic() + 5
    while alive(attacker) and time.monotonic() < deadline:
        time.sleep(0.01)
    if alive(attacker):
        raise RuntimeError('Attacker has not stopped; do not reset')
    current = Path('/etc/passwd').read_bytes()
    after = hashlib.sha256(current).hexdigest()
    record = (LAB / 'input.txt').read_text().strip()
    records = [line for line in current.decode().splitlines() if line.startswith('test:')]
    summary = (LOGS / (label + '-summary.txt')).read_text()
    attempts = elapsed = None
    match = re.search(r'(?:CHANGE detected|INTERRUPTED) after (\d+) attempts and (\d+) seconds', summary)
    if match:
        attempts, elapsed = map(int, match.groups())
    else:
        match = re.search(r'NO CHANGE within (\d+)s; attempts=(\d+)', summary)
        if match:
            elapsed, attempts = map(int, match.groups())
    result = {'label': label, 'victim': victim, 'attacker': attacker['program'],
              'started': started, 'ended': stamp(), 'limit_seconds': duration,
              'attempts': attempts, 'monitor_elapsed_seconds': elapsed,
              'runner_wall_seconds': round(wall, 6), 'monitor_returncode': code,
              'stop_reason': reason, 'before_sha256': before, 'after_sha256': after,
              'changed': before != after, 'test_records': records,
              'exact_record_count': current.decode().splitlines().count(record),
              'runner_ruid': os.getuid(), 'runner_euid': os.geteuid(),
              'attacker_confirmed_stopped': True, 'login_verified': False}
    if before != after:
        (LOGS / (label + '-passwd-after.txt')).write_bytes(current)
    out('Monitor exited: {} | runner wall time: {:.6f}s'.format(code, wall))
    out('Attacker confirmed stopped. ' + reason)
    result['tmp_paths'] = {}
    for name in ('/tmp/XYZ', '/tmp/ABC'):
        path = Path(name)
        try:
            metadata = path.lstat()
        except FileNotFoundError:
            result['tmp_paths'][name] = {'type': 'absent'}
            continue
        kind = 'symlink' if stat.S_ISLNK(metadata.st_mode) else 'regular file' if stat.S_ISREG(metadata.st_mode) else 'other'
        item = {'type': kind, 'uid': metadata.st_uid, 'gid': metadata.st_gid,
                'mode': oct(stat.S_IMODE(metadata.st_mode)), 'inode': metadata.st_ino,
                'size': metadata.st_size}
        if kind == 'symlink':
            item['target'] = os.readlink(path)
        elif kind == 'regular file':
            content = path.read_bytes()
            snapshot = LOGS / (label + '-' + path.name + '-content.bin')
            snapshot.write_bytes(content)
            item['content_sha256'] = hashlib.sha256(content).hexdigest()
            item['saved_content'] = str(snapshot)
        result['tmp_paths'][name] = item
        out('{}: {} uid={} mode={}'.format(name, kind, metadata.st_uid, item['mode']))
    if before != after:
        out('Hash change is a signal to inspect; verify the complete record and non-sudo su login.')
    else:
        out('Password-file SHA-256 is unchanged.')
    write_json(LOGS / (label + '-result.json'), result)
    stream.close()


def wait_for(label, stage):
    # Wait on filesystem events, with a bound, rather than repeatedly launching
    # process checks from the control window.
    libc = ctypes.CDLL(None, use_errno=True)
    fd = libc.inotify_init1(os.O_CLOEXEC | os.O_NONBLOCK)
    if fd < 0:
        raise OSError(ctypes.get_errno(), 'inotify_init1')
    libc.inotify_add_watch(fd, os.fsencode(LOGS), 0x00000008 | 0x00000080)
    suffix = '-attacker-state.json' if stage == 'ready' else '-result.json'
    path = LOGS / (label + suffix)
    deadline = time.monotonic() + (15 if stage == 'ready' else 340)
    try:
        while True:
            if path.exists():
                state = json.loads(path.read_text())
                if stage == 'done' or state.get('phase') in ('ready', 'exited'):
                    print(json.dumps(state, indent=2))
                    if stage == 'ready' and state['phase'] != 'ready':
                        raise RuntimeError('Attacker exited before victim startup')
                    return
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError('Bounded wait expired for ' + str(path))
            ready, _, _ = select.select([fd], [], [], remaining)
            if ready:
                os.read(fd, 65536)
    finally:
        os.close(fd)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    for action in ('attack', 'monitor'):
        p = sub.add_parser(action)
        p.add_argument('program', choices=('./attack_naive', './attack_atomic') if action == 'attack'
                       else ('./vulp', './vulp_least'))
        p.add_argument('duration', type=int)
        p.add_argument('label')
    p = sub.add_parser('wait')
    p.add_argument('label')
    p.add_argument('stage', choices=('ready', 'done'))
    args = parser.parse_args()
    if os.getuid() != 1000 or os.geteuid() != 1000:
        raise RuntimeError('Run as ordinary seed, never through sudo')
    if not re.fullmatch(r'[A-Za-z0-9_-]+', args.label):
        raise ValueError('Invalid log label')
    os.chdir(LAB)
    if args.action == 'wait':
        wait_for(args.label, args.stage)
    else:
        if not 1 <= args.duration <= 330:
            raise ValueError('Duration must be between 1 and 330 seconds')
        if args.action == 'attack':
            attack(args.program, args.duration, args.label)
        else:
            monitor(args.program, args.duration, args.label)


if __name__ == '__main__':
    main()
