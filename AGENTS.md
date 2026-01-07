# GWaken - 智能睡眠监测系统 AGENTS指南

## 构建/测试/代码质量命令

### Python 项目设置
- 项目主要使用 Python 3.6+ 开发
- 依赖管理使用 pip
- 建议使用虚拟环境进行开发
- 主要依赖: flask, pybluez, requests

### 构建命令
- 无特定构建命令 (Python 为解释型语言)
- 安装依赖: `pip install -r sleep_monitor/requirements.txt`
- 或使用 `pip install <package>` 安装单个包

### 测试命令
- 运行单个测试: `cd /work/sleep && PYTHONPATH=. python3 -m unittest sleep_monitor.tests.test_sleep_detector.TestSleepStageDetector.test_detect_deep_sleep -v`
- 运行特定测试类: `cd /work/sleep && PYTHONPATH=. python3 -m unittest sleep_monitor.tests.test_sleep_detector.TestSleepStageDetector -v`
- 运行模块测试: `cd /work/sleep && PYTHONPATH=. python3 -m unittest sleep_monitor.tests.test_sleep_detector`
- 运行所有测试: `cd /work/sleep && PYTHONPATH=. python3 -m unittest discover -s sleep_monitor.tests -p "test_*.py" -v`
- 运行所有测试 (简洁模式): `cd /work/sleep && PYTHONPATH=. python3 -m unittest discover -s sleep_monitor.tests -p "test_*.py"`
- Note: 所有测试应在项目根目录(/work/sleep)运行，并设置PYTHONPATH

### 代码质量命令
- 格式化代码: `black .` 或 `black <file.py>` (如已安装)
- 检查代码风格: `flake8 .` 或 `ruff check .` (如已安装)
- 类型检查: `mypy .` (如已安装)
- 安全检查: `bandit -r .` (如已安装)
- Python语法检查: `python3 -m py_compile <file.py>`

## 代码风格指南

### 导入规范
- 使用标准库导入顺序: 标准库 → 第三方库 → 本地库
- 每个导入组之间用空行分隔
- 避免 `from module import *` 这种通配符导入
- 使用绝对导入而非相对导入
- 项目特定导入示例:

```python
# 标准库导入
import time
import json
import logging
from datetime import datetime
import statistics
import threading
import queue

# 第三方库导入
import flask
from flask import Flask, request, jsonify

# 本地库导入
from sleep_monitor.sleep_analysis.sleep_stage_detector import SleepStageDetector
from sleep_monitor.sensors.bluetooth_sensor import BluetoothSensor
from sleep_monitor.alarm.smart_alarm import SmartAlarm
```

### 代码格式化
- 使用 4 个空格作为缩进
- 每行最大长度为 88-120 字符
- 使用 `black` 或 `autopep8` 自动格式化 (如已安装)
- 函数和类定义之间使用 2 个空行分隔
- 类中的方法之间使用 1 个空行分隔

### 命名约定
- 类名使用 PascalCase (如 SleepStageDetector, SmartAlarm, BluetoothSensor)
- 函数和变量使用 snake_case (如 detect_stage, sensor_data, should_wake_up)
- 常量使用 UPPER_CASE (如 DEEP_SLEEP_THRESHOLD)
- 私有成员使用 _ 前缀 (如 _analyze_heart_rate_trend, _is_rem_indication)
- 避免使用单字符变量名 (除循环计数器外)

### 类型注解
- 函数参数和返回值应添加类型注解
- 使用 `typing` 模块定义复杂类型
- 优先使用内置类型注解 (如 `list`, `dict`) 在 Python 3.9+

```python
from typing import Dict, List, Optional, Tuple
from datetime import datetime

def detect_stage(self, sensor_data: Dict[str, any]) -> str:
    """
    检测当前睡眠阶段
    
    :param sensor_data: 传感器数据，包含heart_rate和movement
    :return: 睡眠阶段 ('awake', 'light_sleep', 'deep_sleep', 'rem_sleep')
    """
    pass
```

### 错误处理
- 使用具体的异常类型捕获
- 提供有意义的错误消息
- 使用日志记录错误信息
- 避免空的 except 块
- 在传感器和网络操作中特别注意错误处理
- 实现优雅降级机制（如蓝牙不可用时使用模拟数据）

