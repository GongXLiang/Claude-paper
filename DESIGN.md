# Current direction · 0.6.0

The whole real Orca workspace is the top sheet of a paper stack. Chat leads; native Claude Code + Codex split panes, diff, editor and files follow. Screenshots remain transform/filter-free at rest. The page retains the warm-paper and charcoal palette, with stronger entrances and a short desktop scroll sequence; manual input, reduced motion, mobile and no-JS take precedence.

Paper Fold 2 uses one slate folder, independent of its name. Files use family silhouettes, luminance-balanced color and individual suffix/name marks. Common formats are visually checked at 16/20 px. The active source is `scripts/build-icons.py`; old colored-folder aliases below are historical.

This version uses one bounded Opus 5.5 Medium consultation for visual direction and an independent implementation review. All product screenshots are genuine public native app captures. See [MEDIA.md](docs/MEDIA.md) for exact provenance and limits.

---

The sections below document previous versions, not current folder matching or page composition.

# 0.4.2 · Small-file recognizers / 小尺寸文件标记

15 个常用文件类型由角落叠加符号改为完整彩色纸页，纸页保留折角，识别符号居中。Python 使用清楚的 Py 与琥珀色折角，C++ 保留双加号；Word / Excel / PowerPoint 使用 W / X / P，PDF 使用字样，Notebook 使用叠放单元格，Docker 使用集装箱与船身。所有字形为原创路径，不依赖字体。文件夹和配色不变。

视觉验收查看 16 / 20 / 32 px 的明暗对照，而不只看放大的图鉴。SVG 仅含安全矢量形状。

# 0.4.1 · 通用目录与双语展示

用户确认保留纯主题方案：扩展通用名称，明确宿主边界，未知目录维持灰蓝图标。目录元数据统一存于 `icons/folders.json`，生成器、网页规则表共用同一份来源。现在为 16 类、118 个精确名称；图鉴按用途分类，不把 `raw` 和 `data` 写成路径。

Python、C、C++、Fortran、JavaScript、TypeScript 使用原创矢量字母标记；Notebook 保留笔记本和代码单元特征。全部 77 个 SVG 不依赖图标字体；512 条映射已到当前宿主上限，后续扩展应先合并无行为差异的重复项。

English and Chinese pages are generated from one template and parallel translation dictionaries. Both are complete static documents; the language link works without JavaScript. With enhancement, it carries the current scene and color mode. Public native screenshots remain in their original language; the SVG galleries, captions and runnable example guides are localized.

# 0.4.0：折纸虎鲸与文件分类

保留原有应用与终端颜色。69 个 SVG（39 个文件图标、30 个文件夹图标），423 条映射，14 类语义目录。未知目录改用灰蓝色；Word、Excel、PPT、PDF、SVG、HTML、Docker 等各有独立符号。新标识由 Opus 5.5 / medium 提供设计方向、GPT 生图工具生成。已检查 16px 文件图标及 32/64px 标识。下面保留此前版本的设计记录。

# Claude Paper 设计说明

## 0.3.0：完整工作场景与纸折图标

本版保持 0.2.1 的 66 个应用颜色令牌及既有语法配色。新增 Orca 1.4.255 支持的 7 个聊天细节令牌：粗体、次要文字、行内代码背景／文字、代码块背景、聊天选区背景／文字。终端增加 `cursorAccent`，原有背景、前景与 ANSI 颜色不变。

原创 Paper Fold 图标由纸页轮廓、折角与语义记号组成。51 个 SVG 包括 29 个文件图标和 22 个文件夹图标；后者包含通用目录与 10 类语义目录的关闭／展开态。355 条映射包括默认项、扩展名、具体文件名和目录名。使用单套图形适配浅深色，避免复制语言或厂商标志。

`scripts/build-icons.py` 生成图标和映射；`scripts/check-theme.py` 检查 SVG 元素、路径、数量、映射完整性与指定颜色组合。新增聊天文字／光标组合的最低对比度：暖纸 5.21:1、暖夜 4.56:1；图标主色在 8 种侧栏、内容、悬停和选中底色上的最低值 3.03:1。这些是指定组合的计算结果，不是所有语言与界面的无障碍认证。

宣传采用一张暖纸上的实际工作场景：聊天和输入框占封面主体，旁边是深色文件树与终端。其余六个展示场景通过网页标签访问；封面不再将同一段回复切成明暗两半。原生截图按区域裁切、等比缩小并拼版，具体处理见 [MEDIA](docs/MEDIA.md)。

设计方向经 Claude Opus 5.5 / medium 咨询；实现与验收独立进行。参考 Claude Theme for Orca 的场景优先信息层级，图标、页面与图像素材均独立制作。

### 当前宿主能力的选择

