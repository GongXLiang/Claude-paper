"""Refresh a small, dated snapshot of Orca's public install statistics."""
from datetime import datetime, timezone, timedelta
from pathlib import Path
import json, urllib.request

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'https://onorca.dev/plugins/stats.json'
PLUGIN = 'gongxliang.claude-paper'

def snapshot(data, now=None):
    now = now or datetime.now(timezone.utc)
    if data.get('schemaVersion') != 1:
        raise ValueError('Unsupported official statistics schema')
    stamp = data['generatedAt']
    date = datetime.fromisoformat(stamp.replace('Z', '+00:00'))
    count = data['plugins'][PLUGIN]['installs']
    if date.tzinfo is None or date > now + timedelta(days=1) or type(count) is not int or count < 0:
        raise ValueError('Invalid official statistics')
    return dict(schemaVersion=1, plugin=PLUGIN, installs=count, generatedAt=stamp, source=SOURCE)

def main():
    path = ROOT / 'docs/install-stats.json'
    try:
        request = urllib.request.Request(SOURCE, headers={'User-Agent':'Claude-Paper-stats/1.0'})
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read(2 * 1024 * 1024 + 1)
        if len(raw) > 2 * 1024 * 1024:
            raise ValueError('Official statistics exceed size limit')
        data = snapshot(json.loads(raw))
        if path.exists():
            previous = json.loads(path.read_text(encoding='utf-8'))
            old = datetime.fromisoformat(previous['generatedAt'].replace('Z', '+00:00'))
            new = datetime.fromisoformat(data['generatedAt'].replace('Z', '+00:00'))
            if new < old:
                raise ValueError('Ignoring an older upstream snapshot')
        temporary = path.with_suffix('.json.tmp')
        temporary.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
        temporary.replace(path)
        print(f"{data['installs']} community installs; statistics generated {data['generatedAt']}")
    except Exception as error:
        if not path.exists():
            raise
        print(f'::warning::Install statistics refresh failed; keeping dated snapshot: {error}')

if __name__ == '__main__':
    main()
