"""Paper Fold 2: explicit, reproducible file marks. No font or runtime dependencies."""
from pathlib import Path
import json,re,hashlib

ROOT=Path(__file__).resolve().parents[1]
COLORS=dict(ink='#817E77',slate='#6D8190',blue='#4D83B5',steel='#6083A0',cyan='#2E88A7',teal='#3C8B87',green='#578B46',olive='#7F8332',amber='#A97416',brown='#A07650',clay='#C26540',rose='#C6605D',magenta='#BE5F8F',plum='#996FA9',indigo='#7677C4',white='#FAF9F6')
def p(d,c,w=1.5,fill=False):
    return f'<path d="{d}" '+(f'fill="{c}"' if fill else f'stroke="{c}" stroke-width="{w}"')+'/>'
def rect(x,y,w,h,c,r=0,stroke=False):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" '+(f'stroke="{c}" stroke-width="1.5"' if stroke else f'fill="{c}"')+'/>'
def circ(x,y,r,c,stroke=False):
    return f'<circle cx="{x}" cy="{y}" r="{r}" '+(f'stroke="{c}" stroke-width="1.5"' if stroke else f'fill="{c}"')+'/>'
def svg(b):return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none" stroke-linecap="round" stroke-linejoin="round">'+b+'</svg>\n'

# Letterforms are original vector strokes, not embedded font/text. 3×5 em.
LETTERS={
'A':'M0 5 1.5 0 3 5M.5 3.3h2','B':'M0 5V0h1.6Q4 0 2.7 2.4Q4 5 1.6 5ZM0 2.4h2',
'C':'M3 .5Q0-1 0 2.5T3 4.5','D':'M0 0h1Q3 0 3 2.5T1 5H0Z','E':'M3 0H0v5h3M0 2.4h2.3',
'F':'M0 5V0h3M0 2.3h2.3','G':'M3 .6Q0-1 0 2.5T3 4.4V2.6H1.6','H':'M0 0v5M3 0v5M0 2.5h3',
'I':'M.2 0h2.6M1.5 0v5M.2 5h2.6','J':'M0 4Q0 5 1.5 5T3 3.5V0','K':'M0 0v5M3 0 0 2.5 3 5',
'L':'M0 0v5h3','M':'M0 5V0l1.5 2.5L3 0v5','N':'M0 5V0l3 5V0','O':'M1.5 0Q0 0 0 2.5T1.5 5T3 2.5T1.5 0Z',
'P':'M0 5V0h1.5Q3 0 3 1.4T1.5 2.8H0','Q':'M1.5 0Q0 0 0 2.5T1.5 5T3 2.5T1.5 0ZM1.6 3.5 3.5 5.5',
'R':'M0 5V0h1.5Q3 0 3 1.4T1.5 2.8H0M1.5 2.8 3 5','S':'M3 .4Q0-1 0 1.4Q0 2.2 1.5 2.5T3 3.6Q3 6 0 4.6',
'T':'M0 0h3M1.5 0v5','U':'M0 0v3.5Q0 5 1.5 5T3 3.5V0','V':'M0 0 1.5 5 3 0',
'W':'M0 0 .5 5 1.5 2.7 2.5 5 3 0','X':'M0 0 3 5M3 0 0 5','Y':'M0 0 1.5 2.5 3 0M1.5 2.5V5',
'Z':'M0 0h3L0 5h3','0':'M1.5 0Q0 0 0 2.5T1.5 5T3 2.5T1.5 0ZM.3 4 2.7 1','1':'M.3 1 1.5 0v5M.3 5h2.4',
'2':'M0 1Q0 0 1.5 0T3 1.4L0 5h3','3':'M0 .2Q3-1 3 1.2T1.5 2.5Q3 2.5 3 3.8T0 4.8',
'4':'M2.5 5V0L0 3.4h3.5','5':'M3 0H0v2.5h1.5Q3 2.5 3 3.7T0 4.7','6':'M3 .2Q0-1 0 2.5T1.5 5T3 3.5T0 2.5',
'7':'M0 0h3L1 5','8':'M1.5 0Q0 0 0 1.2T1.5 2.5T3 3.8T1.5 5T0 3.8T1.5 2.5T3 1.2T1.5 0Z',
'9':'M0 4.8Q3 6 3 2.5T1.5 0T0 1.5T3 2.5','+':'M0 2.5h3M1.5 1v3','#':'M1 0 .5 5M2.7 0 2.2 5M0 1.7h3.4M0 3.4h3.4'}
def lettering(text,c,x=3,y=4,scale=1,stroke=1.25):
    """Bake the coordinates into the paths; runtime transforms are unnecessary."""
    out=''
    for n,ch in enumerate(text):
        d=LETTERS[ch];tokens=re.findall(r'[A-Za-z]|[-+]?(?:\d*\.\d+|\d+)',d);res=[];cmd=None;ix=0
        for t in tokens:
            if t.isalpha():cmd=t;ix=0;res.append(t);continue
            v=float(t)*scale
            if cmd.isupper():v+= (x+n*4.5*scale if cmd in 'H' or (cmd not in 'V' and ix%2==0) else y)
            res.append(f'{v:.3f}'.rstrip('0').rstrip('.'));ix+=1
        out+=p(' '.join(res),c,stroke)
    return out

