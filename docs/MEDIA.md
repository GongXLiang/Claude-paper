# 0.6.0 · Whole Orca, public workspaces / 完整原生工作区

All ten current scene images were recaptured on 2026-11-10 in an isolated Orca profile with a purpose-built `date-kit` repository. They use Orca 1.4.255, the unchanged Claude Paper app/terminal palettes and the new Paper Fold 2 icons.

## Capture and exports

- A real Electron window: **1440 × 900 logical pixels, DPR 2**. PNG masters are **2880 × 1800**; previews are **1600 × 1000**. No source crop is enlarged.
- The complete native renderer is preserved, including navigation, title/tab bars, content panes, right sidebar and status bar. No CLI panels are pasted together or redrawn. A public path such as `D:/paper-demo/date-kit` is intentional.
- `chat-{light,dark}`: genuine native Chat beside code, using Orca's native split. This layout also keeps the machine-name footer hidden through Orca's normal responsive UI. Messages use 16 px; code uses 13 px. The public reply accurately says that it read the files without running tests.
- `agents-{light,dark}`: actual Claude Code 2.1.322 and Codex CLI 0.167.0, simultaneously visible in native left/right terminal panes. IBM Plex Mono, 13 px; each pane has at least 60 columns. Claude Code used a user-configured provider alias; the client branding does not claim a particular underlying model. Codex used GPT-6-Astra. The original four tests passed; their result was passed back to Claude Code. No screenshots imply autonomous inter-agent messages.
- Claude Code used its terminal-aware Auto theme for these captures. Codex used the optional companion syntax theme for each mode and a temporary status-line override that omits account quotas. Running clients were resumed after a palette change.
- `editor-{light,dark}`: the original JavaScript test source in the native editor.
- `diff-{light,dark}`: a separate, public input-validation example and two added tests. All six tests were run successfully after that change. It is not the unchanged four-test state shown in the earlier agent transcript.
- `files-{light,dark}`: native Markdown preview and the public repository tree. Office filenames are explicitly icon fixtures, not claims of working Office previews.

`*-large.png` files are lossless native-resolution exports. Preview PNGs only undergo proportional downsampling and metadata-free encoding. No text replacement, recoloring, generative retouching, blur or fake application controls are used.

## Cover and specimen sheets

`cover.png` places one intact native agent-workspace image inside a branded paper margin. Only the outside title, caption, frame and shadow are presentation design. Reproduce it with `scripts/media-cover.html` at 1600 × 1000.

`icons.png` and `icons-zh.png` are clearly labeled SVG specimen sheets, not Orca screenshots. `scripts/build-gallery.py` uses the shipped SVGs; render `docs/icons-gallery.svg` and `docs/icons-gallery-zh.svg` at 1600 × 1000. The website additionally displays true 16/20 px specimens.

The store uses five full-window scenes plus one clearly labeled icon specimen sheet: light Chat, dark agents, light/dark icon specimens, dark diff, light editor, dark files. The specimen sheet reuses `icons.png`; it is not a native window capture. The website offers all five scenes in both modes. Older terminal/individual-CLI image files and old composition scripts remain historical assets and are no longer linked from the current website or READMEs.

## Privacy and honest presentation

Never publish personal chats, real project names, account information, email addresses, device names, quota data or private filesystem paths. Use a disposable public workspace and review the final pixels before copying assets into Git. Public fixture paths are allowed. Do not publish a private screenshot and rely on CSS to hide part of it.

本版在独立配置中真实拍摄完整 Orca 窗口；Chat、同屏双 Agent、差异、编辑器、文件浏览均有明暗两套。禁止公开个人聊天、真实项目、设备名、账户和额度；演示路径属于专门创建的公开内容。网页里的纸张动效不会改变插件本身的应用布局。

The identity asset is unchanged; see [IDENTITY.md](IDENTITY.md). App palette, ANSI palette, CLI syntax theme and each program's explicit truecolor are separate layers. A screenshot is evidence of its pictured configuration, not universal control over every CLI.

## Verification

Check actual image dimensions and PNG metadata with `node scripts/check-site.mjs`, validate the plugin, review light/dark captures, and exercise desktop/mobile, all scenes, keyboard paging, lightbox zoom, fast/slow image switching, no-JS and reduced-motion fallbacks. Store cover ≤1 MiB; each of up to six screenshots ≤1.5 MiB; gallery total ≤8 MiB.
