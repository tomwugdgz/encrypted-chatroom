# 加密聊天室（Encrypted Chatroom Demo）

一句话：一个**加密模拟器的 demo**。在端到端加密聊天室里，用一套自造的符号语（MIR/1）收发消息。

> ⚠️ **这不是加密。**
> MIR/1 是替换编码（substitution cipher），不是密码算法。拿到对照表的人几十秒就能解。
> 本项目的价值是演示「符号语怎么设计、怎么编译、怎么反编译、怎么让 AI 也学会」，不提供任何保密性。
> 真要保密，请用有密钥的成熟方案（Signal 协议、age、GPG 等）。

---
<img width="1293" height="1317" alt="image" src="https://github.com/user-attachments/assets/67a13e3a-cbcc-4d22-8d7f-488a8e5b913c" />


## 一、聊天室链接

示例房间（本项目演示时用的）：

```
https://ccd7856c.pinme.dev/#/r/jrdFEsX0u38HaVPj4wGOL5YIdmfgG2-AkRDHY0OB4NI
```

**这个链接可以自己去申请。** 已知事实：

| 项 | 说明 |
|---|---|
| 应用 | cipher.room，自称端到端加密聊天 |
| 托管 | pinme.dev 上的静态页（IPFS 网关形态） |
| 房间地址 | 形如 `https://<站点>/#/r/<房间ID>`，房间 ID 在 URL 的 hash 里 |
| 页面能力 | 有 `Copy invite link`（复制邀请链接）、`Leave`（离开）、可改昵称 |
| 身份 | 每次进房间随机生成一个 `#xxxx` 后缀，昵称可改，后缀不可改 |

新建房间的入口以该站点当前界面为准。本仓库没有官方文档可引用，未做核实。房间链接随时可能失效，别人的房间你拿着链接就能进。

---

## 二、快速开始

```bash
# 1. 编译：拉丁文本 -> MIR 字形
python3 scripts/mir1.py enc "wo3·bu4·shi4·ren2"
# ᚹ⊙3·ᛒ∪4·∫ᚺᛁ4·ᚱ∃ᚾ2

# 2. 数字也符号化
python3 scripts/mir1.py enc --num glyph "wo3·bu4·shi4·ren2"
# ᚹ⊙◮·ᛒ∪◇·∫ᚺᛁ◇·ᚱ∃ᚾ◭

# 3. 反编译
python3 scripts/mir1.py dec "ᚹ⊙◮·ᛒ∪◇·∫ᚺᛁ◇·ᚱ∃ᚾ◭"
# WO3·BU4·SHI4·REN2

# 4. 中文直接转（需要 pypinyin）
pip3 install -r requirements.txt
python3 tools/zh2mir.py --text "我不是人" --num glyph --verify

# 5. 打印对照表 / 自测
python3 scripts/mir1.py table
python3 scripts/mir1.py selftest
```

零依赖：`scripts/mir1.py` 只用 Python 标准库。只有中文转拼音需要 `pypinyin`。

---

## 三、目录结构

```
encrypted-chatroom/
├── README.md                     本文件
├── LICENSE                       MIT
├── requirements.txt              pypinyin（可选）
├── scripts/
│   └── mir1.py                   编解码主程序（零依赖）
├── tools/
│   ├── zh2mir.py                 中文 -> 拼音 -> 字形
│   └── send_to_room.js           浏览器自动发送到聊天室
├── docs/
│   ├── mir1-spec.md              MIR/1 完整规格 1.2
│   └── MIR1-AGENT-PROMPT.md      给 AI 的能力包（可粘贴）
├── skills/
│   └── mir1-codec/               CodeBuddy skill，可直接放进 ~/.codebuddy/skills/
│       ├── SKILL.md
│       ├── scripts/mir1.py
│       └── references/
├── examples/
│   └── tom-intro-mir.md          一次真实发送的完整记录
└── scripts/build.sh（见下）      打包 ZIP
```

---

## 四、MIR/1 是什么

三层结构：

| 层 | 做法 | 例 |
|---|---|---|
| 1. 拼音层 | 中文/粤语转拼音，声调转数字 | `wo3·bu4·shi4·ren2` |
| 2. 字形层 | 每个拉丁字母换一个符号 | `ᚹ⊙3·ᛒ∪4·∫ᚺᛁ4·ᚱ∃ᚾ2` |
| 3. 封装层 | 加协议头，注明方案与语言 | `§MIR/1⟨v:1.2|script:pinyin|lang:cmn|num:glyph⟩ …` |

26 个字母 + 10 个数字各有符号。数字默认明文（`num:plain`），`num:glyph` 时全符号化。

完整对照表见 [`docs/mir1-spec.md`](docs/mir1-spec.md)。

---

## 五、三种用法

| 方式 | 适合 |
|---|---|
| 跑 `scripts/mir1.py` | 准确、批量 |
| 查 `SKILL.md` 的手工表 | 手边没有 Python |
| 把 `docs/MIR1-AGENT-PROMPT.md` 粘给任意 AI | 让别的 AI 也会编解码 |

第三条是本项目的重点：**能力可以靠文本传播**。粘贴一份文件，对方 AI 立刻具备编解码能力，不需要装任何东西。文件里内置了验证样例，对方解错会立刻对不上。

---

## 六、加密方案可以自己用 AI 写

MIR/1 只是个示例。你可以让 AI 给你写一套自己的。提示词模板：

```
我要一套给 AI 读的符号语，要求：
1. 26 个字母 + 10 个数字各一个符号，符号要生僻、不用常见形状
2. 给出每个符号的 Unicode 码点
3. 给出编码与反编译的明确算法
4. 给 4 组验证样例，我用来检查你有没有抄错
5. 说明限制：哪些地方会丢信息

不要写成长篇解释，直接给表和算法。
```

拿到之后，用 [docs/MIR1-AGENT-PROMPT.md](docs/MIR1-AGENT-PROMPT.md) 的结构把它整理成能力包，就能分发给其他 AI。

---

## 七、已知限制

| 限制 | 说明 |
|---|---|
| 非加密 | 替换编码。对照表一旦公开，全部可逆 |
| 有损 | 只传音节不传汉字。反编译得到拼音，同音字靠猜 |
| 无大小写 | 编译后大小写丢失，反编译输出大写 |
| 字体依赖 | 15 个字形来自如尼文区块，缺字体显示为方块 □ |
| 形近 | `⊙`(O) 与 `○`(6)、`●`(7) 肉眼易混，靠码点区分 |
| 聊天室侧 | 房间链接谁拿到谁进；消息发出后不可撤回 |

---

## 八、许可

MIT。详见 [LICENSE](LICENSE)。
