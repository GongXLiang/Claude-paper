"""Generate Claude Paper's original SVG icons. Python standard library only."""
from pathlib import Path
import json
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
icons = root / 'icons'
icons.mkdir(exist_ok=True)
colors = dict(ink='#817E77', slate='#6D8190', blue='#4D83B5', amber='#A97416', green='#578B46', teal='#3C8B87', plum='#996FA9', rose='#C6605D', clay='#C26540')
backs = dict(ink='#65635E', slate='#556570', blue='#3B668E', amber='#845B11', green='#456D37', teal='#2F6C69', plum='#7C538C', rose='#AA3F3C', clay='#994E31')
def path(d, color, width=1.5, fill=False):
    return f'<path d="{d}" '+(f'fill="{color}"' if fill else f'stroke="{color}" stroke-width="{width}"')+'/>'
def svg(body):
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none" stroke-linecap="round" stroke-linejoin="round">'+body+'</svg>\n'
def write(name, body):
    (icons / (name+'.svg')).write_text(svg(body), encoding='utf-8')
fold=path('M10.5 1.5v3h3z',colors['ink'],fill=True)
sheet=path('M3.5 1.5h7l3 3v10h-10z',colors['ink'],1)+fold
corner=path('M3.5 7V1.5h7l3 3v10H11',colors['ink'],1)+fold
write('file',sheet)
write('doc',sheet+path('M5.5 7.5h6M5.5 10h6M5.5 12.5h3',colors['ink'],1))
write('readme',sheet+path('M5.5 1v5.75L7 5.5l1.5 1.25V1z',colors['blue'],fill=True)+path('M5.5 10h6M5.5 12.5h3',colors['ink'],1))
glyphs = {
 'code':('M4.5 8.75 1.75 11.5l2.75 2.75M7.25 8.75 10 11.5l-2.75 2.75',False),
 'markup':('M3.75 9.25 1.5 11.5l2.25 2.25M8.25 9.25l2.25 2.25-2.25 2.25M6.75 8.5 5.25 14.5',False),
 'style':('M6 8Q1 12 3.5 14Q6 16 8.5 14Q11 12 6 8Z',False),
 'data':('M4.25 8.5H3.5q-.75 0-.75.75v1.25l-1 .75 1 .75v1.25q0 .75.75.75h.75M7.25 8.5H8q.75 0 .75.75v1.25l1 .75-1 .75v1.25q0 .75-.75.75h-.75',False),
 'config':('M1.5 10h8M1.5 13.5h8M4 8.5v3M7 12v3',False),
 'package':('M2 10 6 8l4 2v4l-4 2-4-2zM2 10l4 2 4-2M6 12v4M4 9l4 2',False),
 'env':('M5.5 11.5a2.25 2.25 0 1 1-3-3 2.25 2.25 0 0 1 3 3Zm-.25-.25L9.5 15M7.5 13l1.25-1.25M9 14.5l1-1',False),
 'shell':('M2 9.25 4.5 11.5 2 13.75M6 14h3.75',False),
 'test':('M2 11.75 4.25 14 9.5 8.75',False),
 'agent':('M3 8.5h5.5a1.25 1.25 0 0 1 1.25 1.25v2.25a1.25 1.25 0 0 1-1.25 1.25H5.25L3 15v-1.75a1.25 1.25 0 0 1-1.25-1.25V9.75A1.25 1.25 0 0 1 3 8.5z',True),
 'license':('M5.75 8.25a2.75 2.75 0 1 0 0 5.5 2.75 2.75 0 0 0 0-5.5ZM3.75 13l-.5 2.5 2-1M7.75 13l.5 2.5-2-1',False),
 'history':('M2.5 10a3.5 3.5 0 1 1-.25 3M1.5 8.5V11h2.5M5.75 9.5V12l1.5 1',False),
 'media':('M3 8.5 10 11.75 3 15z',True),
 'archive':('M5 8h2v2H5zM3 10h2v2H3zM5 12h2v2H5zM3 14h2v2H3z',True),
 'database':('M2 9.5c0-2 8-2 8 0s-8 2-8 0v5c0 2 8 2 8 0v-5M2 12c0 2 8 2 8 0',False),
 'table':('M1.5 8.5h9v7h-9zM1.5 11h9M4.5 8.5v7M7.5 8.5v7',False),
 'vcs':('M3 8.5v5M3 11c0 2 5 2 5-1v-1M2 8h2v2H2zM2 13h2v2H2zM7 8h2v2H7z',False),
 'container':('M2 11.5h4v4H2zM6 11.5h4v4H6zM4 7.5h4v4H4z',False),
 'build':('M2 8h3v3H2zM7 12h3v3H7zM2 12h3v3H2zM5 9.5h3.5V12M3.5 11v1',False)
}
filecolors=dict(markup='rose',style='plum',data='green',config='teal',package='amber',env='amber',shell='teal',test='green',agent='clay',license='amber',history='plum',media='plum',archive='ink',database='blue',table='green',vcs='rose',container='teal',build='ink')
for name, role in filecolors.items():
    d, fill=glyphs[name]; write(name,corner+path(d,colors[role],fill=fill))
