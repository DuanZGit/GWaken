#!/usr/bin/env python3
"""
红米手环2睡眠监测API运行脚本
"""
import sys
import os
# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 设置环境变量，确保模块可以正确导入
os.environ['PYTHONPATH'] = project_root

from sleep_monitor.api.sleep_api import run_api_server

if __name__ == '__main__':
    # 可以通过命令行参数指定端口
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    run_api_server(host='0.0.0.0', port=port)