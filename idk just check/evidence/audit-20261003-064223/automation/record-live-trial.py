#!/usr/bin/env python3
"""Record original full-desktop PNG frames while a real bounded trial starts.

GStreamer's native X11 source avoids launching a screenshot process for every
frame. It does not pause either experiment process or alter the victim.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gst, GLib

import desktop
import lab_runner


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('label')
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    if os.getuid() != 1000 or os.geteuid() != 1000:
        raise RuntimeError('Run the recorder as seed')
    label = args.label
    if any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in label):
        raise ValueError('Invalid label')
    args.directory.mkdir(parents=True, exist_ok=False)
    Gst.init(None)
    desktop.layout()
    pipeline_text = ('ximagesrc name=screen display-name=:0 use-damage=true '
                     'show-pointer=false do-timestamp=true ! '
                     'video/x-raw,framerate=30/1 ! videoconvert ! '
                     'video/x-raw,format=RGB ! queue max-size-buffers=3 '
                     'max-size-bytes=0 max-size-time=0 ! '
                     'pngenc name=encoder compression-level=1 ! '
                     'multifilesink name=files post-messages=true sync=false '
                     'location="' + str(args.directory / 'frame-%05d.png') + '"')
    pipeline = Gst.parse_launch(pipeline_text)
    loop = GLib.MainLoop()
    metadata = {}
    frames = []
    error = []
    started = dt.datetime.now().astimezone().isoformat()
    start_monotonic = time.monotonic()
    sender = None

    def states():
        result = {}
        for kind in ('attacker', 'monitor'):
            path = lab_runner.LOGS / (label + '-' + kind + '-state.json')
            if path.exists():
                state = json.loads(path.read_text())
                result[kind] = {'pid': state['pid'], 'start_ticks': state['start_ticks'],
                                'live': lab_runner.alive(state), 'program': state['program'],
                                'ruid': state['ruid'], 'euid': state['euid']}
        return result

    def raw_frame(pad, info):
        buffer = info.get_buffer()
        metadata[int(buffer.pts)] = {'pts_ns': int(buffer.pts),
                                    'sampled_at': dt.datetime.now().astimezone().isoformat(),
                                    'raw_processes': states()}
        return Gst.PadProbeReturn.OK

    pipeline.get_by_name('encoder').get_static_pad('sink').add_probe(
        Gst.PadProbeType.BUFFER, raw_frame)

    def message(bus, msg):
        if msg.type == Gst.MessageType.ELEMENT:
            structure = msg.get_structure()
            if structure and structure.get_name() == 'GstMultiFileSink':
                pts = int(structure.get_value('timestamp'))
                item = metadata.pop(pts, {'pts_ns': pts, 'raw_processes': {}})
                item.update(filename=structure.get_value('filename'),
                            index=structure.get_value('index'), written_processes=states(),
                            written_at=dt.datetime.now().astimezone().isoformat())
                item['both_live_raw_and_written'] = all(
                    item[field].get(kind, {}).get('live', False)
                    for field in ('raw_processes', 'written_processes')
                    for kind in ('attacker', 'monitor'))
                frames.append(item)
        elif msg.type == Gst.MessageType.ERROR:
            problem, debug = msg.parse_error()
            error.append(str(problem) + ': ' + str(debug))
            loop.quit()
        elif msg.type == Gst.MessageType.EOS:
            loop.quit()

    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect('message', message)

    def launch_victim():
        nonlocal sender
        command = 'python3 ../automation/lab_runner.py monitor ./vulp 300 ' + label
        sender = subprocess.Popen(['python3', str(desktop.HERE / 'desktop.py'),
                                   'send', 'B', command])
        return GLib.SOURCE_REMOVE

    def finish_recording():
        pipeline.send_event(Gst.Event.new_eos())
        return GLib.SOURCE_REMOVE

    def watchdog():
        error.append('Recorder outer deadline reached')
        loop.quit()
        return GLib.SOURCE_REMOVE

    pipeline.set_state(Gst.State.PLAYING)
    GLib.timeout_add(1200, launch_victim)
    GLib.timeout_add_seconds(10, finish_recording)
    GLib.timeout_add_seconds(20, watchdog)
    try:
        loop.run()
    finally:
        pipeline.set_state(Gst.State.NULL)
        if sender:
            sender.wait(timeout=5)
    for item in frames:
        item['sha256'] = hashlib.sha256(Path(item['filename']).read_bytes()).hexdigest()
    data = {'label': label, 'method': 'native GStreamer full-desktop PNG sequence',
            'pipeline': pipeline_text, 'started': started,
            'wall_seconds': time.monotonic() - start_monotonic,
            'requested_fps': 30, 'frames': frames, 'errors': error}
    (args.directory / 'recording.json').write_text(json.dumps(data, indent=2) + '\n')
    candidates = [item for item in frames if item['both_live_raw_and_written']]
    print('Original frames:', len(frames), '| both-live candidates:', len(candidates))
    for item in candidates:
        print(item['index'], item['filename'], 'PTS', round(item['pts_ns'] / 1e9, 6))
    if error:
        raise RuntimeError('; '.join(error))


if __name__ == '__main__':
    main()
