#!/bin/bash

# 同步项目到GitHub的脚本

echo "=== 红米手环2智能睡眠监测系统 - GitHub同步脚本 ==="

# 检查是否已安装git
if ! command -v git &> /dev/null; then
    echo "错误: 未找到git命令"
    exit 1
fi

# 检查当前目录
echo "当前目录: $(pwd)"

# 创建.gitignore文件
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
.coverage
.cache
.pytest_cache/
htmlcov/
.tox/
.coverage*
.nox/
.DS_Store

# Environment
.env
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Data and logs
data/
logs/
*.log
*.csv
*.json
config.json  # 如果包含敏感信息
*.db
*.sqlite

# System
.DS_Store
ehthumbs.db
Icon?
Thumbs.db
*.tmp
EOF

echo "已创建 .gitignore 文件"

# 检查是否已经是git仓库
if [ -d ".git" ]; then
    echo "当前目录已经是git仓库"
    # 拉取最新更改
    git pull origin main || echo "无远程仓库或拉取失败"
else
    echo "初始化git仓库..."
    git init
fi

# 添加所有文件
echo "添加所有文件到git..."
git add .

# 检查是否有待提交的更改
if git diff --cached --quiet; then
    echo "没有更改需要提交"
else
    # 创建初始提交
    echo "创建初始提交..."
    git config user.name "openhands"
    git config user.email "openhands@anomalyai.com"
    git commit -m "Initial commit: 红米手环2智能睡眠监测系统
    
- 完整的睡眠监测功能
- 支持蓝牙连接红米手环2
- 智能唤醒算法
- Web API接口
- 详细的文档和配置"
    
    echo "初始提交完成"
fi

echo ""
echo "=== 同步到GitHub的步骤 ==="
echo "1. 在GitHub上创建新仓库"
echo "2. 复制仓库的HTTPS或SSH URL"
echo "3. 运行以下命令之一:"
echo ""
echo "   # 使用HTTPS (推荐)"
echo "   git remote add origin <your-github-repo-url>"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "   # 使用SSH (需要配置SSH密钥)"
echo "   git remote add origin <your-github-repo-url>"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "注意: 如果远程仓库不为空，请先拉取远程更改:"
echo "   git pull origin main --allow-unrelated-histories"
echo ""

echo "=== 项目结构概览 ==="
find . -name ".*" -prune -o -type f -name "*.py" -print | head -20
echo "... (更多文件)"