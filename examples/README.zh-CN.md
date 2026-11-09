# Date kit：公开主题演示

[English](README.md) · **简体中文** · [主题 README](../README.zh-CN.md)

用一个简单任务展示代码、聊天、差异与终端，避免引入私人数据。本指南与英文版描述同一个示例，并非新增的智能体聊天实录。

## 示例请求

> 让 formatDate 默认使用本地时区，同时保留显式时区参数，并补充跨午夜的测试。

## 行为说明

`formatDate` 使用原生 `Intl.DateTimeFormat`。省略第二个参数时使用运行环境的本地时区；传入 IANA 时区名称可得到明确的指定时区结果，无需安装第三方依赖。

```js
import { formatDate } from './date-kit/format.mjs';

const date = new Date('2026-11-09T23:30:00Z');
formatDate(date, 'UTC');            // 09 Nov 2026
formatDate(date, 'Asia/Shanghai');  // 10 Nov 2026
```

## 运行测试

在仓库根目录运行，需要 Node.js 18 或更新版本：

```sh
node --test examples/date-kit/format.test.mjs
```

四项测试覆盖显式 UTC、本地默认值、显式参数覆盖和跨日期边界。测试会临时设置当前进程的时区并在结束后恢复，不改变操作系统时区。

## 目录示例

```text
demo/
  src/
  skills/
  plugins/
  data/
  output/
  my-project-notes/
```

前五个名称具有专属目录图标。`my-project-notes` 故意使用未收录名称，显示灰蓝色默认图标。匹配精确且不区分大小写：`DATA` 也能匹配，`project-data` 则不能。`raw` 和 `data` 是两个独立的受支持名称，并非单个名称或路径。

[完整目录映射](../icons/folders.json) · [函数实现](date-kit/format.mjs)
