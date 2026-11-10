"""Check shipped theme contrast and the safety/completeness of icon assets."""
from pathlib import Path
import json,re,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
def lum(value):
    rgb=[int(value[i:i+2],16)/255 for i in (1,3,5)]
    return sum(w*(c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4) for c,w in zip(rgb,(.2126,.7152,.0722)))
def contrast(a,b):
    a,b=sorted((lum(a),lum(b)));return (b+.05)/(a+.05)
for mode in ('light','dark'):
    theme=json.loads((ROOT/f'themes/{mode}.json').read_text(encoding='utf-8'))
    t=theme['tokens'];assert len(t)==73
    chat='#F9F8F5' if mode=='light' else '#2A2927'
    pairs=[(t['--chat-bold-foreground'],b) for b in (chat,t['--chat-user-message'],t['--chat-code-block'])]
    pairs += [(t['--chat-muted-foreground'],b) for b in (chat,t['--chat-code-block'],t['--chat-inline-code'])]
    pairs += [(t['--chat-inline-code-foreground'],t['--chat-inline-code']),(t['--text-link'],t['--chat-inline-code']),(t['--chat-selection-foreground'],t['--chat-selection'])]
    terminal=json.loads((ROOT/f'themes/terminal-{mode}.json').read_text())['terminal']
    pairs += [(terminal['cursorAccent'],terminal['cursor'])]
    for fg,bg in pairs: assert contrast(fg,bg)>=4.5,(mode,fg,bg,contrast(fg,bg))
    print(mode,'chat/cursor minimum contrast',round(min(contrast(*p) for p in pairs),2))
icons=json.loads((ROOT/'icons/theme.json').read_text())
catalogue=json.loads((ROOT/'icons/catalogue.json').read_text())
maps=[icons[k] for k in ('icons','fileNames','fileExtensions','folderNames','folderNamesExpanded')]
assert sum(map(len,maps))<=512
assert icons['folderNames']==icons['folderNamesExpanded']=={},'Every folder must use the same neutral fallback'
paths=[]
for mapping in maps:
    assert len({k.lower() for k in mapping})==len(mapping)
    for value in mapping.values():
        assert value.startswith('icons/') and '..' not in value
        paths.append(value)
assert len(paths)==len(set(paths)), 'Each mapping requires a distinct asset'
assert len(catalogue)==len(icons['fileNames'])+len(icons['fileExtensions'])
shape_signatures=set()
for value in paths:
    data=(ROOT/value).read_text();assert len(data.encode())<=65536
    doc=ET.fromstring(data);assert doc.attrib['viewBox']=='0 0 16 16'
    for el in doc.iter():
        assert el.tag.split('}')[-1] in ('svg','path','rect','circle')
        assert not any(k.lower().startswith('on') or k in ('href','style','transform','filter') for k in el.attrib)
    assert not re.search(r'url\(|https?://(?!www.w3.org/2000/svg)',data)
    signature=re.sub(r'#[a-fA-F0-9]{6}','COLOR',data)
    assert signature not in shape_signatures, ('Only color distinguishes this asset',value)
    shape_signatures.add(signature)
for row in catalogue:
    mapping=icons['fileNames' if row['kind']=='name' else 'fileExtensions']
    assert mapping[row['key']]==row['path']
    assert row['label'] and row['category'] and row['shape']
for key in ('d.ts','test.ts','config.ts'):assert icons['fileExtensions'][key]!=icons['fileExtensions']['ts']
for key in ('py','ipynb','cpp','f90','js','json','yaml','yml','toml','docx','xlsx','pptx','md','nix','proto','tf'):
    assert key in icons['fileExtensions'],key
for key in ('.gitignore','.env','package.json','cargo.lock','uv.lock'):
    assert key in icons['fileNames'],key
backgrounds=['#F3F2EF','#E6E5E0','#E1E0DA','#F9F8F5','#201F1D','#31302D','#363532','#2A2927']
colors=['#817E77','#6D8190','#4D83B5','#6083A0','#2E88A7','#A97416','#578B46','#3C8B87','#996FA9','#C6605D','#C26540','#7F8332','#A07650','#BE5F8F','#7677C4']
minimum=min(contrast(c,b) for c in colors for b in backgrounds)
assert minimum>=3,(minimum)
print(len(paths),'active SVGs,',sum(map(len,maps)),'mappings; unique geometry, catalogue, neutral folders and SVG safety checked; minimum icon contrast',round(minimum,2))
