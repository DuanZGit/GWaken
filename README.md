# 红米手环2智能睡眠监测系统

本项目是一个智能睡眠监测系统，专门适配红米手环2设备，能够检测睡眠阶段并在浅睡眠阶段唤醒用户。

## 功能特点

- **睡眠阶段检测**：基于心率和体动数据检测深睡、浅睡、REM等睡眠阶段
- **智能唤醒**：在浅睡眠阶段唤醒用户，提供更舒适的起床体验
- **数据记录**：记录和分析睡眠数据，生成睡眠质量报告
- **红米手环2适配**：支持通过蓝牙连接红米手环2，获取实时传感器数据
- **Web API接口**：提供RESTful API接口，支持远程监控和控制

## 系统架构

```
sleep_monitor/
├── main.py                 # 主程序入口
├── config.json             # 配置文件
├── requirements.txt        # 依赖包列表
├── setup.py               # 安装配置
├── sensors/               # 传感器模块
│   ├── sensor_simulator.py # 传感器数据模拟器
│   ├── bluetooth_sensor.py # 蓝牙传感器
│   ├── hardware_sensor.py # 硬件传感器
│   └── __init__.py
├── sleep_analysis/        # 睡眠分析模块
│   ├── sleep_stage_detector.py # 睡眠阶段检测器
│   ├── signal_processor.py     # 信号处理器
│   └── __init__.py
├── alarm/                 # 闹钟模块
│   ├── smart_alarm.py      # 智能闹钟
│   └── __init__.py
├── api/                   # API接口
│   └── sleep_api.py        # Web API实现
├── utils/                 # 工具模块
│   ├── data_logger.py      # 数据记录器
│   ├── time_utils.py       # 时间工具
│   └── __init__.py
├── data/                  # 数据存储目录
├── docs/                  # 文档目录
└── tests/                 # 测试目录
    └── test_sleep_detector.py
```

## 安装和运行

### 环境要求

- Python 3.6+
- 蓝牙适配器（用于连接手环）

### 安装步骤

1. 克隆项目：
   ```bash
   git clone <repository-url>
   cd sleep-monitor
   ```

2. 安装依赖包：
   ```bash
   pip install -r requirements.txt
   # 或者使用setup.py安装
   pip install -e .
   ```

### 运行方式

#### 方式1：运行主监测程序
```bash
python -m sleep_monitor.main
```

#### 方式2：启动Web API服务
```bash
python -m sleep_monitor.run_api
# 或指定端口
python -m sleep_monitor.run_api 5000
```

API服务启动后，可通过浏览器访问 `http://localhost:5000` 查看Web界面。

## API接口

### 设备管理
- `GET /api/bluetooth/devices` - 搜索可用蓝牙设备
- `POST /api/bluetooth/connect` - 连接蓝牙设备
- `GET /api/device/info` - 获取设备信息
- `POST /api/device/sync` - 同步设备数据

### 数据获取
- `GET /api/sensor_data` - 获取传感器数据
- `GET /api/heart_rate` - 获取心率数据
- `GET /api/movement` - 获取体动数据
- `GET /api/sleep_data` - 获取睡眠数据

### 睡眠分析
- `POST /api/sleep_analysis` - 分析睡眠阶段
- `GET /api/status` - 获取系统状态

## 配置文件

`config.json` 包含以下配置项：

```json
{
  "sleep_detection": {
    "sampling_rate": 60,
    "deep_sleep_hr_threshold": 60,
    "light_sleep_hr_threshold": 70,
    "movement_threshold": 5
  },
  "alarm_settings": {
    "wake_time": "07:00",
    "alarm_window": 30,
    "alarm_duration": 5
  },
  "device_settings": {
    "device_model": "Redmi Band 2",
    "max_battery_usage": 20,
    "data_sync_interval": 300,
    "bluetooth_address": "",
    "device_name": "Redmi Band 2",
    "sensor_type": "bluetooth"
  }
}
```

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

## 蓝牙连接说明

详细蓝牙连接说明请参考 [BLUETOOTH_SETUP.md](BLUETOOTH_SETUP.md) 文件。

## 测试

运行单元测试：
```bash
python -m unittest discover -s sleep_monitor.tests -p "test_*.py" -v
```

## 部署

### 生产环境部署
使用WSGI服务器（如Gunicorn）部署API服务：
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 sleep_monitor.api.sleep_api:app
```

## 许可证

本项目仅供学习和研究使用。