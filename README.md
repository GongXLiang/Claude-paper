<p align="center"><a href="https://gongxliang.github.io/Claude-paper/"><img src="docs/assets/cover.png" alt="Claude Paper：浅色 Orca 原生聊天与输入框，搭配深色纸折文件图标和终端输出" width="100%"></a></p>

<p align="center"><img src="docs/assets/icon.png" width="96" height="96" alt="Claude Paper 折纸虎鲸标识"></p>

<h1 align="center">Claude Paper for Orca</h1>
<p align="center"><b>一张纸，两种光。</b><br>Warm light &amp; dark. Chat, code, terminal and original Paper Fold icons.</p>
<p align="center"><a href="https://gongxliang.github.io/Claude-paper/">查看全部实机效果</a> · <a href="https://www.onorca.dev/plugins/gongxliang/claude-paper">Orca 社区商店</a> · <a href="#安装">安装</a> · <a href="#english">English</a></p>

让 Orca 更接近你喜欢的 Claude 质感。暖白与暖炭灰构成安静的底色，陶土强调动作，蓝色标记链接。把对话、代码、差异、终端与文件树，放进同一套视觉语言。

| 暖纸与暖夜 | 纸折图标 | 配套终端 |
| --- | --- | --- |
| 两套应用主题，73 个色彩令牌 | 69 个原创 SVG，423 条映射 | 两套 16 色 ANSI 色板 |
| 聊天、侧栏、编辑器与 Diff | 文件类型、常用文件名、14 类语义目录及展开态 | 前景、背景、光标、光标下文字与选区 |

**0.4.0 · 免费 · MIT · 纯数据插件**。非官方社区作品，与 Anthropic 或 Stably 无隶属或背书关系。

## 安装