ROWS=[]
def group(category,shape,color,items):
    # key|label|mark ; marks intentionally selected, never generated from hashes.
    for item in items.split():
        bits=item.split('|');key=bits[0];label=bits[1].replace('_',' ') if len(bits)>1 else key
        mark=bits[2] if len(bits)>2 else ''
        ROWS.append(dict(kind='extension',key=key,label=label,category=category,shape=shape,color=color,mark=mark,variant=0))

group('Languages','python','blue','py|Python pyi|Python_stub|I pyw|Python_window|W pyx|Cython|X pxd|Cython_declaration|D')
group('Notebooks','notebook','plum','ipynb|Jupyter_notebook qmd|Quarto|Q rmd|R_Markdown|R jl|Julia|J')
group('Languages','hex','blue','c|C|C h|C_header|H cpp|C++|C+ hpp|C++_header|H+ cc|C++_cc|CC cxx|C++_cxx|CX hxx|C++_hxx|HX cs|C_sharp|C# m|MATLAB|M mm|Objective_C++|M+ cu|CUDA|CU cuh|CUDA_header|CH')
group('Languages','punch','plum','f|Fortran_fixed|F for|Fortran_source|FR ftn|Fortran_ftn|FT f90|Fortran_90|90 f95|Fortran_95|95 f03|Fortran_2003|03 f08|Fortran_2008|08 f18|Fortran_2018|18 f23|Fortran_2023|23')
group('Languages','seal','amber','js|JavaScript|JS mjs|JavaScript_ES_module|MJ cjs|JavaScript_CommonJS|CJ')
group('Languages','seal','blue','ts|TypeScript|TS mts|TypeScript_ES_module|MT cts|TypeScript_CommonJS|CT')
group('Languages','orbit','amber','jsx|React_JavaScript|J')
group('Languages','orbit','blue','tsx|React_TypeScript|T')
group('Languages','header','blue','d.ts|TypeScript_declaration|T d.mts|TypeScript_module_declaration|M d.cts|TypeScript_CommonJS_declaration|C')
group('Languages','gear','clay','rs|Rust|R')
group('Languages','speed','cyan','go|Go|GO')
group('Languages','cup','clay','java|Java|J class|JVM_bytecode|C')
group('Languages','gem','rose','rb|Ruby|R rbs|Ruby_signature|S erb|Embedded_Ruby|E')
group('Languages','oval','indigo','php|PHP|P phtml|PHP_template|PH')
group('Languages','moon','indigo','lua|Lua|L')
group('Languages','seal','magenta','kt|Kotlin|K kts|Kotlin_script|KS')
group('Languages','wing','clay','swift|Swift|S')
group('Languages','steps','rose','scala|Scala|S sc|Scala_script|SC')
group('Languages','dart','cyan','dart|Dart|D')
group('Languages','zig','amber','zig|Zig|Z')
group('Languages','lambda','plum','hs|Haskell|H lhs|Literate_Haskell|L')
group('Languages','drop','plum','ex|Elixir|E exs|Elixir_script|EX')
group('Languages','seal','steel','r|R|R pl|Perl|PL pm|Perl_module|PM clj|Clojure|CL cljs|ClojureScript|CS cljc|Clojure_common|CC edn|EDN|ED erl|Erlang|ER hrl|Erlang_header|HR el|Emacs_Lisp|EL lisp|Lisp|LI cl|Common_Lisp|CL scm|Scheme|SC rkt|Racket|RK groovy|Groovy|GR gradle|Gradle|GD nim|Nim|NI nims|Nim_script|NS v|V|V d|D|D pas|Pascal|PA pp|Pascal_unit|PP ml|OCaml|ML mli|OCaml_interface|MI fs|F_sharp|F# fsx|F_sharp_script|FX fsproj|F_sharp_project|FP vb|Visual_Basic|VB vbs|VB_script|VS asm|Assembly|AS s|Assembly_source|S sol|Solidity|SO move|Move|MV')
group('Documents','markdown','plum','md|Markdown markdown|Markdown_long|M mdx|MDX|X')
group('Documents','lines','ink','rst|reStructuredText|R adoc|AsciiDoc|A org|Org|O txt|Text|T text|Plain_text|TX log|Log|L')
group('Office','word','blue','docx|Word_document doc|Word_legacy|D docm|Word_macro|M dotx|Word_template|T dotm|Word_macro_template|MT odt|OpenDocument_text|O rtf|Rich_text|R pages|Pages|P')
group('Office','excel','green','xlsx|Excel_workbook xls|Excel_legacy|L xlsm|Excel_macro|M xlsb|Excel_binary|B xltx|Excel_template|T ods|OpenDocument_sheet|O numbers|Numbers|N')
group('Office','slides','clay','pptx|PowerPoint ppt|PowerPoint_legacy|L pptm|PowerPoint_macro|M potx|PowerPoint_template|T odp|OpenDocument_slides|O')
group('Documents','pdf','rose','pdf|PDF xps|XPS|X epub|EPUB|E mobi|Mobi|M')
group('Science','tex','teal','tex|LaTeX|TX ltx|LaTeX_source|LT sty|LaTeX_style|ST cls|LaTeX_class|CL bib|Bibliography|BI bst|BibTeX_style|BS')
group('Web','shield','clay','html|HTML|H htm|HTML_short|HT xhtml|XHTML|XH shtml|Server_HTML|SH')
group('Web','pen','blue','css|CSS|C scss|SCSS|SC sass|Sass|SA less|Less|LE styl|Stylus|ST pcss|PostCSS|PC')
group('Web','chevron','green','vue|Vue|V')
group('Web','ribbon','clay','svelte|Svelte|S')
group('Web','rocket','plum','astro|Astro|A')
group('Configuration','braces','amber','json|JSON jsonc|JSON_comments|C json5|JSON5|5 jsonl|JSON_lines|L ndjson|Newline_JSON|N geojson|GeoJSON|G webmanifest|Web_manifest|W')
group('Configuration','toml','teal','toml|TOML')
group('Configuration','yaml','magenta','yaml|YAML yml|YML|Y')
group('Configuration','sliders','steel','ini|INI|I conf|Config|CO cfg|Config_short|CF properties|Properties|P config|Configuration|C config.ts|TypeScript_config|TS config.js|JavaScript_config|JS config.mjs|ES_module_config|MJ config.cjs|CommonJS_config|CJ config.json|JSON_config|J')
group('Configuration','angle','olive','xml|XML xsd|XML_schema|S xsl|XSL|L xslt|XSLT|T plist|Property_list|P rss|RSS|R atom|Atom|A xaml|XAML|X')
group('Security','key','olive','pem|PEM|P key|Private_key|K crt|Certificate|C cer|Certificate_DER|CE p12|PKCS12|12 pfx|PKCS12_archive|PX asc|ASCII_signature|A gpg|GPG|G pub|Public_key|PU')
group('Security','lock','ink','lock|Lockfile lockb|Binary_lockfile|B')
group('Shell','terminal','teal','sh|Shell|S bash|Bash|B zsh|Zsh|Z fish|Fish|F nu|Nushell|N bat|Batch|BA cmd|Command|C')
group('Shell','terminal','blue','ps1|PowerShell|P psm1|PowerShell_module|M psd1|PowerShell_data|D')
group('Testing','check','green','test.ts|TypeScript_test|T test.tsx|TSX_test|TX test.js|JavaScript_test|J test.jsx|JSX_test|JX test.mjs|ES_module_test|M test.py|Python_test|P spec.ts|TypeScript_spec|ST spec.tsx|TSX_spec|SX spec.js|JavaScript_spec|SJ spec.jsx|JSX_spec|SY feature|Gherkin|F')
group('Images','bezier','amber','svg|SVG svgz|Compressed_SVG|Z eps|EPS|E ai|Illustrator|A')
group('Images','image','green','png|PNG|P jpg|JPEG_short|J jpeg|JPEG|JE gif|GIF|G webp|WebP|W avif|AVIF|A bmp|Bitmap|B ico|Icon|I heic|HEIC|HE heif|HEIF|HF tif|TIFF_short|T tiff|TIFF|TI psd|Photoshop|PS sketch|Sketch|SK fig|Figma|FI')
group('Media','video','rose','mp4|MP4|4 mov|QuickTime|M webm|WebM|W mkv|Matroska|K avi|AVI|A')
group('Media','audio','plum','mp3|MP3|3 wav|Wave|W flac|FLAC|F ogg|Ogg|O m4a|M4A|4 aac|AAC|A midi|MIDI|MI mid|MIDI_short|M')
group('Archives','zip','brown','zip|ZIP|Z tar|Tar|T gz|Gzip|G tgz|Tar_gzip|TG bz2|Bzip2|B xz|XZ|X zst|Zstandard|ZS 7z|7Zip|7 rar|RAR|R whl|Python_wheel|PY jar|Java_archive|J war|Java_web_archive|W tar.gz|Tar_gzip_compound|TZ tar.xz|Tar_xz_compound|TX')
group('Data','database','teal','sql|SQL|S sqlite|SQLite|SL sqlite3|SQLite3|S3 db|Database|D prisma|Prisma|P graphql|GraphQL|G gql|GraphQL_short|GQ')
group('Data','grid','green','csv|CSV|C tsv|TSV|T psv|PSV|P parquet|Parquet|PQ feather|Feather|F arrow|Arrow|A')
group('Science','cube','cyan','nc|NetCDF|NC netcdf|NetCDF_long|N4 h5|HDF5|H5 hdf5|HDF5_long|HF hdf|HDF|HD npy|NumPy|NP npz|NumPy_archive|NZ mat|MATLAB_data|M rds|R_data|R rdataset|R_dataset|RD pkl|Pickle|PK pickle|Pickle_long|PI fits|FITS|FI fit|FITS_short|FT zarr|Zarr|ZA')
group('Build','hammer','clay','mk|Make|M cmake|CMake|CM meson|Meson|ME bazel|Bazel|BA bzl|Bazel_extension|BZ ninja|Ninja|NI csproj|C_sharp_project|C# sln|Solution|SL vcxproj|C++_project|C+')
group('Build','chip','steel','exe|Executable|EX dll|Dynamic_library|DL so|Shared_object|SO dylib|Dynamic_library_Mac|DY o|Object|O obj|Object_Windows|OB a|Static_library|A lib|Library|LI wasm|WebAssembly|WA bin|Binary|BI')
group('Fonts','seal','plum','ttf|TrueType|TT otf|OpenType|OT woff|WOFF|WF woff2|WOFF2|W2')
group('Version control','diff','green','diff|Diff patch|Patch|P')
group('Containers','boxes','blue','dockerfile|Dockerfile|D')
group('Languages','chip','blue','pyc|Python_bytecode|PC pyd|Python_extension|PD pyo|Python_optimized|PO')
group('Languages','seal','cyan','nix|Nix|NX proto|Protocol_Buffers|PB idl|Interface_definition|ID thrift|Thrift|TH')
group('Configuration','sliders','plum','hcl|HCL|HC tf|Terraform|TF tfvars|Terraform_variables|TV tfstate|Terraform_state|ST')
group('Web','angle','clay','ejs|EJS|EJ hbs|Handlebars|HB mustache|Mustache|MU twig|Twig|TW jinja|Jinja|JI jinja2|Jinja2|J2 liquid|Liquid|LQ njk|Nunjucks|NJ pug|Pug|PG')
group('Graphics','gem','cyan','glsl|GLSL|GL vert|Vertex_shader|VE frag|Fragment_shader|FR wgsl|WebGPU_shader|WG hlsl|HLSL|HL shader|Shader|SH blend|Blender|BL stl|STL|ST gltf|glTF|GT glb|Binary_glTF|GB')
group('Science','cube','indigo','rdata|R_workspace|RD sav|SPSS|SA dta|Stata|DT')

