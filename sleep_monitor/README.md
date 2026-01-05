# 红米手环2智能睡眠监测系统

本项目是一个智能睡眠监测系统，专门适配红米手环2设备，能够检测睡眠阶段并在浅睡眠阶段唤醒用户。

## 功能特点

- **睡眠阶段检测**：基于心率和体动数据检测深睡、浅睡、REM等睡眠阶段
- **智能唤醒**：在浅睡眠阶段唤醒用户，提供更舒适的起床体验
- **数据记录**：记录和分析睡眠数据，生成睡眠质量报告
- **红米手环2适配**：模拟红米手环2传感器数据，优化算法以适配设备特性

## 项目结构

```
sleep_monitor/
├── main.py                 # 主程序入口
├── config.json             # 配置文件
├── requirements.txt        # 依赖包列表
├── sensors/                # 传感器模块
│   ├── sensor_simulator.py # 传感器数据模拟器
│   └── __init__.py
├── sleep_analysis/         # 睡眠分析模块
│   ├── sleep_stage_detector.py # 睡眠阶段检测器
│   ├── signal_processor.py     # 信号处理器
│   └── __init__.py
├── alarm/                  # 闹钟模块
│   ├── smart_alarm.py      # 智能闹钟
│   └── __init__.py
├── utils/                  # 工具模块
│   ├── data_logger.py      # 数据记录器
│   ├── time_utils.py       # 时间工具
│   └── __init__.py
├── data/                   # 数据存储目录
└── tests/                  # 测试目录
```

## 安装和运行

### 环境要求

- Python 3.6+

### 安装步骤

1. 克隆项目
2. 安装依赖包：
   ```bash
   pip install -r requirements.txt
   ```

### 运行项目

```bash
python -m sleep_monitor.main
```

## 使用说明

### 配置文件

`config.json` 包含以下配置项：

- `sleep_detection`: 睡眠检测相关参数
  - `sampling_rate`: 数据采样率（秒）
  - `deep_sleep_hr_threshold`: 深度睡眠心率阈值
  - `light_sleep_hr_threshold`: 浅度睡眠心率阈值
  - `movement_threshold`: 体动阈值

- `alarm_settings`: 闹钟设置
  - `wake_time`: 唤醒时间（HH:MM格式）
  - `alarm_window`: 唤醒时间窗口（分钟）
  - `alarm_duration`: 闹钟持续时间（分钟）

- `device_settings`: 设备设置
  - `device_model`: 设备型号
  - `max_battery_usage`: 最大电池使用率
  - `data_sync_interval`: 数据同步间隔（秒）

### 数据导入

由于红米手环2没有公开API，项目支持以下数据获取方式：

1. 通过小米运动健康App导出数据
2. 手动输入睡眠数据
3. 使用传感器模拟器进行测试

## 算法原理

### 睡眠阶段检测

系统基于以下生理指标判断睡眠阶段：

- **深睡眠**：心率较低且稳定（<60 BPM），体动很少
- **浅睡眠**：心率稍有波动（60-70 BPM），体动较少
- **REM睡眠**：心率变化较大，体动中等
- **清醒**：心率较高（>70 BPM），体动频繁

### 智能唤醒逻辑

系统在以下条件下触发唤醒：

1. 当前睡眠阶段为浅睡眠
2. 时间在唤醒窗口内（默认目标时间前30分钟）
3. 接近目标唤醒时间

## 扩展功能

未来可扩展的功能：

- 与小米运动健康App数据同步
- 个性化睡眠分析报告
- 睡眠质量评分系统
- 睡眠建议和改善方案

## 注意事项

1. 本项目为模拟实现，实际使用需要接入红米手环2数据
2. 算法准确性基于模拟数据，实际效果可能因设备差异而异
3. 请确保设备有足够的电量支持整夜监测

## 许可证

本项目为学习和研究用途。