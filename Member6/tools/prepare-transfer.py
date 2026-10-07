#!/usr/bin/env python3
"""HOST ACTION: prepare an offline data CD from this Member 6 pack and references.

Copies the two previously downloaded official references, hashes the actual
input files, and uses bsdtar's ISO writer. Does not execute/compile lab code.
"""
from pathlib import Path
import argparse
import datetime as dt
import hashlib
import json
import shlex
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def digest(path, algorithm='sha256'):
    value = hashlib.new(algorithm)
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--references', type=Path, default=Path('/tmp/opencode/member6-reference'))
    parser.add_argument('--label', default='20261007', help='Fresh media label; never overwrites an existing ISO')
    args = parser.parse_args()
    if not args.label or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in args.label):
        parser.error('Invalid label')
    media = Path.home() / 'VirtualBox VMs/ISSD-Member6-media'
    iso = media / ('M6-transfer-' + args.label + '.iso')
    record_path = ROOT / 'evidence/host' / ('transfer-' + args.label + '.json')
    if iso.exists() or record_path.exists():
        parser.error('Existing media/record; preserve it and use a fresh label')
    archive = Path.home() / 'Downloads/SEEDUbuntu12.04.zip'
    md5 = digest(archive, 'md5')
    if md5 != '6ec9c429a2f4a9163530ada20f0621dc':
        raise ValueError('Official SEED archive MD5 mismatch')
    archive_record = {'path': str(archive), 'bytes': archive.stat().st_size,
                      'md5': md5, 'sha256': digest(archive),
                      'official_page': 'https://seedsecuritylabs.org/labsetup.html',
                      'official_link': 'https://seed.nyc3.cdn.digitaloceanspaces.com/SEEDUbuntu12.04.zip',
                      'local_archive_reused': True}
    with zipfile.ZipFile(archive) as source:
        bad = source.testzip()
        if bad:
            raise ValueError('ZIP CRC failure: ' + bad)
        archive_record['zip_crc_all_entries_passed'] = True
        archive_record['entries'] = [{'path': i.filename, 'bytes': i.file_size, 'crc32': '%08x' % i.CRC}
                                     for i in source.infolist()]
    references = ROOT / 'reference'
    references.mkdir(exist_ok=True)
    for name in ('Dirty_COW.pdf', 'Labsetup.zip'):
        source, destination = args.references / name, references / name
        if destination.exists():
            if digest(source) != digest(destination):
                raise ValueError('Existing different reference: ' + str(destination))
        else:
            shutil.copy2(source, destination)
    if not (references / 'Dirty_COW.pdf').read_bytes().startswith(b'%PDF-'):
        raise ValueError('Reference download is not a PDF')
    with zipfile.ZipFile(references / 'Labsetup.zip') as source:
        if source.testzip() is not None or not any(n.endswith('cow_attack.c') for n in source.namelist()):
            raise ValueError('Invalid official source ZIP')
    include = ['lab-files', 'automation', 'reference', 'VM_SESSION_GUIDE.md',
               'README.md', 'START_TO_FINISH_GUIDE.md', 'ARCH_HOST_SETUP.md',
               'evidence/SCREENSHOT_CHECKLIST.md', 'evidence/CAPTURE_PLAN.md']
    files = []
    for name in include:
        path = ROOT / name
        files.extend(sorted(p for p in path.rglob('*') if p.is_file()) if path.is_dir() else [path])
    # The transfer bundle is source-only. A later guest build belongs in the guest.
    for path in files:
        if path.name in ('cow_attack', 'cow_control') or path.suffix == '.pyc':
            raise ValueError('Unexpected generated executable/cache in input bundle: ' + str(path))
    inputs = [{'path': p.relative_to(ROOT).as_posix(), 'bytes': p.stat().st_size, 'sha256': digest(p)} for p in files]
    command = ['bsdtar', '--format=iso9660', '--options=iso9660:volume-id=M6PACK',
               '-cf', str(iso), '-C', str(ROOT)] + include
    print('HOST ACTION: ' + shlex.join(command), flush=True)
    subprocess.run(command, check=True)
    listing = subprocess.check_output(['bsdtar', '-tf', str(iso)], text=True)
    for item in inputs:
        data = subprocess.check_output(['bsdtar', '-xOf', str(iso), item['path']])
        if hashlib.sha256(data).hexdigest() != item['sha256']:
            raise ValueError('ISO content mismatch: ' + item['path'])
    record = {'scope': 'HOST media/transfer provenance; no guest execution',
              'recorded_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
              'official_vm_archive': archive_record, 'iso': str(iso),
              'iso_bytes': iso.stat().st_size, 'iso_sha256': digest(iso),
              'command': command, 'inputs': inputs, 'iso_listing': listing,
              'every_iso_input_hash_verified': True}
    record_path.parent.mkdir(parents=True, exist_ok=True)
    with record_path.open('x') as stream:
        json.dump(record, stream, indent=2)
        stream.write('\n')
    print('Prepared data CD:', iso)
    print('Every input verified against ISO bytes; record:', record_path)


if __name__ == '__main__':
    main()