# Exact filenames take precedence over suffixes. Every entry is explicitly listed.
def names(shape,color,category,items):
    start=len(ROWS);group(category,shape,color,items)
    for r in ROWS[start:]:r['kind']='name'
names('book','blue','Project documents','readme|Readme|R readme.md|Readme_Markdown|M readme.txt|Readme_text|T readme.rst|Readme_RST|S')
names('scales','olive','Project documents','license|License|L license.md|License_Markdown|M license.txt|License_text|T licence|Licence|C copying|Copying|CP notice|Notice|N')
names('history','plum','Project documents','changelog.md|Changelog|C changes.md|Changes|CH history.md|History|H releases.md|Releases|R news.md|News|N')
names('shield','green','Project documents','security.md|Security|S code_of_conduct.md|Code_of_conduct|C contributing.md|Contributing|+ authors|Authors|A codeowners|Code_owners|O citation.cff|Citation|Q')
names('git','clay','Version control','.gitignore|Git_ignore|I .gitattributes|Git_attributes|A .gitmodules|Git_modules|M .gitkeep|Git_keep|K .mailmap|Git_mailmap|E .git-blame-ignore-revs|Git_blame_ignore|B')
names('boxes','blue','Containers','containerfile|Containerfile|C dockerfile|Dockerfile|D dockerfile.dev|Docker_development|DV dockerfile.prod|Docker_production|PR .dockerignore|Docker_ignore|I compose.yaml|Compose_YAML|CY compose.yml|Compose_YML|CM docker-compose.yml|Docker_Compose_YML|DC docker-compose.yaml|Docker_Compose_YAML|DY')
names('package','amber','Packages','package.json|NPM_package|N cargo.toml|Cargo_package|R pyproject.toml|Python_project|P go.mod|Go_module|G gemfile|Ruby_gems|RB composer.json|Composer|PH requirements.txt|Python_requirements|PY pubspec.yaml|Dart_package|D deno.json|Deno|DE deno.jsonc|Deno_comments|DC setup.py|Python_setup|SP setup.cfg|Python_setup_config|SC pom.xml|Maven|MV build.gradle|Gradle_build|GR build.gradle.kts|Gradle_Kotlin|GK')
names('lock','ink','Packages','package-lock.json|NPM_lock|N pnpm-lock.yaml|PNPM_lock|PN yarn.lock|Yarn_lock|Y go.sum|Go_checksums|G cargo.lock|Cargo_lock|R poetry.lock|Poetry_lock|P uv.lock|UV_lock|U gemfile.lock|Ruby_lock|RB composer.lock|Composer_lock|PH bun.lock|Bun_lock|B bun.lockb|Bun_binary_lock|BB')
names('key','olive','Environment','.env|Environment|E .env.local|Local_environment|L .env.development|Development_environment|D .env.production|Production_environment|P .env.test|Test_environment|T .env.example|Example_environment|X .envrc|Direnv|R')
names('chat','clay','Agents','agents.md|Agent_instructions|A agent.md|Agent_instruction|AG claude.md|Claude_instructions|C gemini.md|Gemini_instructions|G .cursorrules|Cursor_rules|CU .windsurfrules|Windsurf_rules|W copilot-instructions.md|Copilot_instructions|CP llms.txt|LLM_index|L orca-plugin.json|Orca_plugin|O')
names('sliders','steel','Tooling','tsconfig.json|TypeScript_options|TS jsconfig.json|JavaScript_options|JS .editorconfig|Editor_config|E .prettierrc|Prettier|P .eslintrc|ESLint|ES .npmrc|NPM_config|N .nvmrc|Node_version|NV .babelrc|Babel|B biome.json|Biome|BI eslint.config.js|ESLint_config_JS|EJ eslint.config.mjs|ESLint_ES_module|EM vite.config.ts|Vite_TypeScript|VT vite.config.js|Vite_JavaScript|VJ next.config.js|Next_JS|NJ next.config.mjs|Next_ES_module|NM next.config.ts|Next_TS|NT .python-version|Python_version|PY rust-toolchain.toml|Rust_toolchain|RU .tool-versions|Tool_versions|TV .ruff.toml|Ruff|RF ruff.toml|Ruff_config|RC pytest.ini|Pytest|PT tox.ini|Tox|TX')
names('hammer','clay','Build','makefile|Makefile|M gnumakefile|GNU_Make|GM justfile|Just|J taskfile.yml|Taskfile|T cmakelists.txt|CMake_lists|CM build|Build|B build.bazel|Bazel_build|BA meson.build|Meson_build|ME')
names('check','green','CI','.travis.yml|Travis|T .gitlab-ci.yml|GitLab_CI|G jenkinsfile|Jenkins|J azure-pipelines.yml|Azure_pipeline|A')
names('lock','ink','Packages','flake.lock|Nix_lock|NX pipfile.lock|Pipenv_lock|PI')

