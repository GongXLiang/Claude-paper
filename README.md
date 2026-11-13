# Claude Paper for Orca

Warm paper by day. Soft charcoal at night. One coherent space for Chat, coding agents and files.

**English** · [简体中文](README.zh-CN.md) · [Live preview](https://gongxliang.github.io/Claude-paper/) · [Orca community store](https://www.onorca.dev/plugins/gongxliang/claude-paper)

![Claude Paper: Claude Code and Codex together in a complete native Orca workspace](docs/assets/cover.png)

Two app themes, matching terminal palettes, **455 original file icons**, one quiet honey-kraft folder style, and optional IBM Plex Mono. An unofficial, data-only community theme; no extra capability permissions.

## Install

Requires **Orca 1.4.255+**. Install from the [community store](https://www.onorca.dev/plugins/gongxliang/claude-paper), or run:

```sh
orca plugin install GongXLiang/Claude-paper --json
```

In **Settings → Appearance**, choose **Claude Paper · 暖纸** for light, **Claude Paper · 暖夜** for dark, their matching terminal palettes, and **Claude Paper · 纸折图标** for file icons. IBM Plex Mono is an optional terminal/editor font selection; existing font choices remain yours.

For the independent Chat palette shown here, keep **Match Terminal Appearance** off. Turn it on if you prefer Chat to follow your terminal colors and font.

The [website](https://gongxliang.github.io/Claude-paper/#install) shows the official installation count and its source date. Counts are periodically refreshed installations, not live or unique users.

## Your conversation, in its workspace

[![Complete native Orca: public Chat, code and file tree in Warm Paper](docs/assets/chat-light.png)](docs/assets/chat-light-large.png)

[View Warm Night](docs/assets/chat-dark-large.png). Every scene retains the complete Orca frame. Click any image for a **2880 × 1800** native-resolution capture.

## Two agents. One Orca window.

[![Claude Code and Codex reviewing the same public date-kit task in native Orca split panes](docs/assets/agents-dark.png)](docs/assets/agents-dark-large.png)

[The same workspace in Warm Paper](docs/assets/agents-light-large.png).

These are genuine Claude Code and Codex CLI sessions in Orca's native left/right split. Claude Code reviews the example; Codex checks the date boundary and runs the tests; the verified result is handed back to Claude Code. The screenshot shows the completed public task, not a staged terminal drawing. Orchestration belongs to Orca and the agents; this plugin coordinates their visual surroundings.

- **Claude Code:** optionally enable **Match Claude Code to Terminal Theme** in Orca's Appearance settings. This host feature follows Orca's terminal palette and can also affect Claude Code outside Orca. Choosing another theme inside Claude Code stops the sync. Installing the plugin does not enable it. [Host implementation](https://github.com/stablyai/orca/blob/v1.4.255/src/main/claude/theme-sync/claude-code-theme.ts)
- **Codex CLI:** the [optional companion syntax themes](extras/codex/README.md) style code and diffs. Select `claude-paper-light` or `claude-paper-dark` with `/theme`; they do not automatically switch with Orca. A running CLI may need to be restarted/resumed when its terminal background changes.
- **Typography:** optional IBM Plex Mono, with system fallback for Chinese. [Font source and OFL license](fonts/README.md)

## Quiet folders. Distinct files.

All folder names now use the **same honey-kraft icon**, with separate closed/open states. A folder called `skills`, `src` or `my-notes` receives the same treatment. Color no longer competes with the files inside it.

![Paper Fold 2: selected original file icons and one uniform folder style in both modes](docs/assets/icons.png)

The sheet above renders the actual SVG assets. **340 suffixes + 115 exact filenames** each have a dedicated SVG. Shapes identify file families; color and small marks distinguish formats and variants. Python snakes, notebook cells, C/C++ hexagons, Office symbols, Markdown, JSON braces, YAML lines, TOML brackets, Git, Docker, shells, databases and media are all covered. Common configuration and tool files include `.gitignore`, `.env`, `package.json`, `Dockerfile`, `Cargo.toml` and `pyproject.toml`.

[Browse all 455 associations](icons/COVERAGE.md) · [Machine-readable catalogue](icons/catalogue.json) · [Native Orca file tree](docs/assets/files-dark-large.png)

Orca matches **exact filenames first, then the longest suffix**, case-insensitively. Thus `format.test.js` gets a test icon, `types.d.ts` a declaration icon, and ordinary `.js`/`.ts` files their language icons. Suffix variants such as `.yaml`/`.yml` retain a shared family but have distinct marks. Unlisted types use a neutral file icon; this is broad curated coverage, not a claim to recognize every possible extension. Ambiguous suffix choices are listed in the coverage document.

## Code and changes, in context

| Editor · Warm Paper | Diff · Warm Night |
| --- | --- |
| [![Native Orca JavaScript editor](docs/assets/editor-light.png)](docs/assets/editor-light-large.png) | [![Native Orca diff review](docs/assets/diff-dark.png)](docs/assets/diff-dark-large.png) |

[Dark editor](docs/assets/editor-dark-large.png) · [Light diff](docs/assets/diff-light-large.png) · [Files in Warm Paper](docs/assets/files-light-large.png)

## What the theme controls

| Area | Scope |
| --- | --- |
| App, Chat, editor and diffs | 73 supported color tokens and editor syntax colors |
| Files and folders | 455 file marks, a neutral fallback and uniform folder states; 458 icon mappings total |
| Terminal | Foreground, background, cursor, selection and 16 ANSI colors |
| CLI truecolor | A CLI's explicit 24-bit colors remain program-controlled; optional host/CLI integrations are separate |
| Font | Optional IBM Plex Mono; manually selected |
| Layout, app motion, settings switches and agent coordination | Orca and user settings control these |

The website's paper motion is a presentation feature, not an app animation added by the plugin. It respects reduced motion; touch devices use ordinary scrolling. Scene buttons and keyboard paging remain available.

## A public example, in two languages

[English walkthrough](examples/README.md) · [中文示例](examples/README.zh-CN.md)

> Use the local time zone by default; retain an explicit time-zone argument. / 默认使用本地时区，并保留显式时区参数。

```js
import { formatDate } from './examples/date-kit/format.mjs';
const date = new Date('2026-11-09T23:30:00Z');
formatDate(date, 'UTC');            // 09 Nov 2026
formatDate(date, 'Asia/Shanghai');  // 10 Nov 2026
```

All current scenes were recaptured in an isolated public demo profile on Orca 1.4.255. No personal chats, accounts, device names, quotas or private projects are published. The visible `D:/paper-demo/date-kit` path is a disposable public fixture. [Capture details](docs/MEDIA.md)

## Development and credits

[Development](DEVELOPMENT.md) · [Design history](DESIGN.md) · [Changelog](CHANGELOG.md) · [Releases](https://github.com/GongXLiang/Claude-paper/releases)

Theme code and file SVGs are original. Research references: [open-claude-ui](https://github.com/Caho1/open-claude-ui), [HwFee DSH CDS](https://github.com/HwFee/HwFee-dsh), [Claude Theme for Orca](https://github.com/jiangwanyutao/orca-claude-theme), [Monospace Icons](https://github.com/faisalmuhammad/orca-monospace-icons), [Orca Material Icons](https://github.com/stablyai/orca-plugins/tree/main/plugins/material-icons), [ThreeUI](https://github.com/MengTo/threeui), and [oil-ui](https://github.com/oil-oil/oil-ui). No third-party screenshots or SVGs were copied. The origami orca identity uses a GPT-generated image; see [identity provenance](docs/IDENTITY.md).

Plugin code is MIT. IBM Plex Mono retains its OFL license. The website vendors GSAP/ScrollTrigger under their [separate license notice](docs/vendor/NOTICE.txt). Unofficial; not affiliated with Anthropic or Stably. The community catalogue indexes version tags asynchronously and may lag behind GitHub.
