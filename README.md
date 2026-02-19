# Claude Code Status Line 30套主题配置方案

这是一个为 Claude Code 状态栏设计的30套不同风格的配置方案集合。

## 快速开始

### 方法一：使用安装脚本
```bash
cd /Users/lei/Desktop/statusline-themes
./install.sh
```

### 方法二：手动安装
1. 选择一个主题脚本（如 `themes/01-tokyo-night.sh`）
2. 复制到 `~/.claude/statusline.sh`
3. 执行 `chmod +x ~/.claude/statusline.sh`
4. 重启 Claude Code 查看效果

```bash
cp themes/01-tokyo-night.sh ~/.claude/statusline.sh
chmod +x ~/.claude/statusline.sh
```

## 主题分类

### 经典配色系列
| 编号 | 主题名 | 风格 | 语言 |
|------|--------|------|------|
| 1 | Tokyo Night | 深蓝/紫色背景 | 英文 |
| 2 | Catppuccin Mocha | 柔和粉彩 | 中文 |
| 3 | Nord | 北极蓝调 | 英文 |
| 4 | Dracula | 深色配紫色强调 | 英文 |
| 5 | Gruvbox | 复古温暖 | 中文 |
| 6 | One Dark | Atom风格 | 英文 |
| 7 | Rose Pine | 自然柔和 | 中文 |
| 8 | Solarized | 经典精准 | 英文 |

### 创意主题系列
| 编号 | 主题名 | 风格 | 语言 |
|------|--------|------|------|
| 9 | Neon Cyberpunk | 霓虹赛博朋克 | 混合 |
| 10 | Ocean Deep | 深海蓝色 | 中文 |
| 11 | Forest Moss | 森林苔藓 | 英文 |
| 12 | Sunset Glow | 日落余晖 | 中文 |
| 13 | Midnight Purple | 午夜紫色 | 英文 |
| 14 | Arctic Frost | 北极冰霜 | 中文 |
| 15 | Cherry Blossom | 樱花粉色 | 混合 |
| 16 | Matrix Green | 矩阵绿色 | 英文 |

### 柔和主题系列
| 编号 | 主题名 | 风格 | 语言 |
|------|--------|------|------|
| 17 | Candy Pop | 糖果流行 | 中文 |
| 18 | Coffee Mocha | 咖啡摩卡 | 英文 |
| 19 | Aurora Borealis | 极光 | 中文 |
| 20 | Monochrome Pro | 单色专业 | 英文 |
| 21 | Tropical Paradise | 热带天堂 | 中文 |
| 22 | Galaxy Purple | 星系紫色 | 英文 |
| 23 | Mint Fresh | 薄荷清新 | 中文 |
| 24 | Vintage Sepia | 复古棕褐 | 英文 |

### 特色主题系列
| 编号 | 主题名 | 风格 | 语言 |
|------|--------|------|------|
| 25 | Electric Blue | 电光蓝 | 中文 |
| 26 | Autumn Leaves | 秋叶 | 英文 |
| 27 | Peach Dream | 蜜桃梦境 | 中文 |
| 28 | Steel Blue | 钢蓝 | 英文 |
| 29 | Lavender Fields | 薰衣草 | 中文 |
| 30 | Obsidian Dark | 黑曜石 | 混合 |

## 配置说明

### 进度条颜色逻辑
- `<50%` - 低使用率（绿色系）
- `50-79%` - 中等使用率（黄色/橙色系）
- `≥80%` - 高使用率（红色系）

### 进度条样式选项
- `▓░` - 方块填充
- `█░` - 实心块
- `●○` - 圆点
- `▮▯` - 竖条
- `■□` - 方框
- `▰▱` - 半圆
- `◆◇` - 菱形
- Emoji符号 - 特殊主题

### 语言选项
- **EN** - 全英文显示
- **CN** - 全中文显示
- **混合** - 标签英文，数值中文

### 目录展示规则
- 最后两级目录
- 完整路径
- 当前目录名
- 带emoji前缀
- 带文字前缀

## 自定义主题

你可以基于现有主题进行修改：

1. 复制一个主题脚本作为模板
2. 修改以下变量：
   - `MODEL_COLOR` - 模型名称颜色
   - `PROGRESS_LOW/MID/HIGH` - 进度条三档颜色
   - `PROGRESS_CHARS` - 进度条样式字符
   - `DIR_PREFIX` - 目录前缀
   - 语言相关字符串

## 颜色参考

### 256色查找表
```bash
# 查看所有256色
for i in {0..255}; do printf "\033[38;5;${i}mColor ${i}\033[0m\n"; done
```

### 常用ANSI颜色
- `\033[38;5;196m` - 红色
- `\033[38;5;46m` - 绿色
- `\033[38;5;226m` - 黄色
- `\033[38;5;51m` - 青色
- `\033[38;5;201m` - 紫色
- `\033[38;5;208m` - 橙色

## 目录结构

```
statusline-themes/
├── README.md              # 本文档
├── theme-previews.md      # 主题预览
├── themes/
│   ├── 01-tokyo-night.sh
│   ├── 02-catppuccin-mocha.sh
│   └── ... (共30个主题)
└── install.sh             # 安装脚本
```

## 故障排除

### 状态栏不显示颜色
- 确保终端支持256色
- 检查 `TERM` 环境变量：`echo $TERM`

### 中文显示乱码
- 确保终端使用UTF-8编码
- 检查 `LANG` 环境变量：`echo $LANG`

### 权限问题
```bash
chmod +x ~/.claude/statusline.sh
```

## 许可证

MIT License - 自由使用和修改
