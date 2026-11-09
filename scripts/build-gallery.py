"""Render bilingual gallery SVGs from the actual shipped icons (not app screenshots)."""
from pathlib import Path
from html import escape
import json
ROOT=Path(__file__).resolve().parents[1]
version=json.loads((ROOT/'orca-plugin.json').read_text())['version']
rows=[
 ('Python','Python','code-python'),('Notebook','Notebook','notebook'),('C','C','code-c'),('C++','C++','code-cpp'),('Fortran','Fortran','code-fortran'),('JavaScript','JavaScript','code-js'),('TypeScript','TypeScript','code-ts'),
 ('Word','Word 文档','word'),('Excel','Excel 表格','spreadsheet'),('PowerPoint','演示文稿','slides'),('PDF','PDF','pdf'),('SVG','SVG 矢量图','vector'),('HTML','HTML','html'),('Docker','Docker','docker'),('Markdown','Markdown','markdown'),('JSON','JSON','data'),
 ('Source code','源代码','folder-src'),('Documentation','文档','folder-docs'),('Data','数据','folder-data'),('Plugins','插件','folder-plugins'),('Output','输出','folder-output'),('Skills','技能','folder-skills'),('References','参考资料','folder-refs'),('Graphs','图谱','folder-graph'),('Other folder','其他文件夹','folder'),('Expanded','展开状态','folder-open')]
for lang in ('en','zh'):
    parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000" viewBox="0 0 1600 1000"><rect width="1600" height="1000" fill="#F3F2EF"/>']
    def text(x,y,value,color,size=18):
        parts.append(f'<text x="{x}" y="{y}" font-family="Microsoft YaHei" font-size="{size}" fill="{color}">{escape(value)}</text>')
    text(64,70,'Paper Fold','#201F1D',40)
    text(360,68,'Languages, files & familiar folders.' if lang=='en' else '语言、文件与熟悉的目录。','#65625C',23)
    text(64,110,f'CLAUDE PAPER {version}  /  ORIGINAL SVG ASSET GALLERY' if lang=='en' else f'CLAUDE PAPER {version}  /  原始 SVG 图标图鉴','#65625C',16)
    for x,bg,fg,muted,title in [(40,'#F9F8F5','#1F1E1C','#65625C','Warm Paper' if lang=='en' else '暖纸'),(820,'#2A2927','#EDEBE6','#B5B2AB','Warm Night' if lang=='en' else '暖夜')]:
        parts.append(f'<rect x="{x}" y="150" width="740" height="780" rx="18" fill="{bg}"/>');text(x+32,195,title,fg,25)
        for i,(en,zh,name) in enumerate(rows):
            cx=x+32+(i%3)*234;cy=226+(i//3)*72
            parts.append((ROOT/f'icons/{name}.svg').read_text().replace('<svg ',f'<svg x="{cx}" y="{cy}" width="32" height="32" ',1))
            text(cx+43,cy+23,en if lang=='en' else zh,fg,17)
        text(x+32,898,'Folder categories shown; exact-name matching, slate fallback.' if lang=='en' else '目录按用途展示；实际按名称精确匹配，未知名称使用灰蓝色。',muted,14)
    text(64,969,'Original SVGs at 2x. Rendered gallery, not an Orca screenshot.' if lang=='en' else '原始 SVG 放大 2 倍展示。此为图标图鉴，并非 Orca 窗口截图。','#65625C',16)
    parts.append('</svg>')
    filename='icons-gallery.svg' if lang=='en' else 'icons-gallery-zh.svg'
    (ROOT/'docs'/filename).write_text(''.join(parts),encoding='utf-8')
print('Built English and Chinese gallery SVGs from plugin assets.')
