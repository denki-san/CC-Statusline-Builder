#!/bin/bash
# Claude Code Status Line 主题安装脚本
# 用法: ./install.sh [主题编号]

THEMES_DIR="$(dirname "$0")/themes"
TARGET_FILE="$HOME/.claude/statusline.sh"

# 显示帮助信息
show_help() {
    echo "Claude Code Status Line 主题安装脚本"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  <编号>     安装指定编号的主题 (1-30)"
    echo "  -l, --list 列出所有可用主题"
    echo "  -h, --help 显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 1        安装 Tokyo Night 主题"
    echo "  $0 -l       列出所有主题"
    echo ""
    echo "主题列表:"
    echo "  1  - Tokyo Night (经典)      16 - Matrix Green (创意)"
    echo "  2  - Catppuccin Mocha (经典) 17 - Candy Pop (柔和)"
    echo "  3  - Nord (经典)             18 - Coffee Mocha (柔和)"
    echo "  4  - Dracula (经典)          19 - Aurora Borealis (柔和)"
    echo "  5  - Gruvbox (经典)          20 - Monochrome Pro (柔和)"
    echo "  6  - One Dark (经典)         21 - Tropical Paradise (柔和)"
    echo "  7  - Rose Pine (经典)        22 - Galaxy Purple (柔和)"
    echo "  8  - Solarized (经典)        23 - Mint Fresh (柔和)"
    echo "  9  - Neon Cyberpunk (创意)   24 - Vintage Sepia (柔和)"
    echo "  10 - Ocean Deep (创意)       25 - Electric Blue (特色)"
    echo "  11 - Forest Moss (创意)      26 - Autumn Leaves (特色)"
    echo "  12 - Sunset Glow (创意)      27 - Peach Dream (特色)"
    echo "  13 - Midnight Purple (创意)  28 - Steel Blue (特色)"
    echo "  14 - Arctic Frost (创意)     29 - Lavender Fields (特色)"
    echo "  15 - Cherry Blossom (创意)   30 - Obsidian Dark (特色)"
}

# 列出所有主题
list_themes() {
    echo "可用主题列表:"
    echo ""
    printf "%-4s %-25s %-12s %s\n" "编号" "主题名称" "语言" "风格"
    echo "--------------------------------------------------------"
    printf "%-4s %-25s %-12s %s\n" "1"   "Tokyo Night"             "EN"  "经典配色"
    printf "%-4s %-25s %-12s %s\n" "2"   "Catppuccin Mocha"        "CN"  "经典配色"
    printf "%-4s %-25s %-12s %s\n" "3"   "Nord"                    "EN"  "经典配色"
    printf "%-4s %-25s %-12s %s\n" "4"   "Dracula"                 "EN"  "经典配色"
    printf "%-4s %-25s %-12s %s\n" "5"   "Gruvbox"                 "CN"  "经典配色"
    printf "%-4s %-25s %-12s %s\n" "6"   "One Dark"                "EN"  "经典配色"
    printf "%-4s %-25s %-12s %s\n" "7"   "Rose Pine"               "CN"  "经典配色"
    printf "%-4s %-25s %-12s %s\n" "8"   "Solarized"               "EN"  "经典配色"
    printf "%-4s %-25s %-12s %s\n" "9"   "Neon Cyberpunk"          "混合" "创意主题"
    printf "%-4s %-25s %-12s %s\n" "10"  "Ocean Deep"              "CN"  "创意主题"
    printf "%-4s %-25s %-12s %s\n" "11"  "Forest Moss"             "EN"  "创意主题"
    printf "%-4s %-25s %-12s %s\n" "12"  "Sunset Glow"             "CN"  "创意主题"
    printf "%-4s %-25s %-12s %s\n" "13"  "Midnight Purple"         "EN"  "创意主题"
    printf "%-4s %-25s %-12s %s\n" "14"  "Arctic Frost"            "CN"  "创意主题"
    printf "%-4s %-25s %-12s %s\n" "15"  "Cherry Blossom"          "混合" "创意主题"
    printf "%-4s %-25s %-12s %s\n" "16"  "Matrix Green"            "EN"  "创意主题"
    printf "%-4s %-25s %-12s %s\n" "17"  "Candy Pop"               "CN"  "柔和主题"
    printf "%-4s %-25s %-12s %s\n" "18"  "Coffee Mocha"            "EN"  "柔和主题"
    printf "%-4s %-25s %-12s %s\n" "19"  "Aurora Borealis"         "CN"  "柔和主题"
    printf "%-4s %-25s %-12s %s\n" "20"  "Monochrome Pro"          "EN"  "柔和主题"
    printf "%-4s %-25s %-12s %s\n" "21"  "Tropical Paradise"       "CN"  "柔和主题"
    printf "%-4s %-25s %-12s %s\n" "22"  "Galaxy Purple"           "EN"  "柔和主题"
    printf "%-4s %-25s %-12s %s\n" "23"  "Mint Fresh"              "CN"  "柔和主题"
    printf "%-4s %-25s %-12s %s\n" "24"  "Vintage Sepia"           "EN"  "柔和主题"
    printf "%-4s %-25s %-12s %s\n" "25"  "Electric Blue"           "CN"  "特色主题"
    printf "%-4s %-25s %-12s %s\n" "26"  "Autumn Leaves"           "EN"  "特色主题"
    printf "%-4s %-25s %-12s %s\n" "27"  "Peach Dream"             "CN"  "特色主题"
    printf "%-4s %-25s %-12s %s\n" "28"  "Steel Blue"              "EN"  "特色主题"
    printf "%-4s %-25s %-12s %s\n" "29"  "Lavender Fields"         "CN"  "特色主题"
    printf "%-4s %-25s %-12s %s\n" "30"  "Obsidian Dark"           "混合" "特色主题"
}

# 安装主题
install_theme() {
    local theme_num=$1

    # 格式化主题编号
    if (( theme_num < 1 || theme_num > 30 )); then
        echo "错误: 主题编号必须在 1-30 之间"
        exit 1
    fi

    # 查找主题文件
    local theme_file=$(printf "%s/%02d-*.sh" "$THEMES_DIR" "$theme_num")
    theme_file=$(ls $theme_file 2>/dev/null | head -1)

    if [[ ! -f "$theme_file" ]]; then
        echo "错误: 找不到主题文件"
        exit 1
    fi

    # 获取主题名称
    local theme_name=$(basename "$theme_file" .sh)
    theme_name=${theme_name#*-}

    echo "正在安装主题: $theme_name"

    # 确保 ~/.claude 目录存在
    mkdir -p "$(dirname "$TARGET_FILE")"

    # 复制主题文件
    cp "$theme_file" "$TARGET_FILE"

    # 设置执行权限
    chmod +x "$TARGET_FILE"

    echo ""
    echo "✅ 主题安装成功!"
    echo ""
    echo "主题文件: $TARGET_FILE"
    echo "主题名称: $theme_name"
    echo ""
    echo "请重启 Claude Code 以查看效果。"
}

# 主逻辑
case "$1" in
    ""|-h|--help)
        show_help
        ;;
    -l|--list)
        list_themes
        ;;
    *)
        if [[ "$1" =~ ^[0-9]+$ ]]; then
            install_theme "$1"
        else
            echo "错误: 无效的参数 '$1'"
            echo "使用 '$0 --help' 查看帮助信息"
            exit 1
        fi
        ;;
esac
