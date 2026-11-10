"""Render a bilingual specimen sheet from the shipped SVGs; not an app screenshot."""
from pathlib import Path
from html import escape
import json
ROOT=Path(__file__).resolve().parents[1]
rows=json.loads((ROOT/'icons/catalogue.json').read_text(encoding='utf-8'))
keys='py ipynb c cpp f90 js ts jsx tsx md docx xlsx pptx pdf svg html dockerfile json toml yaml yml rs go java sh ps1 css vue csv parquet png zip'.split()
selected=[next(r for r in rows if r['kind']=='extension' and r['key']==k) for k in keys]
selected += [next(r for r in rows if r['kind']=='name' and r['key']==k) for k in ['.gitignore','package.json','.env','agents.md']]
for lang in ['en','zh']:
    p=['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000" viewBox="0 0 1600 1000"><rect width="1600" height="1000" fill="#F3F2EF"/>']
    def text(x,y,t,c='#262522',size=18):p.append(f'<text x="{x}" y="{y}" fill="{c}" font-family="Segoe UI,Microsoft YaHei,sans-serif" font-size="{size}">{escape(t)}</text>')
    def glyph(file,x,y):p.append((ROOT/file).read_text().replace('<svg ',f'<svg x="{x}" y="{y}" width="32" height="32" ',1))
    text(48,66,'Paper Fold 2',size=38)
    text(48,104,'One folder. Distinct files. 455 original SVGs.' if lang=='en' else '一种文件夹，鲜明的文件类型。455 枚原创 SVG。',size=20)
    for x,bg,fg,muted,title in [(32,'#F9F8F5','#262522','#6B6962','Warm Paper' if lang=='en' else '暖纸'),(816,'#2A2927','#EBE9E2','#B1ADA5','Warm Night' if lang=='en' else '暖夜')]:
        p.append(f'<rect x="{x}" y="135" width="752" height="812" rx="12" fill="{bg}"/>')
        text(x+30,177,title,fg,23)
        glyph('icons/folder.svg',x+30,198);glyph('icons/folder-open.svg',x+76,198)
        text(x+126,221,'All folder names / closed & open' if lang=='en' else '所有文件夹名称 / 折叠与展开',muted,16)
        for i,r in enumerate(selected):
            cx=x+30+(i%3)*238;cy=258+(i//3)*54
            glyph(r['path'],cx,cy)
            text(cx+43,cy+22,('.' if r['kind']=='extension' else '')+r['key'],fg,17)
        text(x+30,926,'Original icons at 2×; selected examples.' if lang=='en' else '原始图标放大 2 倍；精选示例。',muted,14)
    text(48,978,'Rendered SVG specimens — not an Orca screenshot.' if lang=='en' else '此为 SVG 图鉴，并非 Orca 窗口截图。',size=15)
    p.append('</svg>')
    (ROOT/'docs'/('icons-gallery.svg' if lang=='en' else 'icons-gallery-zh.svg')).write_text(''.join(p),encoding='utf-8')
print('Built two specimen sheets from 36 actual file SVGs and two folder states')
