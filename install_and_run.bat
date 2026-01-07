@echo off
echo 正在安装睡眠监测系统...

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.6+
    pause
    exit /b 1
)

REM 安装依赖
echo 安装依赖包...
pip install -r sleep_monitor/requirements.txt

REM 启动API服务
echo 启动睡眠监测API服务...
cd /work/sleep
set PYTHONPATH=.
python -m sleep_monitor.run_api 5000

echo 服务已启动，访问 http://localhost:5000
pause