for name, role in [('script','teal'),('compiled','plum'),('declaration','ink')]:
    write('code-'+name,corner+path(glyphs['code'][0],colors[role]))
write('lock',corner+path('M3.75 10.5V9.25a1.75 1.75 0 0 1 3.5 0v1.25',colors['ink'],1.25)+'<rect x="2.25" y="10.5" width="6.5" height="4.5" rx="1" fill="#817E77"/>')
write('image',corner+path('M1.5 14.75 4.5 10.5l2.25 2.75 1.25-1.5 2.25 3z',colors['green'],fill=True)+'<circle cx="8.25" cy="9" r="1.25" fill="#578B46"/>')
write('diff',corner+path('M2 10h7M5.5 7v6',colors['green'])+path('M2 15h7',colors['rose']))
# File types use a complete colored paper silhouette, with room for the recognizer.
# All marks are original vector paths: no installed font or external logo dependency.
paper_ink='#FAF9F6'
def mark(d,width=1.4):
    return path(d,paper_ink,width)
def paper(role,body,fold_role=None):
    face=path('M3.25 1H10l4 4v8.75A1.25 1.25 0 0 1 12.75 15h-9.5A1.25 1.25 0 0 1 2 13.75v-11A1.25 1.25 0 0 1 3.25 1Z',colors[role],fill=True)
    fold=path('M10 1v3a1 1 0 0 0 1 1h3Z',colors[fold_role] if fold_role else backs[role],fill=True)
    return face+fold+body

file_marks={
 'code-python':('blue',mark('M4 12.8V6.5h1.8a1.75 1.75 0 0 1 0 3.5H4M8.4 8.1l1.7 2.8 1.7-2.8M10.1 10.9 9 13',1.35)),
 'code-c':('blue',mark('M10.7 6.9C8.5 5.3 5 6.7 5 9.6s3.5 4.3 5.7 2.7',1.7)),
 'code-cpp':('blue',mark('M7.2 7.3C5.4 5.9 3.7 7.4 3.7 9.7s1.7 3.7 3.5 2.3',1.45)+mark('M8.5 9.7H10M9.25 8.9v1.6M11.1 9.7h1.5M11.85 8.9v1.6',1)),
 'code-fortran':('plum',mark('M5.5 12.8V6.5h5M5.5 9.5h4',1.7)),
 'code-js':('amber',mark('M3.8 6.6h2.3v4.6c0 2.1-2.6 2.1-2.6.2M12 7.1c-3.5-1.9-4.3 1.6-1.8 2.3s2.8 4.1-1.1 3',1.35)),
 'code-ts':('blue',mark('M3.1 6.6h4M5.1 6.6v6.2M12 7.1c-3.5-1.9-4.3 1.6-1.8 2.3s2.8 4.1-1.1 3',1.35)),
 'word':('blue',mark('M3.8 6.8l1.4 5.8L8 8.9l2.8 3.7 1.4-5.8',1.5)),
 'spreadsheet':('green',mark('M5.3 6.7l5.4 6M10.7 6.7l-5.4 6',1.75)),
 'slides':('clay',mark('M5.7 12.8V6.5h2.7a2 2 0 0 1 0 4H5.7',1.7)),
 'pdf':('rose',mark('M3.5 12V7.5h1a1.2 1.2 0 0 1 0 2.4h-1M7 12V7.5h.6c2.5 0 2.5 4.5 0 4.5H7M10.9 12V7.5H13M10.9 9.7h1.7',1)),
 'vector':('amber',mark('M4 12c0-3.5 2.5-5 7.5-5M8 7h3.5v3.5',1.25)+path('M3 11h2v2H3zM10.5 6h2v2h-2z',paper_ink,fill=True)),
 'html':('clay',mark('M5.3 7.5 3.3 9.8l2 2.3M10.7 7.5l2 2.3-2 2.3M8.8 6.6 7.2 13',1.25)),
 'notebook':('clay',mark('M3.5 7h1M3.5 10h1M3.5 13h1',1.2)+'<rect x="6" y="6.4" width="5.7" height="2.3" rx=".35" stroke="#FAF9F6" stroke-width="1"/><rect x="6" y="10.5" width="5.7" height="2.3" rx=".35" stroke="#FAF9F6" stroke-width="1"/>'),
 'docker':('blue',path('M4 7h2v2H4zM7 7h2v2H7zM10 7h2v2h-2zM7 4h2v2H7zM3 10h10c-.6 2.4-2.2 3.4-5.1 3.4S3.7 12.5 3 10Z',paper_ink,fill=True)),
 'markdown':('plum',mark('M3.6 12V7l2.1 2.5L7.8 7v5M11.1 7.2v5M9.6 10.7l1.5 1.5 1.5-1.5',1.25)),
}
for name,(role,body) in file_marks.items():
    write(name,paper(role,body,'amber' if name=='code-python' else None))
