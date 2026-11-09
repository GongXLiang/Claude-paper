"""Build the two static pages from one template and checked-in translations."""
from pathlib import Path
import html,json,re
ROOT=Path(__file__).resolve().parents[1]
copy=json.loads((ROOT/'scripts/site-copy.json').read_text(encoding='utf-8'))
template=(ROOT/'scripts/site-template.html').read_text(encoding='utf-8')
manifest=json.loads((ROOT/'orca-plugin.json').read_text(encoding='utf-8'))
folders=json.loads((ROOT/'icons/folders.json').read_text(encoding='utf-8'))
icons=json.loads((ROOT/'icons/theme.json').read_text())
assert copy['en'].keys()==copy['zh'].keys(), 'Translation keys differ'
counts=dict(icon_count=len(list((ROOT/'icons').glob('*.svg'))),mapping_count=sum(len(v) for v in icons.values() if isinstance(v,dict)),folder_count=len(folders),folder_name_count=len(icons['folderNames']))
def glyph(role):
    name='folder' if role=='fallback' else 'folder-'+role
    return (ROOT/f'icons/{name}.svg').read_text().replace('<svg ','<svg aria-hidden="true" width="24" height="24" ',1).strip()
for lang,strings in copy.items():
    data={k:html.escape(v.format(**counts),quote=True) for k,v in strings.items() if isinstance(v,str)}
    data['version']=manifest['version']
    data['icons_asset']='icons.png' if lang=='en' else 'icons-zh.png'
    tabs=[];links=[]
    for scene,(label,caption) in strings['scenes'].items():
        file='cli-compare' if scene=='cli' else scene
        if scene=='icons':file='icons' if lang=='en' else 'icons-zh'
        paired=scene in ('icons','cli')
        tabs.append(f'<button id="tab-{scene}" role="tab" aria-controls="scene-panel" aria-selected="{str(scene=="chat").lower()}" tabindex="{0 if scene=="chat" else -1}" data-scene="{scene}" data-file="{file}" data-paired="{str(paired).lower()}" data-caption="{html.escape(caption,quote=True)}">{html.escape(label)}</button>')
        links.append(f'<a href="assets/{file}{"" if paired else "-dark"}.png">{html.escape(label)}</a>')
    data['tabs_html']='\n'.join(tabs);data['static_links_html']=' · '.join(links)
    for scene in ('chat','diff','icons','terminal'):data[scene+'_alt']=html.escape(strings['scenes'][scene][1],quote=True)
    data['chat_caption']=html.escape(strings['light']+' · '+strings['scenes']['chat'][1])
    data['scope_rows_html']=''.join('<tr>'+''.join('<td>'+html.escape(v)+'</td>' for v in row)+'</tr>' for row in strings['scope_rows'])
    data['folder_rows_html']=''.join('<tr><th scope="row"><span class="folder-category">'+glyph(role)+'<span>'+html.escape(group[lang])+'</span></span></th><td>'+', '.join('<code>'+html.escape(n)+'</code>' for n in group['names'])+'</td></tr>' for role,group in folders.items())
    data['folder_summary_html']=''.join('<span>'+glyph(role)+html.escape(folders[role][lang] if role!='fallback' else strings['fallback'])+'</span>' for role in ('src','data','plugins','output','fallback'))
    keys=set(re.findall(r'\{\{(\w+)\}\}',template));assert keys<=data.keys(), keys-data.keys()
    result=re.sub(r'\{\{(\w+)\}\}',lambda m:data[m[1]],template)
    (ROOT/'docs'/strings['filename']).write_text(result,encoding='utf-8')
print('Built English and Chinese static pages; translations and folder counts agree.')