使用 [1.4.255 公开接口](https://github.com/stablyai/orca/blob/v1.4.255/docs/reference/plugin-themes.md)：应用主题、终端主题和文件图标，无执行入口与额外权限。当前宿主也支持可分发字体与背景资产；本版保留本机字体，围绕暖纸／暖夜完成统一，不附带字体或动态背景。布局、圆角、动效和工具栏按钮图标仍属于宿主。

Orca 的 **Match Claude Code to Terminal Theme** 是宿主可选功能，可根据终端色板生成 Claude Code 自身的颜色覆盖。本主题提供色板，不自动打开该开关。普通终端程序直接输出的 24 位真彩色不会由 ANSI 色板重新解释；演示中保留一行固定 `#D97757` 供对照。

以下保留第二版的配色决策与当时的验证记录；其中 1.4.253 的接口限制不代表当前 0.3.0 的能力。

---

## 历史版本 0.2.0：一张纸，两种光

第二版同时重做浅色与深色。目标是让长时间阅读、聊天与写代码更舒适：用明度区分区域，降低大面积填充的色度，把强调色留给有意义的动作。

## 配色结构

| 角色 | 暖纸 | 暖夜 |
| --- | --- | --- |
| 侧栏与标签栏 | `#F3F2EF` | `#201F1D` |
| 内容、编辑器、终端、活动标签 | `#F9F8F5` | `#2A2927` |
| 卡片 | `#FCFCFA` | `#2E2D2B` |
| 浮层 | `#FFFFFF` | `#33322F` |
| 正文 | `#1F1E1C` | `#EDEBE6` |
| 次要文字 | `#65625C` | `#B5B2AB` |
| 动作与焦点 | `#AC4B2B` | `#D97757` |
| 链接 | `#295E90` | `#8DB5E0` |

暖夜的应用背景是 `#201F1D`。Orca 1.4.253 把原生聊天画布抬亮，约为 `#2A2927`；因此编辑器、活动标签和终端明确设为该值。宿主以后若更改派生公式，应重新检查接缝。

侧栏 hover、选中项和分组条使用暖灰，替代初版的米棕与锈棕。细分隔线保留可见性；主按钮与焦点用陶土色，链接用蓝色，删除用玫红。Markdown 语法标题回归正文色加粗。关键字用紫、类型用青、常量用陶土，标点比变量安静一级。

终端 normal 与 bright 分开，选择区域用蓝色浅染。黑白 ANSI 色仍保留其语义，终端程序自行指定真彩色、低透明度或特殊背景时可能覆盖主题；不能据此声称所有终端程序均符合对比度标准。

## 设计咨询与执行

本版使用一次 Claude Opus 5.5 / medium 设计咨询，GPT-6 Astra 负责实现和独立验收。咨询提供配色方向与四套 JSON 建议；实施时依据未四舍五入的对比度数值，进一步调整了浅色陶土、浅色注释、两套删除字符强调底色和深色终端提示文字。

设计原则参考 [open-claude-ui](https://github.com/Caho1/open-claude-ui) 的[设计令牌研究](https://github.com/Caho1/open-claude-ui/blob/main/code-examples/cds-theme.css)。这是社区逆向研究，不能作为 Anthropic 官方规范。颜色针对 Orca 独立设计，未复制该项目组件、CSS、字体或二进制资产。

## 验证范围

在 Orca 1.4.253 上通过原生 `plugin validate` 与 `plugin check`，每套保留 66 个受支持的应用颜色令牌。

独立 sRGB / WCAG 计算通过 190 项检查。下表是被检查组合的最低值，非所有界面状态的无障碍认证；聊天和半透明控件仍会由宿主混合颜色。

| 检查组 | 暖纸最低 | 暖夜最低 |
| --- | --- | --- |
| 正文 / 所检查表面 | 12.59:1 | 9.84:1 |
| 次要文字 / 所检查表面 | 4.59:1 | 5.53:1 |
| 主按钮文字 / 90% hover 填充 | 4.57:1 | 4.90:1 |
| 语法文字 / 编辑器 | 4.51:1 | 4.93:1 |
| 增删文字 / 对应行、槽、字符强调底色 | 4.67:1 | 4.59:1 |

对比度数值向下截取两位小数。焦点检查阈值为 3:1；Git 文件状态为 3:1；终端 normal 彩色为 4.5:1，bright 彩色为 3:1。真实界面检查包括两种模式的聊天、设置、diff 与 ANSI 色样；普通 JSON 编辑器另在浅色模式检查。深色普通编辑页的截图被窗口切换打断，未将该截图作为验收证据；深色代码颜色已在 diff 中查看。没有穷举所有语言、弹窗、终端应用和显示器。

## 能力边界

使用 [Orca 1.4.253 主题接口](https://github.com/stablyai/orca/blob/v1.4.253/docs/reference/plugin-themes.md)，保持纯数据、无脚本、无额外能力权限。

- 通过颜色弱化分隔线，不改变边框的实际像素宽度。
- 字体、深色字重补偿、圆角、阴影、动效与启动防白闪由 Orca 宿主实现。
- 不写入当前版本不支持的新版聊天令牌。主题不能单独控制当前宿主的所有聊天标题、代码块或工具卡片颜色。
- 默认聊天跟随应用主题；若启用匹配终端外观，实际派生颜色可能不同。

后续调整先查看真实宿主效果，再改小范围颜色；发布新版本标签，不覆盖已发布标签。
