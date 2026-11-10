"""Check companion color parity, fonts and malformed upstream statistics."""
from pathlib import Path
from datetime import datetime, timezone
import importlib.util, json, plistlib, tempfile, subprocess

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('stats', ROOT/'scripts/refresh-stats.py')
stats=importlib.util.module_from_spec(spec);spec.loader.exec_module(stats)
valid={'schemaVersion':1,'generatedAt':'2026-11-10T03:00:00Z','plugins':{stats.PLUGIN:{'installs':31}}}
now=datetime(2026,11,10,4,tzinfo=timezone.utc)
assert stats.snapshot(valid,now)['installs']==31
for count in (-1, True, '31', 2.5):
    bad=json.loads(json.dumps(valid));bad['plugins'][stats.PLUGIN]['installs']=count
    try:stats.snapshot(bad,now)
    except ValueError:pass
    else:raise AssertionError(f'accepted bad count {count!r}')
for stamp in ('bad-date','2026-11-15T00:00:00Z','2026-11-10T00:00:00'):
    bad=json.loads(json.dumps(valid));bad['generatedAt']=stamp
    try:stats.snapshot(bad,now)
    except ValueError:pass
    else:raise AssertionError('accepted invalid date')
for mode in ('light','dark'):
    theme=plistlib.loads((ROOT/f'extras/codex/claude-paper-{mode}.tmTheme').read_bytes())
    app=json.loads((ROOT/f'themes/{mode}.json').read_text(encoding='utf-8'))
    assert theme['settings'][0]['settings']['background']==app['tokens']['--editor-surface']
    for original, exported in zip(app['tokenColors'],theme['settings'][1:]):
        assert exported['settings']==original['settings']
manifest=json.loads((ROOT/'orca-plugin.json').read_text(encoding='utf-8'))
faces=manifest['contributes']['fonts'][0]['faces']
assert len(faces)==4
assert sum((ROOT/f['path']).stat().st_size for f in faces)<8*1024*1024
for face in faces:
    data=(ROOT/face['path']).read_bytes();assert data[:4]==b'wOF2' and len(data)<2*1024*1024
assert 'SIL OPEN FONT LICENSE' in (ROOT/'fonts/OFL.txt').read_text(encoding='utf-8')
with tempfile.TemporaryDirectory(prefix='claude-paper-installer-') as temp:
    destination=Path(temp)/'themes'
    base=['node',str(ROOT/'scripts/install-codex.mjs'),'--destination',str(destination)]
    subprocess.run(base+['--dry-run'],check=True,capture_output=True);assert not destination.exists()
    subprocess.run(base,check=True,capture_output=True)
    subprocess.run(base,check=True,capture_output=True)
    assert not (Path(temp)/'config.toml').exists()
    path=destination/'claude-paper-light.tmTheme';path.write_text('user custom content')
    assert subprocess.run(base,capture_output=True).returncode!=0
    assert path.read_text()=='user custom content'
print('Passed: companion palette parity, font signatures/license, invalid stats rejection, installer dry-run/idempotence/conflict preservation.')
