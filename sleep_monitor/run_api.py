#!/usr/bin/env python3
"""
红米手环2睡眠监测API运行脚本
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.sleep_api import run_api_server

if __name__ == '__main__':
    # 可以通过命令行参数指定端口
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    run_api_server(host='0.0.0.0', port=port)