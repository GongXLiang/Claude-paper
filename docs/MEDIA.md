# Whole Orca, public workspaces / 完整原生工作区

On 2026-11-26 the Chat, agents, editor and files scenes were photographed in both modes in the original public `date-kit` workspace, using an isolated Orca 1.4.274 profile and Claude Paper 0.6.4. The Explorer shows the shipped honey-kraft folders in both states. The two diff scenes show Source Control and come from the 2026-11-10 shoot in Orca 1.4.255.

## Capture and exports

- A real Electron window: **1440 × 900 logical pixels, DPR 2**. PNG masters are **2880 × 1800**; previews are **1600 × 1000**. No source crop is enlarged.
- The complete native renderer is preserved, including navigation, title/tab bars, content panes, right sidebar and status bar. No CLI panels are pasted together or redrawn. A public path such as `D:/paper-demo/date-kit` is intentional.
- `chat-{light,dark}`: genuine native Chat beside code, using Orca's native split. This layout also keeps the machine-name footer hidden through Orca's normal responsive UI. Messages use 16 px; code uses 13 px. The public reply accurately says that it read the files without running tests.
- `agents-{light,dark}`: Claude Code 2.1.332 and Codex CLI 0.172.0 display their original public sessions in Orca's native terminal split. Claude Code shows the bilingual usage notes. Codex's transcript shows the UTC and New York dates and four passing tests. That result was supplied to Claude Code when the notes were written.
- `editor-{light,dark}`: JavaScript date-formatting tests in the native editor.
- `diff-{light,dark}`: a separate, public input-validation example and two added tests. All six tests were run successfully after that change. It is not the unchanged four-test state shown in the earlier agent transcript.
- `files-{light,dark}`: native Markdown preview and the public repository tree. Office filenames are explicitly icon fixtures, not claims of working Office previews.

`*-large.png` files are lossless native-resolution exports. Preview PNGs only undergo proportional downsampling and metadata-free encoding. No text replacement, recoloring, generative retouching, blur or fake application controls are used.

## Cover and specimen sheets

`cover.png` places one intact native agent-workspace image inside a branded paper margin. Only the outside title, caption, frame and shadow are presentation design. Reproduce it with `scripts/media-cover.html` at 1600 × 1000.

`icons.png` and `icons-zh.png` are clearly labeled SVG specimen sheets, not Orca screenshots. `scripts/build-gallery.py` uses the shipped SVGs; render `docs/icons-gallery.svg` and `docs/icons-gallery-zh.svg` at 1600 × 1000. The website additionally displays true 16/20 px specimens.

The store uses five full-window scenes plus one clearly labeled icon specimen sheet: light Chat, dark agents, light/dark icon specimens, dark diff, light editor, dark files. The specimen sheet reuses `icons.png`; it is not a native window capture. The website offers all five scenes in both modes. Older terminal/individual-CLI image files and old composition scripts remain historical assets and are no longer linked from the current website or READMEs.

## Privacy and honest presentation

Never publish personal chats, real project names, account information, email addresses, device names, quota data or private filesystem paths. Use a disposable public workspace and review the final pixels before copying assets into Git. Public fixture paths are allowed. Do not publish a private screenshot and rely on CSS to hide part of it.

Chat、双智能体、编辑器和文件浏览的明暗截图均在同一公开演示环境中重拍，右侧文件树同时展示展开与收起的蜂蜜牛皮纸色文件夹。差异视图沿用展示源代码管理面板的原图。禁止公开个人聊天、真实项目、设备名、账户和额度；演示路径属于专门创建的公开内容。网页里的纸张动效不会改变插件本身的应用布局。

The identity asset is unchanged; see [IDENTITY.md](IDENTITY.md). App palette, ANSI palette, CLI syntax theme and each program's explicit truecolor are separate layers. A screenshot is evidence of its pictured configuration, not universal control over every CLI.

## Verification

Check actual image dimensions and PNG metadata with `node scripts/check-site.mjs`, validate the plugin, review light/dark captures, and exercise desktop/mobile, all scenes, keyboard paging, lightbox zoom, fast/slow image switching, no-JS and reduced-motion fallbacks. Store cover ≤1 MiB; each of up to six screenshots ≤1.5 MiB; gallery total ≤8 MiB.
