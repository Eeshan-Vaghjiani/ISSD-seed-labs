#!/usr/bin/env python3
"""Display a compact, explicitly derived view of the actual retained run data."""
import json
from pathlib import Path

base = Path('/home/seed/issd-member5')
state = json.loads((base / 'automation/desktop-state.json').read_text())
logins = json.loads((Path(state['evidence']) / 'verified-logins.json').read_text())
results = [json.loads(path.read_text()) for path in (base / 'lab-files/logs').glob('*-result.json')]
print('SAVED TRIAL RESULTS — derived from actual logs')
print('Trial                 Attempts Mon(s)  Wall(s) Observation')
for result in sorted(results, key=lambda item: item['started']):
    label = result['label']
    name = label.removesuffix('-' + state['session']) if hasattr(str, 'removesuffix') else label[:-len(state['session'])-1]
    if logins.get(label, {}).get('verified'):
        observation = 'Record + su/id UID 0 verified'
    elif result['changed']:
        observation = 'Hash changed; inspect, no login claim'
    elif result['tmp_paths'].get('/tmp/XYZ', {}).get('uid') == 0:
        observation = 'Sticky-file failure; no target change'
    else:
        observation = 'No target change'
    print('{:<21} {:>8} {:>6} {:>8.3f} {}'.format(name, result['attempts'],
          result['monitor_elapsed_seconds'], result['runner_wall_seconds'], observation))
print('\nOld user log: last progress 76000 attempts / 227s; final totals unknown.')
print('Mon(s) uses integer SECONDS; Wall(s) includes monitor startup/exit.')
print('Defence controls: protected writes denied; permitted write succeeded.')
print('See raw summaries, control logs, actual su/id transcript and PNGs.')
