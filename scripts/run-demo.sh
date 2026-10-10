#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SKILL_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
DEMO_FILE="$SKILL_DIR/examples/demo-sha-seng.md"

usage() {
    cat <<'HELP'
时尚重塑：本地文字示例
用法：run-demo.sh [--prompt [1|2|3] | --live --model MODEL [--json] | --help]
无参数展示完整示例；--prompt 默认显示方案1的提示词。
默认与--prompt只读静态示例，不联网、不调用模型。
--live显式调用一次Codex CLI，按本目录Skill生成新的文字策划；需要账号和模型额度。
--model必须指定当前账号支持的模型；--json输出CLI事件。失败原样退出，不重试或回退到静态示例。
live会发送本包策划文本，不发送私人图片；禁用列出的图像/执行/浏览器能力并使用只读沙箱。
这些设置不保证所有宿主或managed MCP完全隔离，也不控制宿主日志与缓存。
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
    --live)
        [ "$#" -ge 3 ] && [ "$#" -le 4 ] && [ "$2" = "--model" ] || { usage >&2; exit 2; }
        MODEL=$3
        case "$MODEL" in ''|-*) usage >&2; exit 2 ;; esac
        JSON_MODE=0
        if [ "$#" -eq 4 ]; then
            [ "$4" = "--json" ] || { usage >&2; exit 2; }
            JSON_MODE=1
        fi
        command -v codex >/dev/null 2>&1 || { printf '未找到Codex CLI；未执行真实演示。\n' >&2; exit 127; }
        # Preload only the package's planning material. No user assets or global configuration are read here.
        PLANNING_FILES='SKILL.md
references/core/deconstruct.md
references/core/anchor-grading.md
references/core/axes.md
references/core/systems.md
references/core/compile.md
references/characters/sha-seng.md
references/audiences/chinese-general.md'
        for file in $PLANNING_FILES; do
            [ -r "$SKILL_DIR/$file" ] || { printf '缺少策划资料：%s\n' "$file" >&2; exit 1; }
        done
        set -- exec --ignore-user-config --ephemeral --sandbox read-only --skip-git-repo-check \
            -C "$SKILL_DIR" --model "$MODEL" \
            -c 'approval_policy="never"' -c 'web_search="disabled"' \
            -c 'developer_instructions="This is a text-only planning demo. Use only the supplied Skill material. Do not call any tools, browse, generate images, write files, or run commands. Return the planning response as text."' \
            --disable image_generation --disable shell_tool --disable unified_exec \
            --disable code_mode --disable code_mode_host --disable apps --disable plugins --disable hooks \
            --disable multi_agent --disable multi_agent_v2 --disable browser_use \
            --disable browser_use_external --disable browser_use_full_cdp_access \
            --disable computer_use --disable in_app_browser --disable skill_mcp_dependency_install \
            --disable view_image --disable workspace_dependencies --disable remote_plugin \
            --disable request_permissions_tool
        [ "$JSON_MODE" -eq 0 ] || set -- "$@" --json
        printf '真实文字演示：模型%s；使用本目录策划材料，单次调用，0自动重试。\n' "$MODEL" >&2
        {
            printf '使用下面预加载的fashion-remix开发源执行文字策划。只依据所给材料，不调用任何工具，不读写文件、不联网检索、不生图。无需另读同名安装Skill或其他引用。\n'
            for file in $PLANNING_FILES; do
                printf '\n--- 材料：%s ---\n' "$file"
                cat "$SKILL_DIR/$file"
            done
            printf '\n--- 本轮请求 ---\n为沙僧策划三个原创时尚摄影方向，不复刻具体作品、不生图。角色辨识是硬要求，偏好安静、衣装为主；街拍其次。给完整简报、各一段可用提示词和选择理由。资料的默认锚点转为本轮约定并说明依据；最后给可读状态摘要，未选定方案、未保存任务、无图像授权。不要把静态demo原文冒充本次新策划。\n'
        } | codex "$@" -
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
