#!/usr/bin/env python3
"""Inventory every tracked repository file and check retained artifact consistency.

Only syntax/format/hash checks are performed; no lab program or VM is executed.
Requires the host's Pillow and pdftotext. JSON output is an audit, not VM evidence.
"""
from pathlib import Path
import argparse
import ast
import collections
import datetime as dt
import hashlib
import json
import re
import subprocess
import tarfile
import xml.etree.ElementTree as ET
import zipfile

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='New JSON record; refuses overwrites')
    args = parser.parse_args()
    names = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    paths = [ROOT / name for name in names if name]
    result = {'scope': 'Repository static/integrity audit; not new VM execution',
              'recorded_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
              'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
              'files': [], 'checks': [], 'errors': [], 'counts_by_area': {}}
    counts = collections.Counter()
    checked_contents = set()
    for path in paths:
        relative = path.relative_to(ROOT)
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        counts[relative.parts[0]] += 1
        result['files'].append({'path': relative.as_posix(), 'bytes': len(data),
                                'mode': oct(path.stat().st_mode & 0o7777), 'sha256': digest})
        # Duplicate export/selected files are all hashed, but format-checked once.
        if digest in checked_contents:
            continue
        checked_contents.add(digest)
        try:
            if path.suffix == '.png':
                with Image.open(path) as image:
                    image.verify()
            elif path.suffix in ('.docx', '.pptx'):
                with zipfile.ZipFile(path) as archive:
                    if archive.testzip() is not None:
                        raise ValueError('Office ZIP CRC failure')
                    for name in archive.namelist():
                        if name.endswith('.xml'):
                            ET.fromstring(archive.read(name))
            elif path.suffix == '.pdf':
                text = subprocess.check_output(['pdftotext', '-layout', str(path), '-'], stderr=subprocess.PIPE)
                if not text.strip():
                    raise ValueError('No extractable PDF text')
            elif path.suffix == '.py':
                ast.parse(data.decode('utf-8'), filename=str(relative))
            elif path.suffix in ('.sh', '.bash'):
                subprocess.run(['bash', '-n', str(path)], capture_output=True, check=True)
            elif path.suffix == '.json':
                json.loads(data)
            elif path.suffix == '.jsonl':
                for line in data.splitlines():
                    if line.strip():
                        json.loads(line)
            elif path.name.endswith('.tar.gz'):
                # Read members without extracting or executing any archived file.
                with tarfile.open(path, 'r:gz') as archive:
                    for member in archive:
                        if member.isfile():
                            stream = archive.extractfile(member)
                            while stream.read(1024 * 1024):
                                pass
            else:
                # Read the entire tracked text/binary payload for the inventory hash.
                pass
        except (OSError, ValueError, SyntaxError, subprocess.CalledProcessError,
                zipfile.BadZipFile, tarfile.TarError, ET.ParseError) as error:
            result['errors'].append({'path': relative.as_posix(), 'error': str(error)})
    result['counts_by_area'] = dict(counts)
    result['unique_file_contents'] = len(checked_contents)
    result['checks'].append('Every tracked file read and SHA-256 inventoried; unique formats/syntax checked.')

    out = ROOT / 'Member5/submission'
    selected = json.loads((out / 'evidence/SELECTION.json').read_text())
    try:
        for item in selected:
            for path in (out / 'evidence' / item['selected'],
                         ROOT / 'Member5/evidence' / item['selected'],
                         ROOT / 'idk just check/evidence' / item['original']):
                if sha(path) != item['sha256']:
                    raise ValueError('Selected original hash mismatch: ' + str(path))
        result['checks'].append('%d Member 5 selected images match both folders and retained raw captures.' % len(selected))
        crops = json.loads((out / 'figures/CROP_MANIFEST.json').read_text())
        for item in crops:
            original = out / 'evidence' / item['original']
            figure = out / 'figures' / item['figure']
            if sha(original) != item['original_sha256'] or sha(figure) != item['figure_sha256']:
                raise ValueError('Crop hash mismatch: ' + str(figure))
            with Image.open(original) as image, Image.open(figure) as actual:
                expected = image.crop(item['crop_box_xyxy'])
                if expected.size != actual.size or ImageChops.difference(
                        expected.convert('RGB'), actual.convert('RGB')).getbbox() is not None:
                    raise ValueError('Crop pixels mismatch: ' + str(figure))
        result['checks'].append('%d Member 5 derivatives match the recorded original crop pixels.' % len(crops))
        trials = sorted((out / 'logs').glob('*-result.json'))
        for path in trials:
            trial = json.loads(path.read_text())
            summary = (out / 'logs' / (trial['label'] + '-summary.txt')).read_text()
            if trial['changed']:
                expected = 'CHANGE detected after %s attempts and %s seconds' % (
                    trial['attempts'], trial['monitor_elapsed_seconds'])
                valid = (expected in summary and trial['exact_record_count'] == 1 and
                         trial['before_sha256'] != trial['after_sha256'])
            else:
                valid = (trial['before_sha256'] == trial['after_sha256'] and
                         ('attempts=%s' % trial['attempts'] in summary or
                          'INTERRUPTED after %s attempts' % trial['attempts'] in summary))
            if not valid or trial['runner_ruid'] != 1000 or trial['runner_euid'] != 1000 or not trial['attacker_confirmed_stopped']:
                raise ValueError('Trial/summary mismatch: ' + str(path))
        result['checks'].append('%d Member 5 trial JSON records agree with their summaries/identities/hashes.' % len(trials))
    except (OSError, ValueError, KeyError) as error:
        result['errors'].append({'path': 'Member5/submission', 'error': str(error)})

    print(result['scope'])
    print('Commit:', result['commit'])
    print('Tracked files:', len(paths), '| Unique payloads:', len(checked_contents))
    print('Areas:', dict(counts))
    for check in result['checks']:
        print('PASS:', check)
    for error in result['errors']:
        print('ERROR:', error)
    print('Integrity errors:', len(result['errors']))
    print('Semantic screenshot review is separate; hash agreement alone does not prove execution.')
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x') as stream:
            json.dump(result, stream, indent=2)
            stream.write('\n')
        print('Saved:', args.output)
    return 1 if result['errors'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
