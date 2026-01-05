#!/bin/bash

# 部署脚本 - 支持多种部署平台

set -e  # 遇到错误时退出

echo "=== 红米手环2智能睡眠监测系统 - 部署脚本 ==="

# 检查是否在项目根目录
if [ ! -f "requirements.txt" ] || [ ! -d "sleep_monitor" ]; then
    echo "错误: 不在项目根目录"
    exit 1
fi

# 显示帮助信息
show_help() {
    echo "用法: $0 [选项]"
    echo "选项:"
    echo "  docker    - 构建并运行Docker容器"
    echo "  heroku    - 部署到Heroku"
    echo "  local     - 本地运行"
    echo "  -h, --help - 显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 docker    # 构建并运行Docker容器"
    echo "  $0 local     # 本地运行应用"
}

# Docker部署
deploy_docker() {
    echo "=== 构建Docker镜像 ==="
    if ! command -v docker &> /dev/null; then
        echo "错误: Docker未安装或不可用"
        exit 1
    fi
    
    docker build -t sleep-monitor .
    
    echo "=== 运行Docker容器 ==="
    docker run -d -p 5000:5000 --name sleep-monitor-app sleep-monitor
    
    echo "应用已启动，访问 http://localhost:5000"
}

# 本地部署
run_local() {
    echo "=== 本地运行应用 ==="
    
    # 检查Python版本
    if ! command -v python3 &> /dev/null; then
        echo "错误: Python3未安装"
        exit 1
    fi
    
    # 安装依赖
    echo "安装依赖..."
    pip3 install -r requirements.txt || {
        echo "尝试使用pip安装依赖..."
        pip install -r requirements.txt
    }
    
    # 设置环境变量
    export PYTHONPATH=$(pwd)
    
    # 运行应用
    echo "启动应用..."
    python3 -m sleep_monitor.run_api 5000 &
    
    # 显示进程信息
    echo "应用已启动，PID: $!"
    echo "访问 http://localhost:5000"
    
    # 等待几秒后检查服务状态
    sleep 3
    if curl -s http://localhost:5000/ &> /dev/null; then
        echo "服务运行正常"
    else
        echo "警告: 服务可能未正常启动"
    fi
}

# Heroku部署
deploy_heroku() {
    echo "=== 部署到Heroku ==="
    
    if ! command -v heroku &> /dev/null; then
        echo "错误: Heroku CLI未安装"
        echo "请访问 https://devcenter.heroku.com/articles/heroku-cli 安装"
        exit 1
    fi
    
    # 检查是否已登录
    if ! heroku auth:whoami &> /dev/null; then
        echo "请先登录Heroku:"
        echo "  heroku login"
        exit 1
    fi
    
    # 检查是否在git仓库中
    if [ ! -d ".git" ]; then
        echo "错误: 不在git仓库中"
        exit 1
    fi
    
    # 检查是否已关联Heroku应用
    if ! git remote get-url heroku &> /dev/null; then
        echo "创建新的Heroku应用..."
        heroku create
    fi
    
    echo "推送代码到Heroku..."
    git push heroku main
    
    echo "打开应用..."
    heroku open
}

# 解析命令行参数
case "$1" in
    docker)
        deploy_docker
        ;;
    heroku)
        deploy_heroku
        ;;
    local)
        run_local
        ;;
    -h|--help)
        show_help
        ;;
    "")
        echo "请选择部署方式:"
        show_help
        ;;
    *)
        echo "未知选项: $1"
        show_help
        exit 1
        ;;
esac

echo ""
echo "=== 部署完成 ==="