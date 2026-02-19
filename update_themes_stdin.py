#!/usr/bin/env python3
"""
批量更新所有主题文件为 stdin JSON 方式
保留每个主题的颜色配置
"""

import os
import re

THEMES_DIR = "themes"

# 新的通用模板（颜色和进度条字符会被替换）
TEMPLATE = '''#!/bin/bash
# {name}
# 风格：{style}
# 语言：{lang}
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
MODEL_COLOR="{model_color}"
MODEL_CLOSE="\\033[0m"

# 进度条颜色
PROGRESS_LOW="{progress_low}"
PROGRESS_MID="{progress_mid}"
PROGRESS_HIGH="{progress_high}"

# 进度条样式
PROGRESS_FILLED="{progress_filled}"
PROGRESS_EMPTY="{progress_empty}"

# Token 颜色
TOKEN_COLOR="{token_color}"

# 目录颜色
DIR_COLOR="{dir_color}"

# Git 分支颜色
GIT_BRANCH_COLOR="{git_branch_color}"
# Git 状态颜色（干净/脏）
GIT_CLEAN_COLOR="{git_clean_color}"
GIT_DIRTY_COLOR="{git_dirty_color}"

# 获取进度条颜色
get_progress_color() {{
    local p=$1
    if (( p < 50 )); then
        echo -e "$PROGRESS_LOW"
    elif (( p < 80 )); then
        echo -e "$PROGRESS_MID"
    else
        echo -e "$PROGRESS_HIGH"
    fi
}}

# 获取进度条
get_progress_bar() {{
    local p=$1
    local filled=$((p / 10))
    local empty=$((10 - filled))
    local bar=""
    for ((i=0; i<filled; i++)); do bar+="${{PROGRESS_FILLED}}"; done
    for ((i=0; i<empty; i++)); do bar+="${{PROGRESS_EMPTY}}"; done
    echo "$bar"
}}

# 获取目录显示（最后两级）
get_directory() {{
    local dir="$1"
    local parent=$(basename "$(dirname "$dir")")
    local current=$(basename "$dir")
    if [[ "$parent" == "/" || -z "$parent" ]]; then
        echo "~/${{current}}"
    else
        echo "~/${{parent}}/${{current}}"
    fi
}}

# 获取 git 分支名
get_git_branch() {{
    local dir="$1"
    git -C "$dir" rev-parse --abbrev-ref HEAD 2>/dev/null
}}

# 获取 git 状态（是否有未提交的更改）
get_git_status() {{
    local dir="$1"
    if git -C "$dir" diff --quiet 2>/dev/null && git -C "$dir" diff --cached --quiet 2>/dev/null; then
        echo "clean"
    else
        echo "dirty"
    fi
}}

# 格式化 token 数量为 k
format_tokens() {{
    local tokens=$1
    echo $((tokens / 1000))
}}

# 主逻辑
progress_color=$(get_progress_color "$percent")
progress_bar=$(get_progress_bar "$percent")
directory=$(get_directory "$cwd")
input_k=$(format_tokens "$input")
output_k=$(format_tokens "$output")

# 第一行：模型、进度、token
printf "${{MODEL_COLOR}}[${{model}}]${{MODEL_CLOSE}} "
printf "${{progress_color}}${{progress_bar}} ${{percent}}%%${{MODEL_CLOSE}} "
printf "${{TOKEN_COLOR}}| Total: input %sk / output %sk${{MODEL_CLOSE}}\\n" "$input_k" "$output_k"

# 第二行：目录和 git 信息
printf "${{DIR_COLOR}}${{directory}}${{MODEL_CLOSE}}"

# Git 分支和状态
if [[ -n "$cwd" ]]; then
    git_branch=$(get_git_branch "$cwd")
    if [[ -n "$git_branch" ]]; then
        git_status=$(get_git_status "$cwd")
        printf " "
        printf "${{GIT_BRANCH_COLOR}}${{git_branch}}${{MODEL_CLOSE}}"
        if [[ "$git_status" == "clean" ]]; then
            printf " ${{GIT_CLEAN_COLOR}}✓${{MODEL_CLOSE}}"
        else
            printf " ${{GIT_DIRTY_COLOR}}✗${{MODEL_CLOSE}}"
        fi
    fi
fi
'''

def extract_ansi256_color(content, var_name):
    """提取 ANSI 256 颜色代码"""
    match = re.search(rf'{var_name}="\\033\[38;5;(\d+)m"', content)
    if match:
        return f"\\033[38;5;{match.group(1)}m"
    return "\\033[38;5;183m"  # 默认颜色

def extract_char(content, var_name, default):
    """提取字符变量"""
    match = re.search(rf'{var_name}="(.+?)"', content)
    if match:
        return match.group(1)
    return default

def extract_header_info(content):
    """提取头部信息"""
    # 主题名称
    name_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    name = name_match.group(1) if name_match else "Theme"

    # 风格
    style_match = re.search(r'# 风格：(.+)$', content, re.MULTILINE)
    style = style_match.group(1) if style_match else "自定义"

    # 语言
    lang_match = re.search(r'# 语言：(.+)$', content, re.MULTILINE)
    lang = lang_match.group(1) if lang_match else "中文"

    return name, style, lang

def update_theme(filepath):
    """更新单个主题文件"""
    with open(filepath, 'r') as f:
        content = f.read()

    # 提取颜色配置
    model_color = extract_ansi256_color(content, "MODEL_COLOR")
    progress_low = extract_ansi256_color(content, "PROGRESS_LOW")
    progress_mid = extract_ansi256_color(content, "PROGRESS_MID")
    progress_high = extract_ansi256_color(content, "PROGRESS_HIGH")
    token_color = extract_ansi256_color(content, "TOKEN_COLOR")

    # 提取进度条字符
    progress_filled = extract_char(content, "PROGRESS_FILLED", "█")
    progress_empty = extract_char(content, "PROGRESS_EMPTY", "░")

    # 提取头部信息
    name, style, lang = extract_header_info(content)

    # 生成新内容
    new_content = TEMPLATE.format(
        name=name,
        style=style,
        lang=lang,
        model_color=model_color,
        progress_low=progress_low,
        progress_mid=progress_mid,
        progress_high=progress_high,
        progress_filled=progress_filled,
        progress_empty=progress_empty,
        token_color=token_color,
        dir_color=progress_low,  # 目录颜色使用低进度条颜色
        git_branch_color=model_color,  # git 分支颜色使用模型颜色
        git_clean_color=progress_low,  # 干净状态使用低进度条颜色
        git_dirty_color=progress_high  # 脏状态使用高进度条颜色
    )

    # 写入文件
    with open(filepath, 'w') as f:
        f.write(new_content)

    print(f"已更新: {os.path.basename(filepath)}")

def main():
    themes_path = THEMES_DIR
    if not os.path.exists(themes_path):
        print(f"错误: 找不到 {themes_path} 目录")
        return

    count = 0
    for filename in sorted(os.listdir(themes_path)):
        if filename.endswith('.sh'):
            filepath = os.path.join(themes_path, filename)
            update_theme(filepath)
            count += 1

    print(f"\n完成! 共更新了 {count} 个主题文件")

if __name__ == "__main__":
    main()
