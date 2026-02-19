# Statusline Builder

自定义你的 Claude Code 状态栏 —— 可视化配置，实时预览，一键安装。
<img width="483" height="104" alt="image" src="https://github.com/user-attachments/assets/7c2f60b9-34b6-4e37-98b6-82001f31fd64" />

## 使用方式

打开 [preview.html](preview.html)。

## 快速开始（3 步）

1. 在页面里选择样式  
2. 点击 `Copy Install Cmd`  
3. 在终端粘贴执行并重启 Claude Code

## 可配置内容

- 进度条样式（6 种）
- 配色主题（10 种）
- 目录前缀（5 种）
- Token 显示格式（3 种）
- Git 状态显示（开关 + 样式）

可组合出大量主题，按你的终端风格自由调整。

## 前置要求

- 终端支持 256 色
- 已安装 `jq`
- UTF-8 编码

## 常见问题

### 状态栏不显示？
```bash
chmod +x ~/.claude/statusline.sh
```

### 没有颜色？
```bash
echo $TERM  # 应该显示 xterm-256color 或类似
```

### 出现乱码？
```bash
echo $LANG  # 应该包含 UTF-8
```
