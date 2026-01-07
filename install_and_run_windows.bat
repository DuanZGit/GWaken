@echo off
chcp 65001 >nul
echo 正在安装红米手环2智能睡眠监测系统...

REM 检查Python是否安装
echo.
echo 正在检查Python版本...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.6+
    echo 请从 https://www.python.org/downloads/ 下载并安装Python
    pause
    exit /b 1
)

echo.
echo 正在检查并安装依赖包...
if exist "sleep_monitor\requirements.txt" (
    echo 安装项目依赖...
    python -m pip install --upgrade pip
    pip install -r sleep_monitor\requirements.txt
) else (
    echo requirements.txt 未找到，安装默认依赖...
    python -m pip install --upgrade pip
    pip install Flask PyBluez requests
)

echo.
echo 正在验证安装...
python -c "import flask, json, bluetooth, requests; print('依赖包安装成功')"

echo.
echo 正在启动睡眠监测API服务...
echo 服务将在 http://localhost:5000 启动
echo.

REM 设置环境变量并启动服务
cd /d "%~dp0"
set PYTHONPATH=%~dp0
python -m sleep_monitor.run_api 5000

echo.
echo 如果看到错误信息，请确保：
echo 1. 已正确安装Python 3.6+
echo 2. 已安装所有依赖包
echo 3. 5000端口未被占用
echo 4. Windows防火墙允许Python访问网络
echo.
echo 服务已启动，访问 http://localhost:5000 查看Web界面
echo 在手机浏览器中访问 http://<电脑IP地址>:5000 可远程监控
echo.
echo 注意：首次运行可能需要允许防火墙访问
pause