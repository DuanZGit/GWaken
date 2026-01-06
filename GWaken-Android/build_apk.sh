#!/bin/bash
# build_apk.sh

echo "开始构建GWaken Android APK..."

# 检查是否已安装buildozer
if ! command -v buildozer &> /dev/null; then
    echo "Buildozer未安装，正在安装..."
    pip install buildozer
fi

# 初始化buildozer (如果还没有spec文件)
if [ ! -f buildozer.spec ]; then
    echo "Buildozer spec文件不存在，正在初始化..."
    buildozer init
fi

# 更新依赖
echo "更新项目依赖..."
pip install -r requirements.txt

# 构建APK
echo "开始构建APK..."
buildozer android debug

echo "APK构建完成，位于 bin/ 目录下"