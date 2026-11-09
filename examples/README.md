# Date kit: a public theme demo

**English** · [简体中文](README.zh-CN.md) · [Theme README](../README.md)

One small task to preview code, chat, diffs and terminal output without private data. This guide and its Chinese counterpart describe the same example; they are not a new agent transcript.

## Example request

> Let formatDate use the local time zone by default, while keeping an explicit time-zone argument. Add tests around midnight.

## Behavior

`formatDate` uses native `Intl.DateTimeFormat`. Leaving out the second argument uses the runtime's local time zone. Pass an IANA time-zone name for an explicit result. There are no package dependencies.

```js
import { formatDate } from './date-kit/format.mjs';

const date = new Date('2026-11-09T23:30:00Z');
formatDate(date, 'UTC');            // 09 Nov 2026
formatDate(date, 'Asia/Shanghai');  // 10 Nov 2026
```

## Run the tests

From the repository root, with Node.js 18 or newer:

```sh
node --test examples/date-kit/format.test.mjs
```

The four tests cover explicit UTC, the local default, explicit override and calendar-day boundaries. Tests temporarily set the process time zone and restore it afterwards; they do not change the operating system time zone.

## Folder example

```text
demo/
  src/
  skills/
  plugins/
  data/
  output/
  my-project-notes/
```

The first five names have dedicated folder icons. `my-project-notes` is deliberately unmatched and uses the slate fallback. Folder matching is case-insensitive and exact: `DATA` also matches, but `project-data` does not. `raw` and `data` are separate supported names, not a single name or path.

[Full folder map](../icons/folders.json) · [Format implementation](date-kit/format.mjs)