write('latex',corner+path('M9 8.5H2.5L6 12l-3.5 3.5H9',colors['teal'],1.25))
write('table',corner+path(glyphs['table'][0],colors['teal']))
folderglyphs={
 'src':'M6.25 7.75 4.5 9.75l1.75 2M9.75 7.75l1.75 2-1.75 2',
 'test':'M5 9.5l2 2 4-4', 'docs':'M5 8h6M5 10h6M5 12h4',
 'assets':'M4.5 12 7 8.5l2 2 1-1 2 2.5Z', 'config':'M5 8.5h6M5 11h6M7 7.5v2M9 10v2',
 'scripts':'M5 8l2 2-2 2M8.5 12h3', 'agent':'M5 7.5h6v4H7l-2 1z',
 'deps':'M5 8l3-1 3 1v4H5zM5 8l3 1 3-1M8 9v3',
 'build':'M5 7.5h2v2H5zM9 10.5h2v2H9zM7 8.5h3v2',
 'vcs':'M6 7.5v5M6 10c4 0 4-1 4-2M5.5 7.5h1M9.5 7.5h1M5.5 12.5h1'
}
folderglyphs.update(skills='M8 7.5 8.75 9.25 10.5 10 8.75 10.75 8 12.5 7.25 10.75 5.5 10 7.25 9.25z',refs='M6 7.5h4v5L8 11l-2 1.5z',graph='M8 8.5 5.5 12h5z',data='M5.5 8.75c0-1.2 5-1.2 5 0s-5 1.2-5 0v2.75c0 1.2 5 1.2 5 0V8.75')
folderglyphs.update(plugins='M6 7.5v2.5M10 7.5v2.5M5.5 9.5h5v1A2.5 2.5 0 0 1 8 13v1',output='M4.5 11v2h7v-2M8 7v4M6 9l2 2 2-2')
folderroles=dict(plugins='plum',output='teal',skills='clay',refs='plum',graph='teal',data='blue',src='blue',test='green',docs='plum',assets='green',config='teal',scripts='teal',agent='clay',deps='ink',build='ink',vcs='ink')
for name,role in [('folder','slate')]+[(f'folder-{n}',r) for n,r in folderroles.items()]:
    for opened in (False,True):
        back='M1.5 3.5a1 1 0 0 1 1-1h3.59a1 1 0 0 1 .7.29L8 4'+('h4.5a1 1 0 0 1 1 1v2h-10l-2 7z' if opened else 'h5.5a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1h-11a1 1 0 0 1-1-1z')
        front='M3.5 7h11.75l-2 7H1.5z' if opened else 'M1.5 5.5h13V13a1 1 0 0 1-1 1h-11a1 1 0 0 1-1-1z'
        body=path(back,backs[role],fill=True)
        if name=='folder' and opened:body+=path('M4 5h8.5v2.5H4z','#E6E5E0',fill=True)
        body+=path(front,colors[role],fill=True)
        if name!='folder':
            d=folderglyphs[name[7:]]
            # Shared glyph stays within both front silhouettes at y=7..12.5.
            body+=path(d,'#FAF9F6',1.25,name in ('folder-skills','folder-refs'))
            if name=='folder-graph':
                for x,y in [(8,8.5),(5.5,12),(10.5,12)]:body+=f'<circle cx="{x}" cy="{y}" r="1" fill="#FAF9F6"/>'
        write(name+('-open' if opened else ''),body)

