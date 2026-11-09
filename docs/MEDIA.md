# 0.4.1 · Bilingual icon galleries / 双语图鉴

`assets/icons.png` (English) and `assets/icons-zh.png` (中文) render the actual 0.4.1 SVGs, including distinct programming-language marks and general folder categories. Generate the source SVGs with `python scripts/build-gallery.py`, then rasterize with resvg. On this Windows build, Microsoft YaHei regular was supplied to the renderer to keep Chinese glyph weights consistent; no font file is distributed.

文件夹标签表示用途分类；匹配仍由 Orca 按自身名称执行。`raw` 与 `data` 是独立别名，宣传图不再将其写为路径。新图鉴不是实机截图；原生场景保持原图与原文，中英文网页分别提供说明和图注。所有新增素材只含公开示例。

# 0.4.0 asset update

`assets/icon.png` is the GPT-generated Paper Orca mark, downsampled to 256 px. `assets/identity-master.png` preserves the generated master. The built-in tool does not expose a model version selector. See `IDENTITY.md` for the exact prompt.

`assets/icons.png` replaces the older native file-tree image with a labeled gallery rendered directly from original plugin SVGs; source: `icons-gallery.svg`. It is not a screenshot. All other scene images remain the documented 0.3.0 native captures; their app/terminal colors are unchanged in 0.4.0. No private images were added.

# 宣传素材与网页维护

展示页为 `index.html`、`style.css` 与 `app.js`，零依赖，无远程字体、分析脚本或构建步骤。GitHub Pages 从 `main:/docs` 发布。主题运行时不执行网页脚本。

## 0.3.0 素材

共 **11 张 1600×1000 场景 PNG**，另有一张 **256×256 插件图标**。场景来自 Orca 1.4.255 / Claude Paper 0.3.0 的原生界面；原始整窗捕获为 2586×1880 像素，沿用本机 91% UI 缩放。没有宣称按逻辑 1280×800 / 200% 采集。

| 文件 | 内容与处理 |
| --- | --- |
| `cover.png` | 浅色聊天为主，深色原生文件树及终端为辅的三区域拼版 |
| `chat-light.png` / `chat-dark.png` | 同一公开回复与输入框；裁去上方更早回复和下方设备信息，保留原生标签栏；文件树分别裁切后按列拼版 |
| `editor-light.png` / `editor-dark.png` | 原生 JavaScript 测试代码与文件树；去除绝对路径栏，保留标签栏 |
| `diff-light.png` / `diff-dark.png` | 原生 format.js 差异、同任务真实测试输出和文件树三部分拼版，不代表新增的固定布局 |
| `terminal-light.png` / `terminal-dark.png` | 原生终端标签与实际输出，裁去外围栏和无关留白 |
| `icons.png` | 同一文件树的两种模式并排展示 |
| `cli-compare.png` | 相同输出在 Ghostty Default Style Dark 与 Claude Paper 暖夜色板中的原生捕获；不是 Claude Code CLI 界面 |
| `icon.png` | 原创纸页与陶土折角的插件标识，源文件为 `icon.svg` |

商店使用封面与六图：暖纸聊天、暖夜差异、暖纸编辑器、暖夜终端、双模式图标、CLI 色板对照。网页另提供另外四张明暗场景。

图片内的界面文字、图标和颜色均来自真实捕获。每个区域只做裁切与等比缩小，没有放大、生成式重绘、替换文字、补画按钮或调色。外部标题、说明、底板与阴影是宣传排版。聊天代码块与编辑器使用各自宿主渲染器，不能把两者的高亮差别当成截图错误。字体与字号由本机设置决定，不随主题分发。

## 公开演示

独立 `date-kit` 项目，任务是让日期格式化默认使用本地时区，并保留显式时区参数。截图中的 `npm test` 已实际执行，4 项测试通过；Git 状态反映真实的三个文件修改。

终端色样使用 SGR 30–37、90–97 以及 `38;2;217;119;87`。两张 CLI 对照从同一段终端输出切换色板采集，没有重新运行以改变时长。光标闪烁时相可能不同。图中提示文字不等于已逐项验证所有光标样式；`cursorAccent` 的检查是颜色对比度计算。

## 隐私与复现

公开图片不得包含私人聊天、项目列表、用户名、邮箱、设备名、账户、用量、绝对路径或任务标识。必须使用独立公开演示内容；原始整窗截图与咨询记录仅留在本地，不能提交到 Git。

`scripts/media-studio.html` 保存本版的区域坐标与排版源码。将原生截图放在仓库外的私有目录，文件名为 `p03-chat-light-raw.png` 等；以本地浏览器打开模板，使用 `?scene=cover&raw=file:///your-private-capture-directory/`。页面加载完成时 `html[data-ready=true]`；固定视口 1600×1000 后导出整个页面。不要把含本机路径的 URL 写入仓库。新版宿主、窗口尺寸或缩放改变后必须重新检查坐标。

只有最终独立 PNG 能进入 `assets/`；不得发布原始截图，再依靠网页 CSS 隐藏私人区域。逐张查看最终图片的像素和边缘，检查 PNG 元数据。

## 检查

```sh
python scripts/check-theme.py
node scripts/check-site.mjs
node --check docs/app.js
orca plugin validate . --json
orca plugin check . --json
```

另用浏览器查看 360px 与桌面宽度、两种模式、全部场景、键盘标签切换、灯箱 Escape 与焦点返回、复制成功／失败提示、减少动态效果，以及不执行 JavaScript 时的图片和安装链接。

商店限额：封面至少 800×500、≤1 MiB；截图最多六张、每张至少 1280×800、≤1.5 MiB，合计≤8 MiB。插件标识至少128×128、≤256 KiB。页面默认静态展示，不自动播放；仅有 180ms hover 过渡，尊重减少动态效果设置。
