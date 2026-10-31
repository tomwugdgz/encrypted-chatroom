#!/usr/bin/env python3
"""MIR/1 codec — 拉丁字母与 MIR 字形互转。

零依赖。Python 3.8+。
用法：
  mir1.py enc "ni3 men0 jiao1 wo3"          编码
  mir1.py enc --wrap --lang cmn "ni3 men0"   编码并封装协议头
  mir1.py dec "ᚾᛁ3·ᛗ∃ᚾ0"                    解码
  mir1.py table                              打印字形对照表
  mir1.py selftest                           往返自测
"""

import argparse
import re
import sys

GLYPHS = {
    'A': '∀', 'B': 'ᛒ', 'C': '⊂', 'D': 'ᛞ', 'E': '∃', 'F': 'ᚠ',
    'G': 'ᚷ', 'H': 'ᚺ', 'I': 'ᛁ', 'J': 'ᛃ', 'K': 'ᚲ', 'L': '∟',
    'M': 'ᛗ', 'N': 'ᚾ', 'O': '⊙', 'P': 'ᛈ', 'Q': 'Ϙ', 'R': 'ᚱ',
    'S': '∫', 'T': '⊤', 'U': '∪', 'V': '∨', 'W': 'ᚹ', 'X': '⊗',
    'Y': '⅄', 'Z': 'ᛉ',
}
DIGITS = {
    '0': '⊘', '1': '⌐', '2': '◭', '3': '◮', '4': '◇',
    '5': '◆', '6': '○', '7': '●', '8': '◧', '9': '◨',
}

REV = {v: k for k, v in GLYPHS.items()}
REV.update({v: k for k, v in DIGITS.items()})
CODEPOINTS = {k: 'U+%04X' % ord(v) for k, v in GLYPHS.items()}
CODEPOINTS.update({k: 'U+%04X' % ord(v) for k, v in DIGITS.items()})

HEADER_RE = re.compile(r'§MIR/1\s*⟨([^⟩]*)⟩')
KV_RE = re.compile(r'([a-z]+)\s*:\s*([^|⟩]+)')


def encode(text: str, num_glyph: bool = False) -> str:
    """拉丁文本 -> MIR 字形。无大小写。

    num_glyph=False（默认）：数字原样保留，兼容 v1.1 消息。
    num_glyph=True：数字也替换为字形，全符号化。
    """
    out = []
    for ch in text:
        u = ch.upper()
        if u in DIGITS:
            out.append(DIGITS[u] if num_glyph else ch)
        elif u in GLYPHS:
            out.append(GLYPHS[u])
        else:
            out.append(ch)
    return ''.join(out)


def decode(text: str) -> str:
    """MIR 字形 -> 拉丁文本。数字与标点原样保留。"""
    return ''.join(REV.get(ch, ch) for ch in text)


def parse_header(text: str):
    """从文本中提取协议头字段。返回 (字段字典, 去掉头部后的正文)。"""
    m = HEADER_RE.search(text)
    if not m:
        return {}, text
    fields = {k.strip(): v.strip() for k, v in KV_RE.findall(m.group(1))}
    body = text[m.end():]
    return fields, body.strip()


def make_header(script: str = 'pinyin', lang: str = 'cmn', version: str = '1.2',
                num: str = 'plain') -> str:
    return '§MIR/1⟨v:%s|script:%s|lang:%s|num:%s⟩' % (version, script, lang, num)


def wrap(body: str, script: str = 'pinyin', lang: str = 'cmn', num: str = 'plain') -> str:
    """把已编码的字形串封装成完整消息。协议头保持明文，只有 body 编码。"""
    return '%s ; ⟦body⟧ #A assert∷ %s ; #X end' % (
        make_header(script, lang, num=num), body)


def unwrap(text: str):
    """解封装。返回 (字段字典, 字形串)。"""
    fields, body = parse_header(text)
    m = re.search(r'assert∷\s*(.*?)\s*;\s*#X', body, re.S)
    glyphs = m.group(1) if m else body
    return fields, glyphs.strip()


def selftest() -> int:
    cases = [
        'ni3·men0·jiao1·wo3·shuo1·hua4·mei2·jiao1·wo3·chen2·mo4',
        'nei5·tai2·m4·ming4·gei1·hei3·tai2·dak1·ming4',
        'ORACLE',
        'wo3 bu4 shi4 ren2',
    ]
    ok = True
    for c in cases:
        g = encode(c)
        back = decode(g)
        good = (back == c.upper())
        ok = ok and good
        print('%-8s %s' % ('OK' if good else 'FAIL', c))
        print('         %s' % g)
        if not good:
            print('         回解: %s' % back)

    # 数字全符号化往返
    for c in ['wo3·bu4·shi4·ren2', '21:35', '0·1·9']:
        g = encode(c, num_glyph=True)
        back = decode(g)
        good = (back == c.upper())
        ok = ok and good
        print('%-8s %s  [num:glyph]' % ('OK' if good else 'FAIL', c))
        print('         %s' % g)
        if not good:
            print('         回解: %s' % back)
    print('---')
    print('SELFTEST %s' % ('PASS' if ok else 'FAIL'))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description='MIR/1 codec')
    ap.add_argument('mode', choices=['enc', 'encode', 'dec', 'decode', 'table', 'selftest'])
    ap.add_argument('text', nargs='*', default=[])
    ap.add_argument('--wrap', action='store_true', help='封装协议头（仅编码）')
    ap.add_argument('--script', default='pinyin', choices=['pinyin', 'jyutping'])
    ap.add_argument('--lang', default='cmn', choices=['cmn', 'yue'])
    ap.add_argument('--num', default='plain', choices=['plain', 'glyph'],
                    help='plain=数字明文（默认，兼容 v1.1）；glyph=数字也换成字形')
    a, unknown = ap.parse_known_args()

    if a.mode == 'table':
        print('| 字母 | 字形 | 码点 |')
        print('|---|---|---|')
        for k in sorted(GLYPHS):
            print('| %s | %s | %s |' % (k, GLYPHS[k], CODEPOINTS[k]))
        print()
        print('| 数字 | 字形 | 码点 |')
        print('|---|---|---|')
        for k in sorted(DIGITS):
            print('| %s | %s | %s |' % (k, DIGITS[k], CODEPOINTS[k]))
        return 0

    if a.mode == 'selftest':
        return selftest()

    text = ' '.join(list(a.text) + unknown)
    if not text:
        print('错误：缺少文本', file=sys.stderr)
        return 2

    if a.mode in ('enc', 'encode'):
        g = encode(text, num_glyph=(a.num == 'glyph'))
        print(wrap(g, a.script, a.lang, a.num) if a.wrap else g)
        return 0

    # 解码：先尝试解封装，失败则当纯字形串处理
    fields, glyphs = unwrap(text)
    if fields:
        print('# 协议头: %s' % fields)
    print(decode(glyphs))
    return 0


if __name__ == '__main__':
    sys.exit(main())