需要 **Orca 1.4.255+**。可从[社区商店](https://www.onorca.dev/plugins/gongxliang/claude-paper)安装，或运行：

```sh
orca plugin install GongXLiang/Claude-paper --json
```

在 **设置 → 外观** 中完成三项选择：

1. 应用浅色主题选 **Claude Paper · 暖纸**，深色主题选 **Claude Paper · 暖夜**。
2. 终端主题选择同名配色，或使用应用主题下的「使用其终端配色」。
3. 图标主题选 **Claude Paper · 纸折图标**。

在 **设置 → 聊天界面** 中关闭「匹配终端外观」，可使用独立的聊天细节色；开启时，聊天采用终端的配色与字体。

**使用 Claude Code CLI？** Orca 的终端主题设置还提供 **Match Claude Code to Terminal Theme**。这是宿主的可选同步功能，会修改本机 Claude Code 的主题设置，使其界面跟随所选终端色板；插件安装本身不会打开它。详见[Orca 的同步实现](https://github.com/stablyai/orca/blob/v1.4.255/src/main/claude/theme-sync/claude-code-theme.ts)。

## 对话，有了温度

完整的公开任务、原生回复和输入框，连同文件树一起展示。浅色与深色使用同一段演示内容；正文、行内代码、链接和代码块各有清楚的层次。

![暖纸模式：Orca 原生聊天、完整回复、输入框与纸折文件图标](docs/assets/chat-light.png)

<details><summary>展开暖夜聊天</summary>

![暖夜模式下同一段原生聊天与输入框](docs/assets/chat-dark.png)

</details>

## 从代码，到每一行改动

保留熟悉的原生编辑器，让语法、注释、增加与删除各自清楚。下方差异图同时展示该任务真实执行的测试输出。

| 暖纸 · 编辑器 | 暖夜 · 差异与测试 |
| --- | --- |
| [![暖纸 JavaScript 编辑器与文件树](docs/assets/editor-light.png)](docs/assets/editor-light.png) | [![暖夜原生代码差异、测试输出与文件树拼版](docs/assets/diff-dark.png)](docs/assets/diff-dark.png) |

[查看暖夜代码](docs/assets/editor-dark.png) · [查看暖纸差异](docs/assets/diff-light.png)

## 文件，也有自己的形状

原创 **Paper Fold 纸折图标**：纸页轮廓、折角与大号语义符号。代码、文档、测试、配置、图片和智能体文件各有记号；文件夹具有对应的关闭与展开图标。同一套 SVG 适配两种模式，不借用品牌标志。

![0.4.0 原始 SVG 图鉴：文件类型与文件夹的明暗对照](docs/assets/icons.png)

新版图鉴直接渲染插件 SVG，并非 Orca 窗口截图。Word、Excel、PPT、PDF、SVG、HTML、Docker 现在各有独立符号；未知文件夹使用灰蓝色，skills、references、graphify、raw 等目录也有专属图标。

覆盖常见扩展名，以及 `README.md`、`AGENTS.md`、`package.json` 等文件名。`d.ts`、`test.ts`、`config.ts` 使用更具体的映射；未匹配的文件与目录仍有通用图标。[查看完整映射](icons/theme.json)

## 命令行，也在同一张纸上

两套终端色板与应用画布协调，普通／高亮 ANSI 颜色分别设置。下面是实际运行的 `npm test`、Git 状态与色样；演示项目的 4 项测试通过。

![暖夜终端：公开项目的真实命令、测试结果与 ANSI 色样](docs/assets/terminal-dark.png)

[查看暖纸终端](docs/assets/terminal-light.png)

### 颜色能改变什么？

同一终端输出，左侧是 **Ghostty Default Style Dark**，右侧是 **Claude Paper · 暖夜**。ANSI 颜色跟随色板，`Truecolor #D97757` 一行保持程序指定的颜色。这是原生终端对照，并非 Claude Code CLI 的界面截图。

![两套终端色板的真实对照：ANSI 变化，24 位真彩色不变](docs/assets/cli-compare.png)

| 范围 | Claude Paper 的作用 |
| --- | --- |
| 应用、聊天、编辑器、Diff | 73 个公开颜色令牌与语法配色 |
| 文件与目录 | 原创纸折图标、文件名与后缀匹配、文件夹展开态 |
| 终端 | 背景、前景、光标、选区、16 色 ANSI |
| CLI 硬编码的 24 位真彩色 | 单靠终端色板不改写；Claude Code 可另用 Orca 的宿主同步功能 |
| 布局、圆角、动效、按钮图标 | 由 Orca 控制 |
| 字体与字号 | 本插件不附带字体，沿用 Orca 与使用者设置 |

主题是纯数据内容，没有入口脚本、后台进程或额外能力权限。展示网页的标签切换、灯箱与轻微过渡只属于网页。

## 关于图片与这一版

图片来自 **Orca 1.4.255 / Claude Paper 0.3.0** 的公开 `date-kit` 演示。仅做区域裁切、等比缩小与外部拼版；没有生成式重绘，也没有替换界面文字。聊天保留完整回复与输入框，编辑器路径栏、机器名、账号、私人项目与用量信息均未进入公开图片。[素材与复现说明](docs/MEDIA.md)

0.3.0 保留第二版的原有配色，加入 7 个当前宿主支持的聊天细节令牌、光标下文字颜色、纸折图标及独立插件图标。封面、六张商店图片和网页一起重做；网页提供十张场景图，可按场景与明暗模式浏览。

[设计说明](DESIGN.md) · [开发与发布](DEVELOPMENT.md) · [更新记录](CHANGELOG.md) · [版本下载](https://github.com/GongXLiang/Claude-paper/releases)

商店按版本标签异步索引，可能晚于 GitHub 发布；以[商店实际显示](https://www.onorca.dev/plugins/gongxliang/claude-paper)为准。

## 致谢

- [Monospace Icons for Orca](https://github.com/faisalmuhammad/orca-monospace-icons)：文件类型细分思路参考；未复制其 SVG。

- [open-claude-ui](https://github.com/Caho1/open-claude-ui)：层次与克制用色的社区研究。
- [HwFee DSH CDS theme](https://github.com/HwFee/HwFee-dsh/tree/master/plugins/cds-theme)：初版视觉方向的参考。
- [Claude Theme for Orca](https://github.com/jiangwanyutao/orca-claude-theme)：以实际工作场景介绍主题的展示思路。
- [Orca 主题规范](https://github.com/stablyai/orca/blob/v1.4.255/docs/reference/plugin-themes.md)：本插件使用的公开接口。

配色、图标与页面独立实现；未复制上述项目的主题代码、SVG、截图、组件或字体资产。

## English

Claude Paper brings a coherent, Claude-inspired palette to Orca: warm light and charcoal dark themes for chat, code, diffs and terminal, plus original **Paper Fold file icons**. It includes 2 app themes, 2 terminal palettes and 1 icon family with 69 SVGs and 423 mappings.

Requires **Orca 1.4.255+**. Install with `orca plugin install GongXLiang/Claude-paper --json`, then select **Claude Paper · 暖纸** for light mode, **Claude Paper · 暖夜** for dark mode, the matching terminal palettes, and **Claude Paper · 纸折图标** in Settings → Appearance.

[Explore all scenes](https://gongxliang.github.io/Claude-paper/). Images are cropped, downscaled native Orca captures of a public demo, composed into presentation frames. No private chats, account information or local paths are published. The CLI comparison shows terminal palettes, not a Claude Code CLI screenshot. Hardcoded truecolor remains program-controlled; Orca's optional Claude Code theme sync is a separate host setting.

A data-only community plugin. Native layouts, animations and controls remain Orca's; fonts follow your settings. Unofficial, not affiliated with or endorsed by Anthropic or Stably. [MIT licensed](LICENSE).
