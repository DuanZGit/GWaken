# 项目配置说明

## 构建/测试/代码质量命令

### Python 项目设置
- 项目主要使用 Python 3.6+ 开发
- 依赖管理使用 pip
- 建议使用虚拟环境进行开发

### 构建命令
- 无特定构建命令 (Python 为解释型语言)
- 安装依赖: `pip install -r requirements.txt`
- 或使用 `pip install <package>` 安装单个包

### 测试命令
- 运行单个测试: `cd sleep && python -m pytest <test_file.py> -v` 或 `cd sleep && python -m unittest <test_file>.TestClassName -v`
- 运行特定测试函数: `cd sleep && python -m unittest sleep_monitor.tests.test_sleep_detector.TestSleepStageDetector.test_detect_deep_sleep -v`
- 运行所有测试: `cd sleep && python -m unittest discover -s sleep_monitor.tests -p "test_*.py" -v`
- 使用 pytest: `cd sleep && python -m pytest sleep_monitor/tests/ -v`
- Note: All tests should be run from the project root directory (/work/sleep)

### 代码质量命令
- 格式化代码: `black .` 或 `black <file.py>`
- 检查代码风格: `flake8 .` 或 `ruff check .`
- 类型检查: `mypy .` (如已安装)
- 安全检查: `bandit -r .` (如已安装)

## 代码风格指南

### 导入规范
- 使用标准库导入顺序: 标准库 → 第三方库 → 本地库
- 每个导入组之间用空行分隔
- 避免 `from module import *` 这种通配符导入
- 使用绝对导入而非相对导入

```python
# 标准库导入
import time
import json
import logging
from datetime import datetime
import statistics
from pathlib import Path

# 第三方库导入
import requests

# 本地库导入
from sleep_monitor.sleep_analysis.sleep_stage_detector import SleepStageDetector
from sleep_monitor.sensors.sensor_simulator import SensorSimulator
from sleep_monitor.alarm.smart_alarm import SmartAlarm
```

### 代码格式化
- 使用 4 个空格作为缩进
- 每行最大长度为 88-120 字符
- 使用 `black` 或 `autopep8` 自动格式化
- 函数和类定义之间使用 2 个空行分隔
- 类中的方法之间使用 1 个空行分隔

### 命名约定
- 类名使用 PascalCase (如 SleepStageDetector, SensorSimulator)
- 函数和变量使用 snake_case (如 detect_stage, sensor_data)
- 常量使用 UPPER_CASE
- 私有成员使用 _ 前缀 (如 _analyze_heart_rate_trend)
- 避免使用单字符变量名 (除循环计数器外)

### 类型注解
- 函数参数和返回值应添加类型注解
- 使用 `typing` 模块定义复杂类型
- 优先使用内置类型注解 (如 `list`, `dict`) 在 Python 3.9+

### 错误处理
- 使用具体的异常类型捕获
- 提供有意义的错误消息
- 使用日志记录错误信息
- 避免空的 except 块

```python
import logging

logger = logging.getLogger(__name__)

try:
    result = risky_operation()
except SpecificException as e:
    logger.error(f"操作失败: {e}")
    raise
```

### 文档字符串
- 所有公共函数、类、模块都应包含文档字符串
- 使用 Google 或 NumPy 风格的文档字符串
- 描述参数、返回值、异常和用法示例

```python
def detect_stage(self, sensor_data):
    """
    检测当前睡眠阶段
    
    :param sensor_data: 传感器数据，包含heart_rate和movement
    :return: 睡眠阶段 ('awake', 'light_sleep', 'deep_sleep', 'rem_sleep')
    """
```

### 代码结构
- 保持函数简短，单一职责
- 避免深度嵌套 (通常不超过 3 层)
- 使用辅助函数分解复杂逻辑
- 合理使用配置文件管理常量

## 项目特定说明

### 环境配置
- 项目要求 Python 3.6+
- 主要依赖: datetime (用于时间处理)
- 项目位于 `/work/sleep/sleep_monitor` 目录

### 项目架构
- 主要技术栈: Python
- 核心模块:
  - sensors: 传感器模块 (sensor_simulator.py)
  - sleep_analysis: 睡眠分析模块 (sleep_stage_detector.py, signal_processor.py)
  - alarm: 闹钟模块 (smart_alarm.py)
  - utils: 工具模块 (data_logger.py, time_utils.py)

### 项目运行
- 主程序入口: `cd sleep_monitor && python -m sleep_monitor.main` or `PYTHONPATH=. python sleep_monitor/main.py`
- Configuration file: config.json (contains sleep detection, alarm settings, device settings parameters)
- To run from project root: `PYTHONPATH=. python -m sleep_monitor.main`
- Note: When running from project root, ensure config.json is in the correct location (sleep_monitor/config.json)

### 开发工作流
- 遵循模块化设计
- 每个模块包含 __init__.py 文件
- 测试文件位于 tests/ 目录

### 代码组织结构
- sleep_monitor/: 主模块目录
  - main.py: 主程序入口
  - config.json: 配置文件
  - sensors/: 传感器相关功能
  - sleep_analysis/: 睡眠分析算法
  - alarm/: 闹钟逻辑
  - utils/: 通用工具
  - tests/: 测试文件

## 安全考虑
- 避免在代码中硬编码敏感信息
- 使用配置文件管理参数
- 验证和清理所有外部输入
- 在文件操作中使用适当的安全措施

## Git 工作流
- 使用功能分支进行开发
- 保持提交信息清晰简洁
- 为复杂更改提供详细说明
- 定期同步主分支的更改