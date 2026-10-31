#!/usr/bin/env bash
# 打包整个项目为 ZIP。用法：bash scripts/build.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
NAME="$(basename "$ROOT")"
OUT="$(dirname "$ROOT")/${NAME}.zip"
rm -f "$OUT"
cd "$(dirname "$ROOT")"
zip -r "$OUT" "$NAME" -x "$NAME/.git/*" "*.DS_Store" >/dev/null
echo "已打包: $OUT"
