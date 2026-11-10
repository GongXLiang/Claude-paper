# Codex CLI 配套主题

[English](README.md) · **简体中文**

暖纸、暖夜两套可选语法主题，与 Claude Paper 编辑器共用色板，作用于 Codex CLI 的代码块和文件差异。终端负责基础色板，CLI 自己控制布局、消息样式和硬编码真彩色。

## 安装

下载或克隆 **Claude Paper 仓库**后，在仓库根目录运行：

```sh
node scripts/install-codex.mjs --dry-run
node scripts/install-codex.mjs
```

脚本仅复制 `claude-paper-light.tmTheme` 和 `claude-paper-dark.tmTheme` 到 `$CODEX_HOME/themes`；未设置 `CODEX_HOME` 时使用 `~/.codex/themes`。不修改 `config.toml`，不覆盖内容不同的文件，不安装依赖。也可用 `--destination /your/path` 指定主题目录。

在 Codex CLI 输入 `/theme`，搜索 **claude-paper**，选择与终端一致的 light 或 dark；选择由 Codex 自己保存。语法主题不会自动跟随 Orca 切换。如果运行中的 CLI 在换色后保留了旧消息底色，可退出并恢复该会话，让它重新识别终端背景。

仅安装 Orca 插件不会自动安装这些配套文件。已在 Windows、Orca 1.4.255、Codex CLI 0.167.0 验证。

## 移除

先用 `/theme` 选择其他主题，再仅删除自己安装的这两个文件，保留其他主题。

由 `python scripts/build-codex.py` 从 `themes/light.json` 和 `themes/dark.json` 生成。[Codex 官方定制说明](https://learn.chatgpt.com/docs/cli-customization)。
