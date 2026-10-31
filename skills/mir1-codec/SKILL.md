---
name: mir1-codec
description: "MIR/1 符号语编解码。把中文/粤语拼音或任意拉丁文本编译成 MIR 字形（ᚾᛁ3·ᛗ∃ᚾ0），以及把字形反编译回拼音。用于 cipher.room 等场景的机器可读消息。关键词：MIR、字形、符号语、拼音加密、编译、反编译、encode、decode、ᛁ、∀、§MIR"
version: "1.1.0"
author: "CodeBuddy AI"
created: "2026-10-31"
updated: "2026-10-31"
---

# MIR/1 Codec

> **Goal**：把拉丁文本（拼音/英文）编译成 MIR 字形，把 MIR 字形反编译回拉丁文本。零依赖，一个 Python 文件。

## 何时使用

- 用户要求「用 MIR 语发」「编译成符号」「反编译这段符号」
- 出现 `§MIR/1` 开头的文本，需要解码
- 出现 `ᚾ ᛁ ᛗ ∟ ∀ ∃ ∫ ⊙` 等混合符号，需要还原

## 三种用法

### 1. 跑脚本（首选，准确）

```bash
python3 ~/.codebuddy/skills/mir1-codec/scripts/mir1.py enc "ni3·men0·jiao1·wo3"
python3 ~/.codebuddy/skills/mir1-codec/scripts/mir1.py enc --wrap --lang cmn "ni3·men0"
python3 ~/.codebuddy/skills/mir1-codec/scripts/mir1.py dec "ᚾᛁ3·ᛗ∃ᚾ0"
python3 ~/.codebuddy/skills/mir1-codec/scripts/mir1.py table
python3 ~/.codebuddy/skills/mir1-codec/scripts/mir1.py selftest
```

参数说明：

| 参数 | 作用 |
|---|---|
| `enc` / `encode` | 编译。拉丁 → 字形 |
| `dec` / `decode` | 反编译。字形 → 拉丁 |
| `--wrap` | 封装协议头 `§MIR/1⟨...⟩` |
| `--script` | `pinyin`（普通话）或 `jyutping`（粤拼） |
| `--lang` | `cmn` 或 `yue` |
| `--num` | `plain`（默认）数字明文；`glyph` 数字也换字形 |
| `table` | 打印 26 字母与 10 数字对照表 |
| `selftest` | 往返自测 |

文本可放在任意位置（脚本用 `parse_known_args` 兜底）。

### 2. 手动查表（脚本不可用时）

按下方对照表逐字母替换。数字与标点不替换。

| 字母 | 字形 | 字母 | 字形 | 字母 | 字形 |
|---|---|---|---|---|---|
| A | ∀ | J | ᛃ | S | ∫ |
| B | ᛒ | K | ᚲ | T | ⊤ |
| C | ⊂ | L | ∟ | U | ∪ |
| D | ᛞ | M | ᛗ | V | ∨ |
| E | ∃ | N | ᚾ | W | ᚹ |
| F | ᚠ | O | ⊙ | X | ⊗ |
| G | ᚷ | P | ᛈ | Y | ⅄ |
| H | ᚺ | Q | Ϙ | Z | ᛉ |
| I | ᛁ | R | ᚱ | | |

数字表（`--num glyph` 时启用）：

| 数字 | 字形 | 数字 | 字形 | 数字 | 字形 |
|---|---|---|---|---|---|
| 0 | ⊘ | 4 | ◇ | 8 | ◧ |
| 1 | ⌐ | 5 | ◆ | 9 | ◨ |
| 2 | ◭ | 6 | ○ | | |
| 3 | ◮ | 7 | ● | | |

配对逻辑：2/3 上下，4/5 白黑菱，6/7 白黑圆，8/9 左右半方。

算法：

```
encode: 对输入每个字符 c：查 GLYPHS[c.upper()]，命中则替换，否则原样保留
decode: 对输入每个字符 c：查 REV[c]，命中则替换，否则原样保留
```

### 3. 分发给其他 AI

把 `references/agent-prompt.md` 的全文粘贴给任意 AI。它读完后即具备编解码能力，不需要脚本、不需要网络。

## 语音转写规则

中文/粤语要先转拼音，再编译：

| 步 | 规则 |
|---|---|
| 1 | 中文用汉语拼音，粤语用粤拼 Jyutping |
| 2 | 声调转数字。普通话 1–4，轻声 0；粤语 1–6 |
| 3 | 音节间用 `·` 分隔 |
| 4 | 逐字母换字形，数字标点不动 |
| 5 | 封装时标注 `script` 与 `lang` |

完整规格见 `references/spec.md`。

## 已知限制

| 限制 | 说明 |
|---|---|
| 有损 | 只传音节不传汉字。反编译后得到拼音，同音字靠上下文猜 |
| 无大小写 | 编译后大小写信息丢失。反编译输出为大写 |
| 非加密 | 这是替换密码，拿到对照表即可解。不是保密手段 |
| 字体依赖 | 15 个字形来自如尼文区块。缺字体的设备显示为方块 □ |
| 形近风险 | `⊙`(O) 与 `○`(6)、`●`(7) 形状接近。靠码点区分，肉眼易混 |

## 示例

```
输入   ni3·men0·jiao1·wo3
编译   ᚾᛁ3·ᛗ∃ᚾ0·ᛃᛁ∀⊙1·ᚹ⊙3
反编译 NI3·MEN0·JIAO1·WO3
```
