"""Create a clearly labelled presentation edit from native VM recordings.

HOST media processing only. Original WebM files remain byte-for-byte copies.
Sequential decoding avoids the old recorder's observed random-seek VP8 issue.
Title cards are ordinary presentation graphics, never terminal reconstructions.
"""
from pathlib import Path
import datetime as dt
import hashlib
import json
import shutil
import subprocess

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
FRESH = ROOT / 'evidence/incoming/opus-fresh-20261008'
OUT = ROOT / 'submission/video'
RANGES = (
    ('M6-task2-recorded-screen0.webm', 0.0, 22.0, '01-uid-overwrite.mp4'),
    ('M6-task2-login-screen0.webm', 268.0, 304.2, '02-login-proof.mp4'),
)
FONT_DIR = Path('/usr/share/fonts/liberation')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / 'TASK2_FALLBACK.mp4'
    manifest_path = OUT / 'VIDEO_MANIFEST.json'
    if target.exists():
        assert manifest_path.is_file(), 'Preserve an existing video without its manifest.'
        manifest = json.loads(manifest_path.read_text())
        assert manifest['output_sha256'] == sha(target), 'Preserve modified existing output.'
        assert manifest['ranges'] == [list(item) for item in RANGES], 'Existing edit uses different ranges.'
        for item in manifest['originals']:
            assert sha(FRESH / item['filename']) == item['sha256']
        print('Verified existing fallback; original edit preserved.')
        return

    actions = []
    def run(command):
        result = subprocess.run(command, text=True, capture_output=True)
        actions.append({'command': command, 'returncode': result.returncode,
                        'stdout': result.stdout, 'stderr': result.stderr})
        if result.returncode:
            diagnostic = OUT / ('failed-build-' + dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '.json')
            diagnostic.write_text(json.dumps(actions, indent=2) + '\n')
            result.check_returncode()
        return result

    encoding = ['-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16',
                '-pix_fmt', 'yuv420p', '-r', '15', '-movflags', '+faststart']
    original_dir = OUT / 'originals'
    segment_dir = OUT / 'segments'
    card_dir = OUT / 'title-cards'
    for directory in (original_dir, segment_dir, card_dir):
        directory.mkdir(exist_ok=True)
    originals = []
    for filename, start, end, output in RANGES:
        source = FRESH / filename
        destination = original_dir / filename
        if destination.exists():
            assert sha(source) == sha(destination)
        else:
            shutil.copy2(source, destination)
        originals.append({'filename': filename, 'sha256': sha(source), 'bytes': source.stat().st_size})
        # Output-side -ss: decode from the start instead of trusting seek indices.
        run(['ffmpeg', '-nostdin', '-v', 'error', '-i', str(source),
             '-ss', str(start), '-t', str(round(end - start, 3)),
             *encoding, '-n', str(segment_dir / output)])

    cards = (
        ('01-introduction', 'RECORDED EVIDENCE · 9 OCTOBER 2026',
         'Task 2: UID-field overwrite',
         ['Ordinary seed · one bounded trial in SEED12',
          'Native recording excerpt 1 of 2',
          '0–22 seconds of the original trial recording']),
        ('02-transition', 'LATER IN THE SAME EXPERIMENT',
         'Fresh non-sudo login proof',
         ['Excerpt begins after interactive authentication.',
          'The first failure and successful retry remain visible.',
          'Waiting omitted · original login recording 268–304.2 s']),
        ('03-restoration', 'VERIFIED AFTER THIS LOGIN',
         'Normal UID 1001 restored',
         ['The proof shell ended before full account restoration.',
          'A new ordinary login and complete cleanup passed.',
          'See genuine S11 / S13 images and the final export.']),
    )
    card_manifest = []
    regular = FONT_DIR / 'LiberationSans-Regular.ttf'
    bold = FONT_DIR / 'LiberationSans-Bold.ttf'
    for name, heading, title, body in cards:
        image = Image.new('RGB', (1280, 960), '#142A43')
        draw = ImageDraw.Draw(image)
        draw.rectangle((70, 120, 84, 824), fill='#087E8B')
        draw.text((124, 157), heading, font=ImageFont.truetype(str(bold), 26), fill='#86E0DA')
        draw.text((122, 300), title, font=ImageFont.truetype(str(bold), 49), fill='white')
        for index, text in enumerate(body):
            draw.text((126, 440 + index * 68), text,
                      font=ImageFont.truetype(str(regular), 28), fill='#DDE9F4')
        draw.text((126, 773), 'Member 6 — ISSD · Wenliang Du / SEED Labs attribution retained',
                  font=ImageFont.truetype(str(regular), 21), fill='#B8CEDF')
        path = card_dir / (name + '.png')
        image.save(path)
        card_manifest.append({'filename': path.name, 'sha256': sha(path),
                              'description': 'Presentation title card, not experimental terminal evidence'})
        run(['ffmpeg', '-nostdin', '-v', 'error', '-loop', '1', '-framerate', '15',
             '-i', str(path), '-t', '3', *encoding, '-n', str(segment_dir / (name + '.mp4'))])

    sequence = [
        '01-introduction.mp4', '01-uid-overwrite.mp4', '02-transition.mp4',
        '02-login-proof.mp4', '03-restoration.mp4',
    ]
    concat_file = segment_dir / 'sequence.ffconcat'
    concat_file.write_text('ffconcat version 1.0\n' + ''.join("file '" + name + "'\n" for name in sequence))
    run(['ffmpeg', '-nostdin', '-v', 'error', '-f', 'concat', '-safe', '0',
         '-i', str(concat_file), '-c', 'copy', '-movflags', '+faststart', '-n', str(target)])
    probe = run(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(target)])
    decode = run(['ffmpeg', '-nostdin', '-v', 'error', '-i', str(target), '-f', 'null', '-'])
    assert not decode.stderr, 'Inspect full-decode diagnostics before publishing.'
    manifest = {
        'built_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'source': 'Two unaltered native VirtualBox guest recordings; original hashes/copies retained',
        'ranges': RANGES, 'originals': originals, 'title_cards': card_manifest,
        'sequence': sequence, 'output': target.name, 'output_sha256': sha(target),
        'ffprobe': json.loads(probe.stdout), 'full_decode_passed': True, 'actions': actions,
        'qualifications': [
            'Edited recorded presentation fallback, not a continuous live classroom run.',
            'First excerpt is 0–22 s of trial recording. Second is 268–304.2 s of login recording.',
            'Authentication waiting before the second excerpt is omitted; initial failure remains visible.',
            'Second excerpt shows actual identity commands, proof shell exit and return to seed.',
            'Final title card summarizes separately evidenced S11/S13 restoration; it is not video of restoration.',
            'H.264 transcoding changes encoding; no terminal text is reconstructed or overlaid.',
        ],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    print('Fallback created:', target)
    print('Duration:', manifest['ffprobe']['format']['duration'], 'seconds; full decode passed.')


if __name__ == '__main__':
    main()
