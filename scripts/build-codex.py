"""Export the app's existing syntax palette as two optional Codex CLI themes."""
from pathlib import Path
import json, plistlib

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'extras' / 'codex'
DEST.mkdir(parents=True, exist_ok=True)
for mode, name in [('light', 'Warm Paper'), ('dark', 'Warm Night')]:
    app = json.loads((ROOT / f'themes/{mode}.json').read_text(encoding='utf-8'))
    tokens = app['tokens']
    settings = [{'settings': {
        'background': tokens['--editor-surface'], 'foreground': tokens['--foreground'],
        'caret': tokens['--ring'], 'selection': tokens['--chat-selection'],
        'lineHighlight': tokens['--chat-code-block'],
    }}]
    for rule in app['tokenColors']:
        scope = rule['scope']
        settings.append({'scope': ', '.join(scope) if isinstance(scope, list) else scope,
                         'settings': rule['settings']})
    # Make the intended added/removed syntax hues explicit for Syntect consumers.
    settings.extend([{'scope': scope, 'settings': {'foreground': tokens[token]}}
                     for scope, token in [('markup.inserted', '--diff-added'), ('markup.deleted', '--diff-removed')]])
    theme = {'name': f'Claude Paper · {name}', 'author': 'GongXLiang', 'settings': settings}
    path = DEST / f'claude-paper-{mode}.tmTheme'
    path.write_bytes(plistlib.dumps(theme, sort_keys=False))
    assert plistlib.loads(path.read_bytes()) == theme
    print(path.name)
