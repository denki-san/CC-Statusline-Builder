#!/bin/bash
# Aurora Borealis 极光主题
# 风格：极光
# 语言：中文
# 从 stdin 读取 JSON 数据

# 读取 stdin 的 JSON 数据
JSON_INPUT=$(cat)

# 解析 JSON 字段
model=$(echo "$JSON_INPUT" | jq -r '.model.display_name // "GLM-5"')
input=$(echo "$JSON_INPUT" | jq -r '.context_window.total_input_tokens // 0')
output=$(echo "$JSON_INPUT" | jq -r '.context_window.total_output_tokens // 0')
percent=$(echo "$JSON_INPUT" | jq -r '.context_window.used_percentage // 0')
cwd=$(echo "$JSON_INPUT" | jq -r '.cwd // (.workspace.current_dir // "")')

# 模型名称颜色
MODEL_COLOR="\033[38;5;48m"
MODEL_CLOSE="\033[0m"

# 进度条颜色
PROGRESS_LOW="\033[38;5;48m"
PROGRESS_MID="\033[38;5;39m"
PROGRESS_HIGH="\033[38;5;202m"

# 进度条样式
PROGRESS_FILLED="🌌"
PROGRESS_EMPTY="  "

# Token 颜色
TOKEN_COLOR="\033[38;5;123m"

# 目录颜色
DIR_COLOR="\033[38;5;48m"

# Git 分支颜色
GIT_BRANCH_COLOR="\033[38;5;48m"
# Git 状态颜色（干净/脏）
GIT_CLEAN_COLOR="\033[38;5;48m"
GIT_DIRTY_COLOR="\033[38;5;202m"

# 获取进度条颜色
get_progress_color() {
    local p=$1
    if (( p < 50 )); then
        echo -e "$PROGRESS_LOW"
    elif (( p < 80 )); then
        echo -e "$PROGRESS_MID"
    else
        echo -e "$PROGRESS_HIGH"
    fi
}

# 获取进度条
get_progress_bar() {
    local p=$1
    local filled=$((p / 10))
    local empty=$((10 - filled))
    local bar=""
    for ((i=0; i<filled; i++)); do bar+="${PROGRESS_FILLED}"; done
    for ((i=0; i<empty; i++)); do bar+="${PROGRESS_EMPTY}"; done
    echo "$bar"
}

# 获取目录显示（最后两级）
get_directory() {
    local dir="$1"
    local parent=$(basename "$(dirname "$dir")")
    local current=$(basename "$dir")
    if [[ "$parent" == "/" || -z "$parent" ]]; then
        echo "~/${current}"
    else
        echo "~/${parent}/${current}"
    fi
}

# 获取 git 分支名
get_git_branch() {
    local dir="$1"
    git -C "$dir" rev-parse --abbrev-ref HEAD 2>/dev/null
}

# 获取 git 状态（是否有未提交的更改）
get_git_status() {
    local dir="$1"
    if git -C "$dir" diff --quiet 2>/dev/null && git -C "$dir" diff --cached --quiet 2>/dev/null; then
        echo "clean"
    else
        echo "dirty"
    fi
}

# 格式化 token 数量为 k
format_tokens() {
    local tokens=$1
    echo $((tokens / 1000))
}

# 主逻辑
progress_color=$(get_progress_color "$percent")
progress_bar=$(get_progress_bar "$percent")
directory=$(get_directory "$cwd")
input_k=$(format_tokens "$input")
output_k=$(format_tokens "$output")

# 第一行：模型、进度、token
printf "${MODEL_COLOR}[${model}]${MODEL_CLOSE} "
printf "${progress_color}${progress_bar} ${percent}%%${MODEL_CLOSE} "
printf "${TOKEN_COLOR}| Total: input %sk / output %sk${MODEL_CLOSE}\n" "$input_k" "$output_k"

# 第二行：目录和 git 信息
printf "${DIR_COLOR}${directory}${MODEL_CLOSE}"

# Git 分支和状态
if [[ -n "$cwd" ]]; then
    git_branch=$(get_git_branch "$cwd")
    if [[ -n "$git_branch" ]]; then
        git_status=$(get_git_status "$cwd")
        printf " "
        printf "${GIT_BRANCH_COLOR}${git_branch}${MODEL_CLOSE}"
        if [[ "$git_status" == "clean" ]]; then
            printf " ${GIT_CLEAN_COLOR}✓${MODEL_CLOSE}"
        else
            printf " ${GIT_DIRTY_COLOR}✗${MODEL_CLOSE}"
        fi
    fi
fi
