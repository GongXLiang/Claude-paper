"""Build the bilingual static pages from shared copy, template and icon catalogue."""
from pathlib import Path
import html,json,re
from datetime import datetime
ROOT=Path(__file__).resolve().parents[1]
copy=json.loads((ROOT/'scripts/site-copy.json').read_text(encoding='utf-8'))
template=(ROOT/'scripts/site-template.html').read_text(encoding='utf-8')
manifest=json.loads((ROOT/'orca-plugin.json').read_text(encoding='utf-8'))
catalogue=json.loads((ROOT/'icons/catalogue.json').read_text(encoding='utf-8'))
icons=json.loads((ROOT/'icons/theme.json').read_text())
assert copy['en'].keys()==copy['zh'].keys(),'Translation keys differ'
counts=dict(icon_count=len(catalogue),mapping_count=len(catalogue)+3,folder_count=1,folder_name_count=0,extension_count=len(icons["fileExtensions"]),filename_count=len(icons["fileNames"]))
PRIORITY='py ipynb c cpp f90 js ts jsx tsx md docx xlsx pptx pdf svg html dockerfile json toml yaml yml rs go java sh ps1 css vue csv parquet png zip'.split()
selected=[next(r for r in catalogue if r['kind']=='extension' and r['key']==k) for k in PRIORITY]
selected += [next(r for r in catalogue if r['kind']=='name' and r['key']==k) for k in ['.gitignore','package.json','.env','AGENTS.md'.lower()]]
def glyph(path):return (ROOT/path).read_text(encoding='utf-8').replace('<svg ','<svg aria-hidden="true" ',1).strip()
for lang,strings in copy.items():
    data={k:html.escape(v.format(**counts),quote=True) for k,v in strings.items() if isinstance(v,str)}
    data['version']=manifest['version']
    stats=json.loads((ROOT/'docs/install-stats.json').read_text(encoding='utf-8')) if (ROOT/'docs/install-stats.json').exists() else None
    count=str(stats['installs']) if stats else '';stamp=stats['generatedAt'] if stats else ''
    date=datetime.fromisoformat(stamp.replace('Z','+00:00')).date().isoformat() if stats else ''
    data['stats_html']='<p class="install-stats" data-install-stats'+('' if stats else ' hidden')+'><a href="https://onorca.dev/plugins/stats.json">'+data['installs_prefix']+'<span data-install-count>'+count+'</span>'+data['installs_unit']+'</a>'+data['installs_asof']+'<time datetime="'+html.escape(stamp,quote=True)+'">'+date+'</time></p>'
    tabs=[];links=[]
    for scene,(label,caption) in strings['scenes'].items():
        tabs.append(f'<button id="tab-{scene}" role="tab" aria-controls="scene-panel" aria-selected="{str(scene=="chat").lower()}" tabindex="{0 if scene=="chat" else -1}" data-scene="{scene}" data-large="true" data-file="{scene}" data-paired="false" data-caption="{html.escape(caption,quote=True)}">{html.escape(label)}</button>')
        links.append(f'<a href="assets/{scene}-light-large.png">{html.escape(label)} · {data["light"]}</a><a href="assets/{scene}-dark-large.png">{html.escape(label)} · {data["dark"]}</a>')
    data['tabs_html']='\n'.join(tabs);data['static_links_html']='\n'.join(links)
    data['chat_alt']=html.escape(strings['scenes']['chat'][1],quote=True)
    data['chat_caption']=html.escape(strings['light']+' · '+strings['scenes']['chat'][1])
    data['scope_rows_html']=''.join('<tr>'+''.join('<td>'+html.escape(v)+'</td>' for v in row)+'</tr>' for row in strings['scope_rows'])
    data['folder_summary_html']=''.join('<span>'+glyph('icons/'+name+'.svg')+data[label]+'</span>' for name,label in [('folder','folder_closed'),('folder-open','folder_open')])
    data['specimen_html']=''.join('<div class="specimen" title="'+html.escape(r['label'],quote=True)+'"><span class="actual16">'+glyph(r['path'])+'</span>'+glyph(r['path'])+'<code>'+html.escape(('.' if r['kind']=='extension' else '')+r['key'])+'</code></div>' for r in selected)
    keys=set(re.findall(r'\{\{(\w+)\}\}',template));assert keys<=data.keys(),keys-data.keys()
    result=re.sub(r'\{\{(\w+)\}\}',lambda m:data[m[1]],template)
    (ROOT/'docs'/strings['filename']).write_text(result,encoding='utf-8')
print(f'Built both languages: {len(copy["en"]["scenes"])} full-window scenes and {len(selected)} actual-size specimens')
