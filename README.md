# Claude Paper for Orca

[English](#english) · [设计说明](DESIGN.md) · [开发与发布](DEVELOPMENT.md)

为 Orca 提供 Claude 风格的暖纸浅色与暖夜深色配色，覆盖应用界面、原生聊天、代码编辑器与终端。保留 Orca 的原生布局、字体设置和工具卡片。

**非官方社区主题，与 Anthropic 或 Stably 无隶属或背书关系。** 免费使用，MIT 许可。

| 主题 | 风格 |
| --- | --- |
| Claude Paper · 暖纸 | 中性暖白纸面、细腻灰阶、陶土动作色与墨蓝链接 |
| Claude Paper · 暖夜 | 暖炭灰层次、柔和浅灰文字、陶土动作色与雾蓝链接 |

## 第二版 · 0.2.0

浅色与深色同时重新配色：减少棕黄色块，以细小明度差区分侧栏、内容、卡片和浮层。链接使用蓝色，标题回归正文色，代码标点与变量分层；终端提供可区分的 normal / bright 颜色。详见[设计说明](DESIGN.md)。

## 安装

需要 **Orca 1.4.253 或更新版本**。

```sh
orca plugin install GongXLiang/Claude-paper --json
```

安装后打开 **设置 → 外观**，选择浅色主题「Claude Paper · 暖纸」、深色主题「Claude Paper · 暖夜」。终端主题可分别选择同名项目。

在 **设置 → 聊天界面** 中，关闭「匹配终端外观」可让聊天跟随应用主题；若开启，请同时选择匹配的终端配色。字体、字号和聊天宽度仍使用你自己的 Orca 设置。

[Orca 插件页面与收录状态](https://www.onorca.dev/plugins/GongXLiang/Claude-paper) · [GitHub Releases](https://github.com/GongXLiang/Claude-paper/releases)

商店收录由 Orca 的自动检查决定；GitHub 发布成功不等于商店已经完成收录。

## 覆盖范围

- 两套应用主题，每套设置 66 个公开颜色令牌。
- 左右侧栏、标签页、菜单、按钮、用户消息、链接与 Git/diff 配色。
- 编辑器语法高亮，以及两套匹配的终端 ANSI 配色。
- 纯数据插件：没有运行脚本、网络请求、后台进程或额外能力权限。

本插件只修改公开颜色接口。字体、圆角、阴影、布局、工具卡片渲染和欢迎页动画不在其范围内。宿主信任与审批对话框由 Orca 自己控制。

## 卸载

在 **设置 → 插件** 找到 Claude Paper 并卸载，或先运行以下命令获取确切的插件标识：

```sh
orca plugin list --json
orca plugin uninstall <pluginKey> --json
```

卸载前可先在外观设置中切换到其他应用和终端主题。

## 验证

0.2.0 在 Orca 1.4.253 上通过 `plugin validate`、`plugin check` 与 190 项独立对比度检查。两套模式均已查看实际聊天、设置、diff 与 ANSI 终端色样，浅色另检查了普通 JSON 编辑器。未穷举所有语言与终端程序；具体范围见 [DESIGN.md](DESIGN.md)。

## 致谢

第二版的层次、品牌色与功能色分工参考 [open-claude-ui](https://github.com/Caho1/open-claude-ui) 的社区研究，具体颜色针对 Orca 独立调整；未引入其组件、CSS、字体或动效代码。

初版视觉方向参考 [HwFee 的 DSH CDS 主题](https://github.com/HwFee/HwFee-dsh/tree/master/plugins/cds-theme)，基于 [Orca 的公开主题接口](https://github.com/stablyai/orca/blob/v1.4.253/docs/reference/plugin-themes.md) 独立实现。本仓库未包含 DSH 的代码、字体资产或 Anthropic 商业字体。

## English

Claude-inspired warm light and dark color themes for Orca, covering the application, native chat, code editor, and terminal. Native layouts, typography settings, and tool-card behavior stay intact.

Requires **Orca >=1.4.253**. Install:

```sh
orca plugin install GongXLiang/Claude-paper --json
```

Select **Claude Paper · 暖纸** for the light app theme and **Claude Paper · 暖夜** for the dark app theme under Settings → Appearance. Matching terminal palettes are provided separately.

This is a **content-only** plugin: no runtime code, network requests, or extra capabilities. It cannot replace Orca's layouts, fonts, radii, or tool renderers. Version 0.2.0 passed Orca validation and 190 contrast checks. Both modes were visually checked in native chat, settings, diffs and an ANSI terminal sample; the regular JSON editor was also checked in light mode. This is not exhaustive testing of every language or terminal application.

Unofficial community project; not affiliated with or endorsed by Anthropic or Stably. Free under the [MIT license](LICENSE).