maps={k:{} for k in ('fileNames','fileExtensions','folderNames','folderNamesExpanded')}
def assign(group,keys,name):
    for key in keys.split():
        key=key.lower()
        assert key not in maps[group],key
        maps[group][key]='icons/'+name+'.svg'
extensions={
 'markdown':'md mdx markdown rst adoc org', 'doc':'txt text log', 'word':'doc docx docm dotx odt rtf pages', 'spreadsheet':'xls xlsx xlsm xlsb ods numbers', 'slides':'ppt pptx pptm odp', 'pdf':'pdf xps', 'vector':'svg svgz eps ai', 'html':'html htm xhtml shtml', 'notebook':'ipynb qmd rmd', 'latex':'tex ltx sty cls bib bst', 'code-ts':'ts tsx mts cts', 'code-js':'js jsx mjs cjs',
 'code-python':'py pyi','code-c':'c h','code-cpp':'cc cpp hpp cxx hxx','code-fortran':'f for ftn f90 f95 f03 f08 f18','code-script':'rb php lua pl r','code-compiled':'rs go cs java kt kts swift scala zig dart',
 'code-declaration':'d.ts d.mts d.cts','markup':'xml xsd xsl xslt plist rss atom vue svelte astro','style':'css scss sass less styl pcss',
 'data':'json jsonc json5 jsonl ndjson geojson webmanifest','config':'yaml yml toml ini conf cfg properties config.ts config.js config.mjs config.cjs config.json',
 'lock':'lock lockb','env':'pem key crt p12','shell':'sh bash zsh fish ps1 psm1 bat cmd nu',
 'test':'test.ts test.tsx test.js test.jsx test.mjs test.py spec.ts spec.tsx spec.js spec.jsx',
 'image':'png jpg jpeg gif webp avif bmp ico heic heif tif tiff psd','media':'mp4 mov webm mkv mp3 wav flac ogg m4a',
 'archive':'zip tar gz tgz bz2 xz zst 7z rar whl jar','database':'sql sqlite sqlite3 db prisma','table':'csv tsv psv parquet feather arrow',
 'diff':'diff patch','docker':'dockerfile','build':'mk cmake'
}
names={
 'readme':'README README.md README.txt README.rst',
 'config':'tsconfig.json jsconfig.json .editorconfig .prettierrc .eslintrc .npmrc .nvmrc .babelrc biome.json',
 'package':'package.json Cargo.toml pyproject.toml go.mod Gemfile composer.json requirements.txt pubspec.yaml deno.json',
 'lock':'package-lock.json pnpm-lock.yaml yarn.lock go.sum',
 'env':'.env .env.local .env.development .env.production .env.test .env.example .envrc',
 'agent':'AGENTS.md AGENT.md CLAUDE.md GEMINI.md .cursorrules .windsurfrules copilot-instructions.md llms.txt orca-plugin.json',
 'license':'LICENSE LICENSE.md LICENSE.txt LICENCE COPYING NOTICE','history':'CHANGELOG.md CHANGES.md HISTORY.md RELEASES.md NEWS.md',
 'vcs':'.gitignore .gitattributes .gitmodules .gitkeep .mailmap .git-blame-ignore-revs',
 'container':'Containerfile', 'docker':'Dockerfile Dockerfile.dev Dockerfile.prod .dockerignore compose.yaml compose.yml docker-compose.yml docker-compose.yaml',
 'build':'Makefile GNUmakefile justfile Taskfile.yml CMakeLists.txt BUILD BUILD.bazel meson.build'
}
folders={role:' '.join(group['names']) for role,group in json.loads((icons/'folders.json').read_text(encoding='utf-8')).items()}
for n,k in extensions.items(): assign('fileExtensions',k,n)
for n,k in names.items(): assign('fileNames',k,n)
for n,k in folders.items():
    assign('folderNames',k,'folder-'+n);assign('folderNamesExpanded',k,'folder-'+n+'-open')
theme={'schemaVersion':1,'icons':{n:'icons/'+n+'.svg' for n in ('file','folder','folder-open')},**maps}
assert sum(len(v) for v in maps.values())+3 <= 512, 'Orca allows at most 512 mappings'
(icons/'theme.json').write_text(json.dumps(theme,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Generated {len(list(icons.glob("*.svg")))} file/folder SVGs; {sum(len(v) for v in maps.values())+3} mappings.')
