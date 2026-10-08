#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SKILL_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
DEMO_FILE="$SKILL_DIR/examples/demo-sha-seng.md"

usage() {
    cat <<'HELP'
时尚重塑：本地文字示例
用法：run-demo.sh [--prompt [1|2|3] | --help]
无参数展示完整示例；--prompt 默认显示方案1的提示词。
此脚本只读取已保存的示例，不联网、不调用模型、不生图。
HELP
}

if [ ! -r "$DEMO_FILE" ]; then
    printf '找不到可读的示例文件：%s\n' "$DEMO_FILE" >&2
    exit 1
fi

if [ "$#" -eq 0 ]; then
    cat "$DEMO_FILE"
    exit 0
fi

case "$1" in
    --help|-h)
        [ "$#" -eq 1 ] || { usage >&2; exit 2; }
        usage
        ;;
    --prompt)
        [ "$#" -le 2 ] || { usage >&2; exit 2; }
        NUMBER=${2:-1}
        case "$NUMBER" in
            1|2|3) ;;
            *) usage >&2; exit 2 ;;
        esac
        awk -v number="$NUMBER" '
            $0 == "<!-- prompt:" number " -->" { selected=1; next }
            $0 == "<!-- /prompt:" number " -->" { selected=0; next }
            selected && $0 == "```text" { inside=1; next }
            selected && $0 == "```" { inside=0; next }
            selected && inside { print; found=1 }
            END { if (!found) exit 1 }
        ' "$DEMO_FILE"
        ;;
    *)
        usage >&2
        exit 2
        ;;
esac
