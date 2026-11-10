# Development quick start / 双语展示维护

The plugin root is this repository. It is a data-only theme; do not patch Orca resources or add unsupported theme fields. Source files:

- `icons/folders.json`: folder categories, bilingual labels and exact aliases. Expanded and closed mappings are generated together. All icon maps combined must stay at or below 512 entries (0.5.0 uses all 512).
- `scripts/build-icons.py`: original SVGs and the icon map. Inspect changed file recognizers at 16 and 20 px in both modes, not only in the 32 px gallery.
- `scripts/site-template.html` and `scripts/site-copy.json`: one page template and complete English/Chinese strings; `scripts/build-site.py` writes `docs/index.html` and `docs/zh-CN.html`.
- `scripts/build-gallery.py`: English/Chinese SVG gallery sources. Rasterize them to `docs/assets/icons.png` and `docs/assets/icons-zh.png` using resvg; inspect both images before publishing.
- `README.md`, `README.zh-CN.md`, `examples/README.md`, `examples/README.zh-CN.md`: keep content and commands equivalent.

```sh
python scripts/build-icons.py
python scripts/build-gallery.py
python scripts/build-site.py
python scripts/build-codex.py
python scripts/check-theme.py
python scripts/check-extras.py
node scripts/check-site.mjs
node --check docs/app.js
node --test examples/date-kit/format.test.mjs
orca plugin validate . --json
```

High-density chat exports use the optional `width=2560` compositor parameter. Keep the crop guard in output pixels, export into a private review directory first, and review the final pixels before adding PNGs to the repository.

For browser verification, evaluate `scripts/check-browser.js` on each language page. It checks gallery modes, keyboard tabs, labels, language URLs, overflow, the lightbox and copy feedback (clipboard calls are stubbed and restored). Also click the actual language link and check desktop/mobile appearance; test responsive mode after each navigation. The script changes only the preview page's controls and theme preference.

中文说明：修改通用目录请编辑 `icons/folders.json`；网页中英文文案编辑 `scripts/site-copy.json`，不要直接改生成的两个 HTML。发布前运行以上校验、检查双语图片与真实浏览器切换，再更新本地插件并发布新的版本标签。中英文示例应始终使用同一份公开代码，原生截图保持原文。

# 开发与发布

本文件用于后续人工或 AI（例如 Opus）维护。此仓库根目录就是插件根目录。

## 文件

- `orca-plugin.json`：插件清单、版本与兼容范围。
- `themes/light.json`、`themes/dark.json`：应用、聊天与编辑器颜色。
- `themes/terminal-light.json`、`themes/terminal-dark.json`：终端颜色。
- `icons/theme.json` 与 `icons/*.svg`：纸折图标及匹配规则。
- `scripts/build-icons.py`：图标生成器；修改后运行并检查实际文件树。
- `scripts/check-theme.py`：新增聊天、光标、图标对比度与 SVG 安全检查。
- `scripts/media-studio.html`：只读取外部私有截图的拼版模板。

## 修改原则

保留纯数据插件和原生布局。不要增加未公开的令牌，也不要修改 Orca 安装资源。
配色必须满足 Orca 的对比度要求，否则宿主可能丢弃该颜色并回退。
仅允许提交经过逐张隐私检查的公开演示截图；原始整窗截图、私人聊天、账号信息、绝对路径、缓存、压缩包或商业字体不得进入仓库。详见 [素材维护规则](docs/MEDIA.md)。

当前 `publisher` 字段按 Orca 1.4.255 的作者指南省略：Git 安装由仓库所有者派生身份，目录安装使用 `local`。不要为了旧网页示例随意添加发布者字段。

## 校验与预览

```sh
orca plugin validate . --json
orca plugin check . --json
orca plugin inspect . --json
orca plugin dev load . --json
```

开发加载后在设置中选择主题，保存 JSON 后检查实际应用、聊天、代码和终端。
本地开发身份通常是 `local.claude-paper`；Git 安装身份由仓库所有者派生。
结束预览：

```sh
orca plugin dev unload . --json
```

正式目录安装并不会自动跟随源码修改。改完后重新安装目录，或使用开发加载进行调试。

## 发布

先更新清单版本及 CHANGELOG，通过校验，确认只提交公开文件。提交后为该版本创建新的 `vX.Y.Z` tag 并推送。已发布 tag 不移动、不覆盖。

```sh
git add .
git commit -m "Describe the theme change"
git tag -a vX.Y.Z -m "Claude Paper vX.Y.Z"
git push origin main
git push origin vX.Y.Z
```

仓库保留 `orca-plugin` topic。Orca 从版本 tag 扫描，不会因为只推送 main 就更新商店。
在 [插件状态页](https://www.onorca.dev/plugins/GongXLiang/Claude-paper) 检查自动收录结果。

[官方发布说明](https://www.onorca.dev/plugins/add) · [主题规范](https://github.com/stablyai/orca/blob/main/docs/reference/plugin-themes.md) · [颜色令牌](https://github.com/stablyai/orca/blob/main/docs/reference/plugin-theme-tokens.md)

## 展示页与素材

网站位于 `docs/`，由 GitHub Pages 从 `main:/docs` 发布。图片位于 `docs/assets/`，由 README 和商店清单共同引用。网页交互脚本仅在访问网站时执行，不属于主题插件运行代码。

发布前运行 `python scripts/check-theme.py`、`node scripts/check-site.mjs` 和 `node --check docs/app.js`，然后检查手机/桌面效果与所有公开图片。更新版本标签后再检查商店索引结果。


## 0.5.0 additions / 配套主题与安装统计

- `scripts/build-codex.py` exports both `.tmTheme` files from the app's existing syntax tokens. `scripts/install-codex.mjs` is explicit opt-in; it never changes Codex configuration. `scripts/check-extras.py` checks palette parity, font signatures/license, statistics validation and installer conflict handling.
- `fonts/` contains unmodified OFL-licensed IBM Plex Mono faces and source hashes. Keep their license separate from the project's MIT license.
- `scripts/refresh-stats.py` reads the official public store stats, validates them and updates `docs/install-stats.json`. It retains the last valid snapshot if fetching fails, and rejects invalid or older data. Run `python scripts/build-site.py` after refreshing to update the no-JS fallback in both pages.
- `.github/workflows/install-stats.yml` refreshes twice daily and can be run manually. The source timestamp stays visible: counts are installations, not unique users or a live measurement. The workflow explicitly requests a Pages build after its own commit because a `GITHUB_TOKEN` push alone does not trigger a legacy Pages build.
- Page switches decode the next image before changing colors; controls respond immediately. Test rapid changes, failed/slow images, reduced motion, deep URLs, no-JS content, keyboard focus and 360 px layouts. `scripts/check-browser.js` covers both languages with 75 browser assertions; visual motion and native screenshots still need separate review.

中文：先运行最小有效校验，再做实机与网页验收。原生 CLI 演示不能用模拟输出替代。字体与 Codex 配套主题是本版新增能力；Claude Code 同步是 Orca 的既有可选功能，不应写成插件新增的宿主接口。

Evaluate scripts/check-motion.js in a visible Chromium page to check actual color/opacity frames, delayed decoding and Escape focus restoration. The 0.5.0 run sampled 80 frames and 27 intermediate background colors in isolated Edge; embedded automation views can throttle animation clocks. Also verified explicit dark first paint, no-JS dark/mobile fallback and reduced motion. These browser test helpers are development-only; the website remains dependency-free.
