@echo off
chcp 65001 >nul
echo #########################################################################
echo #                红米手环2智能睡眠监测系统 - Windows安装脚本             #
echo #########################################################################
echo.

REM 检查Python版本
echo [1/5] 检查Python版本...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.6+
    echo 请从 https://www.python.org/downloads/ 下载并安装Python
    pause
    exit /b 1
)

for /f "tokens=2 delims= " %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
for /f "tokens=1,2,3 delims=." %%a in ("%PYTHON_VERSION%") do (
    set PY_MAJOR=%%a
    set PY_MINOR=%%b
    set PY_PATCH=%%c
)

if %PY_MAJOR% lss 3 (
    echo 错误: Python版本过低，需要Python 3.6+
    pause
    exit /b 1
)

if %PY_MAJOR% equ 3 if %PY_MINOR% lss 6 (
    echo 错误: Python版本过低，需要Python 3.6+
    pause
    exit /b 1
)

echo Python版本: %PYTHON_VERSION% - 满足要求
echo.

REM 升级pip
echo [2/5] 升级pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo 警告: pip升级失败，继续安装
)
echo.

REM 安装依赖
echo [3/5] 安装项目依赖...
if exist "sleep_monitor\requirements.txt" (
    echo 正在安装 requirements.txt 中的依赖...
    pip install -r sleep_monitor\requirements.txt
) else (
    echo requirements.txt 未找到，安装默认依赖...
    pip install Flask==2.3.3 PyBluez==0.23 requests==2.31.0
)

if errorlevel 1 (
    echo 警告: 依赖安装可能失败，尝试使用国内源...
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ Flask==2.3.3 PyBluez==0.23 requests==2.31.0
)
echo.

REM 验证安装
echo [4/5] 验证安装...
python -c "import flask, json, requests; print('基本依赖验证通过')"
if errorlevel 1 (
    echo 警告: 验证失败，但继续运行
)

REM 检查蓝牙模块
python -c "import bluetooth; print('蓝牙模块可用')" >nul 2>&1
if errorlevel 1 (
    echo 蓝牙模块不可用，系统将使用模拟数据模式
    echo 这在Windows上是正常的，如果没有蓝牙适配器或PyBluez不可用
)
echo.

REM 启动服务
echo [5/5] 启动睡眠监测API服务...
echo.
echo 服务将在 http://localhost:5000 启动
echo.
echo 请在浏览器中访问以下地址:
echo   - 本地访问: http://localhost:5000
echo   - 手机访问: http://<电脑IP地址>:5000
echo.
echo 按 Ctrl+C 停止服务
echo #########################################################################
echo.

REM 设置环境变量并启动服务
cd /d "%~dp0"
set PYTHONPATH=%~dp0
python -m sleep_monitor.run_api 5000

echo.
echo 服务已停止
pause