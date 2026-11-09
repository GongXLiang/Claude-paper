# 开发与发布

本文件用于后续人工或 AI（例如 Opus）维护。此仓库根目录就是插件根目录。

## 文件

- `orca-plugin.json`：插件清单、版本与兼容范围。
- `themes/light.json`、`themes/dark.json`：应用、聊天与编辑器颜色。
- `themes/terminal-light.json`、`themes/terminal-dark.json`：终端颜色。

## 修改原则

保留纯数据插件和原生布局。不要增加未公开的令牌，也不要修改 Orca 安装资源。
配色必须满足 Orca 的对比度要求，否则宿主可能丢弃该颜色并回退。
仅允许提交经过逐张隐私检查的公开演示截图；原始整窗截图、私人聊天、账号信息、绝对路径、缓存、压缩包或商业字体不得进入仓库。详见 [素材维护规则](docs/MEDIA.md)。

当前 `publisher` 字段按 Orca 1.4.253 的作者指南省略：Git 安装由仓库所有者派生身份，目录安装使用 `local`。不要为了旧网页示例随意添加发布者字段。

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

发布前运行 `node scripts/check-site.mjs` 和 `node --check docs/app.js`，然后检查手机/桌面效果与所有公开图片。更新版本标签后再检查商店索引结果。