# Full project filenames have their own marks, even when a broad suffix exists.
OVERRIDES={('extension','cl'):'LI',('name','.prettierrc'):'PR',('name','tsconfig.json'):'TC',('name','jsconfig.json'):'JC',('name','.env.production'):'PR',('name','bun.lock'):'BU',('name','.travis.yml'):'TR',('name','jenkinsfile'):'JE',('name','makefile'):'MF',('name','cmakelists.txt'):'CL',('name','meson.build'):'MB',('name','build.bazel'):'BB',('name','dockerfile'):'DK'}
for row in ROWS:
    if (row['kind'],row['key']) in OVERRIDES:row['mark']=OVERRIDES[(row['kind'],row['key'])]
    if row['kind']=='extension' and row['key']=='cl':row['mark']='LC'
    if row['kind']=='extension' and row['key']=='jl':row.update(category='Languages',shape='julia',mark='')
    if row['kind']=='extension' and row['key']=='rdata':row['mark']='RW'
    if row['kind']=='name' and row['key']=='.tool-versions':row['mark']='VR'

def draw(row):
    c=COLORS[row['color']];w=COLORS['white'];ink=COLORS['ink'];sh=row['shape'];m=row['mark'];b=''
    # Main silhouettes occupy most of the 16 px square. Marks, where present,
    # occupy 6–10 px and never depend on the common paper-sheet outline.
    if sh=='python':
        b=p('M12 3.5H6a2.25 2.25 0 0 0 0 4.5h2',c,2.5)+p('M8 8h2a2.25 2.25 0 0 1 0 4.5H3.75',COLORS['amber'],2.5)+circ(12,3.5,1.7,c)+circ(3.75,12.5,1.3,COLORS['amber'])+circ(12.4,3.1,.6,w)
        if m:b+=lettering(m,c,1,1,.65,.9)
        return b
    if sh=='notebook':
        b=rect(3,1.5,11.5,13,c,1.5,True)+p('M1.5 4h3M1.5 8h3M1.5 12h3',COLORS['amber'],1.7)
        return b+(lettering(m,c,7,5,1.1,1.4) if m else rect(6,4,5.5,2,c,.3)+p('M6 9h5.5M6 11.5h3.5',c,1.5))
    if sh=='markdown':
        b=rect(1,2.5,14,11,c,1.5,True)+p('M3.2 10.5v-5L5.4 8l2.2-2.5v5M11.5 5.5v5m-1.6-1.6 1.6 1.6 1.6-1.6',c,1.5)
        if m:b=rect(1,2,14,12,c,1.5)+lettering('M'+m,w,3,5,1,1.3)
        return b
    if sh=='word':
        b=p('M6 1.5h4.5l3.5 3.5v9H6z',c,1.3)+p('M10.5 1.5V5H14M11.5 8H13M11.5 11H13',c,1.2)+rect(.5,5,9.5,9.5,c,1.5)
        b+=p('M2.1 7.3 3.1 12 5.2 9.1 7.2 12 8.2 7.3',w,1.35)
        if m:b=rect(1.5,1.5,13,13,c,1.5)+lettering('W'+m[:1],w,3.2,5,1,1.25)+(p('M2 13h12',w,1) if len(m)>1 else '')
        return b
    if sh=='excel':
        b=rect(5,1.5,9.5,13,c,1.3,True)+p('M6 6h8M6 10h8M10.5 2v12',c,1.2)+rect(.5,4.5,8.5,9,c,1.4)+p('M2.8 7 6.5 11M6.5 7 2.8 11',w,1.5)
        if m:b=rect(1,1.5,14,13,c,1.5)+lettering('X'+m,w,3,4,1,1.3)+p('M3 12h10',w,1.3)
        return b
    if sh=='slides':
        b=rect(1,2,14,10,c,1.3)+p('M8 12v3M5 15h6',c,1.5)
        return b+(lettering(m,w,6,4,.95,1.3) if m else circ(8,7,3,w)+p('M8 4v3h3',c,1.3))
    if sh=='pdf':
        b=p('M8 1 10 3h3v3l2 2-2 2v3h-3l-2 2-2-2H3v-3L1 8l2-2V3h3z',c,fill=True)
        return b+(lettering(m,w,6,5,1,1.4) if m else p('M5 10q3-8 3-6t-3 6q6-4 6-1t-4-2',w,1.3))
    if sh=='braces':
        b=p('M5 2H3.5v4L1.5 8l2 2v4H5M11 2h1.5v4l2 2-2 2v4H11',c,1.9)
        return b+(lettering(m,c,6.5,5,.8,1.1) if m else circ(8,5.5,1,c)+circ(8,10.5,1,c))
    if sh=='toml':return p('M5 2H2v12h3M11 2h3v12h-3M5.5 5.5h5M5.5 10.5h5',c,2)
    if sh=='yaml':
        b=p('M2 2.5h5M4.5 6h7M7 9.5h7M7 13h5',c,2)+circ(2,6,.8,c)+circ(4.5,9.5,.8,c)+circ(4.5,13,.8,c)
        return b if not m else p('M2 2.5h12M2 6h5M4.5 9.5h7M7 13h7',c,2)+circ(2,9.5,.8,c)+circ(4.5,13,.8,c)
    if sh=='git':
        b=p('M8 .8 15.2 8 8 15.2 .8 8Z',c,fill=True)
        if m=='I':return b+p('M5 4v7M5 6h5v4M3 12 12 3',w,1.25)
        return b+lettering(m,w,6.3,5,1,1.4)
    if sh=='hex':b=p('M4 1.5h8l3 6.5-3 6.5H4L1 8Z',c,fill=True)
    elif sh=='seal':b=rect(1,1,14,14,c,2)
    elif sh=='punch':b=p('M3 1.5h12v13H1v-11z',c,fill=True)+p('M4 3h1M7 3h1M10 3h1',w,1)
    elif sh=='header':b=p('M2 1.5h9l3 3v10H2z',c,fill=True)+p('M3.5 4.5h6',w,1.2)
    elif sh=='orbit':
        b=p('M15 8A7 2.6 0 1 1 1 8A7 2.6 0 1 1 15 8M11.5 14.062A7 2.6 60 1 1 4.5 1.938A7 2.6 60 1 1 11.5 14.062M11.5 1.938A7 2.6 -60 1 1 4.5 14.062A7 2.6 -60 1 1 11.5 1.938',c,1.1)
        return b+(circ(8,8,1.4,c) if m=='J' else p('M8 6.2 9.8 8 8 9.8 6.2 8Z',c,fill=True))
    elif sh=='julia':return circ(8,3.7,2.8,COLORS['green'])+circ(4.3,11.3,2.8,COLORS['plum'])+circ(11.7,11.3,2.8,COLORS['rose'])
    elif sh=='gear':b=p('M6 1h4l.5 2 1 .5 2-.5 2 3-1.5 1.5v1L15 10l-2 3-2-.5-1 .5-.5 2H6l-.5-2-1-.5-2 .5-2-3L2 8.5v-1L.5 6l2-3 2 .5 1-.5z',c,fill=True)
    elif sh=='speed':b=rect(3,3,12,10,c,5)+p('M1 5h2M.5 8h2M1 11h2',c,1.5)
    elif sh=='cup':b=p('M2 6h10v4q0 3-5 3t-5-3zM12 7h2v3h-2',c,1.6)+p('M5 4q-2-1 0-3M8 4q2-1 0-3M2 15h12',c,1.4)
    elif sh=='gem':b=p('M4 1.5h8l3 4.5-7 9-7-9Z',c,fill=True)+p('M1 6h14M4 1.5 8 15 12 1.5',w,1)
    elif sh=='oval':b=p('M8 2Q0 2 0 8t8 6q8 0 8-6T8 2Z',c,fill=True)
    elif sh=='moon':b=p('M11 1.5a6.7 6.7 0 1 0 3.5 11A8 8 0 0 1 11 1.5Z',c,fill=True)+circ(12.8,3.5,1.8,c)
    elif sh=='wing':b=p('M1 3 8 8 4 1l9 7 2 6-5-2-8 2 4-4Z',c,fill=True)
    elif sh=='steps':b=p('M1 3 15 1v4L1 7zm0 5 14-2v4L1 12zm0 5 14-2v3L1 16Z',c,fill=True)
    elif sh=='dart':b=p('M1 6 6 1h5l4 14H5Z',c,fill=True)+p('M1 6h7l7 9',w,1.2)
    elif sh=='zig':b=p('M1 1h14v3L5 12h10v3H1v-3l10-9H1Z',c,fill=True)
    elif sh=='lambda':b=p('M3 1h3l7 14M2 15 7.5 5',c,2.4)
    elif sh=='drop':b=p('M9 1q-10 10-5 13t9-3Q12 7 9 1Z',c,fill=True)
    elif sh=='lines':b=rect(2,1.5,12,13,c,1.5,True)+p('M4 11.5h8',c,1.5)
    elif sh=='tex':b=p('M1 2h14v12H1Z',c,1.5)
    elif sh=='shield':b=p('M1.5 1.5h13l-1.5 11L8 15l-5-2.5z',c,fill=True)
    elif sh=='pen':b=p('M10 1 15 6 6 15H1v-5Z',c,fill=True)+p('M8 3 13 8',w,1.3)
    elif sh=='chevron':b=p('M1 2h4l3 6 3-6h4L8 15Z',c,fill=True)
    elif sh=='ribbon':b=p('M12 2q-2-2-5 0L3 5q-3 4 2 5l6-5q4-1 2 4l-6 5q-3 2-5-1',c,3)
    elif sh=='rocket':b=p('M6 1h4l5 11-5-2-2-6-2 6-5 2Z',c,fill=True)+p('M6 12 8 15l2-3',COLORS['clay'],2)
    elif sh=='sliders':b=p('M2 3h12M2 8h12M2 13h12',c,1.5)+rect(4,1,2.5,4,c,1)+rect(10,6,2.5,4,c,1)+rect(5,11,2.5,4,c,1)
    elif sh=='angle':b=p('M5 3 1 8l4 5M11 3l4 5-4 5M9.5 2 6.5 14',c,1.7)
    elif sh=='key':b=circ(5,5,3.3,c,True)+p('M7.5 7.5 14 14M11 11l2-2M13 13l2-2',c,2)
    elif sh=='lock':b=p('M4.5 7V5a3.5 3.5 0 0 1 7 0v2',c,1.8)+rect(2,6.5,12,8.5,c,2)
    elif sh=='terminal':b=rect(1,2,14,12,c,1.5,True)+p('M3 5 6 8 3 11M8 11h4',c,1.6)
    elif sh=='check':b=rect(1,1,14,14,c,3)+p('M3 9 5.5 12 12.5 4',w,1.8)
    elif sh=='bezier':b=p('M2 12Q2 3 13 3',c,1.8)+p('M2 3h11M2 3v9',c,1)+rect(.5,10.5,3,3,c,.4)+rect(11.5,1.5,3,3,c,.4)+circ(2,3,1.5,c)
    elif sh=='image':b=rect(1,1.5,14,13,c,1.5,True)+p('M2 12 6 7 9 10l2-2 3 4Z',c,fill=True)+circ(11.5,4.5,1.5,c)
    elif sh=='video':b=rect(1,3,11,10,c,2)+p('M12 6 15 4v8l-3-2z',c,fill=True)+p('M5 5.5 9 8l-4 2.5Z',w,fill=True)
    elif sh=='audio':b=p('M1 6v4M4 3v10M7 1v14M10 4v8M13 6v4',c,1.8)
    elif sh=='zip':b=p('M2 2h12v13H2ZM1 2h14V.5H1Z',c,fill=True)+p('M7 2h2v2H7v2h2v2H7v2h2',w,1.3)+rect(6.5,10,3,3,w,.8,True)
    elif sh=='database':b=p('M1.5 4q6.5-5 13 0v8q-6.5 5-13 0ZM1.5 4q6.5 5 13 0M1.5 8q6.5 5 13 0',c,1.7)
    elif sh=='grid':b=rect(1.5,1.5,13,13,c,1,True)+p('M2 5h12M6 5v9M10 5v9M2 10h12',c,1.3)+rect(2,2,12,2,c)
    elif sh=='cube':b=p('M8 1 15 5v7l-7 3-7-3V5ZM1 5l7 3 7-3M8 8v7',c,1.5)
    elif sh=='hammer':b=p('M3 1h7l4 4-3 3-2-2-7 9-2-2 7-9-2-1z',c,fill=True)
    elif sh=='chip':b=rect(3,3,10,10,c,1.5)+p('M5 1v2M9 1v2M5 13v2M9 13v2M1 5h2M1 9h2M13 5h2M13 9h2',c,1.5)
    elif sh=='diff':b=rect(2,1.5,12,13,c,1.3,True)+p('M4.5 5h7M8 2.5v5M4.5 11h7',c,1.7)
    elif sh=='boxes':b=rect(1,8,14,5,c,1)+rect(2,3,3.3,3.3,c,.3)+rect(6.3,3,3.3,3.3,c,.3)+rect(10.6,3,3.3,3.3,c,.3)
    elif sh=='book':b=p('M8 4Q5 1 1 2v11q4-1 7 2 3-3 7-2V2q-4-1-7 2Zm0 0v11',c,1.5)
    elif sh=='scales':b=p('M8 1v13M4 15h8M2 4h12M3 4 1 9h5L3 4M13 4l-3 5h5Z',c,1.5)
    elif sh=='history':b=p('M3 4a6 6 0 1 1-1 7M1 1v4h4M8 4v4l3 2',c,1.7)
    elif sh=='package':b=p('M1 4 8 1l7 3v8l-7 3-7-3Zm0 0 7 3 7-3M8 7v8M4.5 2.5l7 3v3',c,1.5)
    elif sh=='chat':b=p('M2 1.5h12v10H7l-5 4Z',c,fill=True)
    else:raise ValueError(sh)
    if m:
        solid=sh in {'hex','seal','punch','header','gear','speed','oval','moon','wing','steps','dart','drop','shield','lock','chip','chat'}
        if sh in {'cup','gem','zig','lambda','chevron','ribbon','rocket','sliders','angle','key','terminal','check','bezier','image','video','audio','zip','database','grid','cube','hammer','diff','boxes','book','scales','history','package','pen'}:
            # A substantial lower corner label carries format semantics; it is
            # intentionally larger than a tiny generic glyph on a paper sheet.
            width=5 if len(m)==1 else 8.5
            b+=rect(16-width,8,width,8,c,1.1)
            b+=lettering(m,w,16-width+1,9.5,.85,1.15)
        else:
            scale=1.35 if len(m)==1 else 1.05
            x=(16-(3+4.5*(len(m)-1))*scale)/2
            b+=lettering(m,w if solid else c,x,5.3,scale,1.4 if len(m)==1 else 1.25)
    return b