```python
import logging

logger = logging.getLogger(__name__)

try:
    sensor_data = self.sensor.get_sensor_data()
except bluetooth.btcommon.BluetoothError as e:
    logger.error(f"蓝牙数据读取错误: {e}")
    # 回退到模拟数据
    sensor_data = self._get_simulation_data()
except Exception as e:
    logger.error(f"获取传感器数据失败: {e}")
    raise
```

### 文档字符串
- 所有公共函数、类、模块都应包含文档字符串
- 使用 Google 或 NumPy 风格的文档字符串
- 描述参数、返回值、异常和用法示例

```python
def detect_stage(self, sensor_data: Dict[str, any]) -> str:
    """
    检测当前睡眠阶段
    
    基于心率和体动数据检测睡眠阶段，优先检测REM睡眠特征
    
    Args:
        sensor_data: 传感器数据，包含heart_rate和movement
        
    Returns:
        str: 睡眠阶段 ('awake', 'light_sleep', 'deep_sleep', 'rem_sleep')
        
    Example:
        >>> detector = SleepStageDetector(config)
        >>> data = {'heart_rate': 65, 'movement': 2.5}
        >>> stage = detector.detect_stage(data)
        >>> print(stage)  # 'light_sleep'
    """
```

### 代码结构
- 保持函数简短，单一职责
- 避免深度嵌套 (通常不超过 3 层)
- 使用辅助函数分解复杂逻辑
- 合理使用配置文件管理常量
- 传感器数据处理和睡眠分析应保持逻辑清晰
- 实现优雅的异常处理和资源清理

## 项目特定说明

### 环境配置
- 项目要求 Python 3.6+
- 主要依赖: flask, pybluez, requests
- 项目位于 `/work/sleep/sleep_monitor` 目录

### 项目架构
- 主要技术栈: Python
- 核心模块:
  - sensors: 传感器模块 (bluetooth_sensor.py, sensor_simulator.py, hardware_sensor.py)
  - sleep_analysis: 睡眠分析模块 (sleep_stage_detector.py)
  - alarm: 闹钟模块 (smart_alarm.py)
  - api: Web API模块 (sleep_api.py)
  - utils: 通用工具模块 (data_logger.py, time_utils.py)

### 项目运行
- 主程序入口: `cd /work/sleep && PYTHONPATH=. python3 -m sleep_monitor.main`
- API服务入口: `cd /work/sleep && PYTHONPATH=. python3 -m sleep_monitor.run_api 5000`
- 配置文件: config.json (包含睡眠检测、闹钟设置、设备设置参数)
- API测试: 访问 http://localhost:5000

### 开发工作流
- 遵循模块化设计
- 每个模块包含 __init__.py 文件
- 测试文件位于 tests/ 目录
- 优先确保所有测试通过后再提交代码
- 传感器模块需要考虑蓝牙不可用时的优雅降级

### 代码组织结构
- sleep_monitor/: 主模块目录
  - main.py: 主程序入口
  - run_api.py: API运行脚本
  - config.json: 配置文件
  - sensors/: 传感器相关功能
  - sleep_analysis/: 睡眠分析算法
  - alarm/: 闹钟逻辑
  - api/: Web API实现
  - utils/: 通用工具
  - tests/: 测试文件

## 安全考虑
- 避免在代码中硬编码敏感信息
- 使用配置文件管理参数
- 验证和清理所有外部输入
- 在文件操作中使用适当的安全措施
- 蓝牙连接和API接口需考虑安全措施
- 对用户数据进行适当的隐私保护

## Git 工作流
- 使用功能分支进行开发
- 保持提交信息清晰简洁，包含功能描述
- 为复杂更改提供详细说明
- 定期同步主分支的更改
- 提交前确保所有测试通过

## 项目特定注意事项
- 项目适配红米手环2设备，需考虑传感器精度限制
- 实现了蓝牙、硬件和模拟三种传感器接入方式
- 睡眠检测算法考虑了红米手环2的传感器特性
- API接口设计用于与小米运动健康App集成
- 代码中包含大量错误处理和降级逻辑