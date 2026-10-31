#!/usr/bin/env python3
"""中文 / 粤语 -> 拼音 -> MIR 字形。

依赖：pypinyin（仅中文转拼音需要，纯拉丁文本编解码不需要）
用法：
  python3 tools/zh2mir.py --text "我不是人"
  python3 tools/zh2mir.py --file input.md
  python3 tools/zh2mir.py --text "你睇唔明" --lang yue --num glyph --wrap
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
from mir1 import encode, decode, wrap  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description='中文转 MIR 字形')
    ap.add_argument('--text', default='')
    ap.add_argument('--file', default='')
    ap.add_argument('--num', default='glyph', choices=['plain', 'glyph'])
    ap.add_argument('--lang', default='cmn', choices=['cmn', 'yue'])
    ap.add_argument('--script', default='pinyin', choices=['pinyin', 'jyutping'])
    ap.add_argument('--wrap', action='store_true', help='封装协议头')
    ap.add_argument('--verify', action='store_true', help='反编译回验')
    a = ap.parse_args()

    if a.file:
        with open(a.file, encoding='utf-8') as f:
            text = f.read().strip()
    else:
        text = a.text

    if not text:
        print('错误：用 --text 或 --file 提供内容', file=sys.stderr)
        return 2

    try:
        from pypinyin import lazy_pinyin, Style
    except ImportError:
        print('错误：需要 pypinyin。安装：pip3 install pypinyin', file=sys.stderr)
        return 2

    py = '·'.join(lazy_pinyin(text, style=Style.TONE3))
    g = encode(py, num_glyph=(a.num == 'glyph'))

    print('原文: %s' % text)
    print('拼音: %s' % py)
    print('字形: %s' % g)

    if a.wrap:
        print('封装: %s' % wrap(g, a.script, a.lang, a.num))

    if a.verify:
        back = decode(g)
        print('回验: %s (%s)' % ('一致' if back == py.upper() else '不一致', back))

    return 0


if __name__ == '__main__':
    sys.exit(main())