def build(root=ROOT):
    dest=root/'icons/files';dest.mkdir(parents=True,exist_ok=True)
    mapping={'schemaVersion':1,'icons':{'file':'icons/file.svg','folder':'icons/folder.svg','folder-open':'icons/folder-open.svg'},'fileNames':{},'fileExtensions':{},'folderNames':{},'folderNamesExpanded':{}}
    catalogue=[];seen=set();bodies={}
    for row in ROWS:
        assert (row['kind'],row['key']) not in seen,row;seen.add((row['kind'],row['key']))
        # Preserve a stable filename across future edits and avoid name/extension collisions.
        slug=('dot-' if row['key'].startswith('.') else '')+re.sub('[^a-z0-9]+','-',row['key']).strip('-')
        asset=f"icons/files/{row['kind']}-{slug}.svg"
        body=draw(row)
        if body in bodies:raise AssertionError(f"Indistinguishable geometry: {row['key']} and {bodies[body]}")
        bodies[body]=row['key'];(root/asset).write_text(svg(body),encoding='utf-8')
        mapping['fileNames' if row['kind']=='name' else 'fileExtensions'][row['key']]=asset
        catalogue.append({**row,'path':asset})
    assert len(catalogue)+3<=512,len(catalogue)
    assert len({r['path'] for r in catalogue})==len(catalogue)
    (root/'icons/file.svg').write_text(svg(p('M3 1.5h7l3 3v10H3z',COLORS['ink'],1.4)+p('M10 1.5v3h3',COLORS['ink'],1.3)),encoding='utf-8')
    # Approved kraft folder pair: shared baseline, translucent face and open flap.
    folders={'folder': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none" stroke="#A3763A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M2.25 12V4.25q0-1 1-1H5.5c.9 0 1.1 1.5 2 1.5h5.25q1 0 1 1V12q0 1-1 1h-9.5q-1 0-1-1Z" fill="#A3763A" fill-opacity=".3"/></svg>\n', 'folder-open': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none" stroke="#A3763A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 13H3.25q-1 0-1-1V4.25q0-1 1-1H5.5c.9 0 1.1 1.5 2 1.5h4.75q1 0 1 1v2H6Z" fill="#A3763A" fill-opacity=".15"/><path d="M6 7.75h7.95q.8 0 .58.77l-1.06 3.71q-.22.77-1.02.77H4.5Z" fill="#A3763A" fill-opacity=".3"/></svg>\n'}
    for name,asset in folders.items():
        (root/f'icons/{name}.svg').write_text(asset,encoding='utf-8')
    (root/'icons/theme.json').write_text(json.dumps(mapping,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    (root/'icons/catalogue.json').write_text(json.dumps(catalogue,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    lines=['# Paper Fold 2 · File coverage / 文件覆盖','',f'{len(catalogue)} individual file marks; one honey-kraft folder family. / {len(catalogue)} 个独立文件图标；文件夹统一牛皮纸金棕色。','',
    'Exact filename first, then the longest known suffix, case-insensitive. Unknown files use the neutral paper mark. / 优先匹配完整文件名，再匹配最长已知后缀，不区分大小写。未知文件使用中性纸页。','',
    'These are filename-based visual associations, not content detection. `.h` uses C, `.m` uses MATLAB, `.mm` uses Objective-C++, `.ts` uses TypeScript, and `.key` uses a private key. / 图标依据名称匹配，不分析内容；以上多义后缀按列出的默认含义显示。','',
    '| Match / 匹配 | Meaning / 含义 | SVG |','|---|---|---|']
    for r in catalogue:lines.append(f"| `{r['key'] if r['kind']=='name' else '*.'+r['key']}` | {r['label']} | [SVG](../{r['path']}) |")
    (root/'icons/COVERAGE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(f"Paper Fold 2: {len(mapping['fileExtensions'])} suffixes + {len(mapping['fileNames'])} names + 3 defaults = {len(catalogue)+3} mappings")

if __name__=='__main__':build()
