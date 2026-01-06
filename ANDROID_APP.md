# GWaken Android APK 开发方案

## 概述
将GWaken智能睡眠监测系统打包为Android APK应用，使用户可以直接在手机上使用睡眠监测功能。

## 技术选型

### 方案1: 使用 Kivy + Buildozer (推荐)
- **Kivy**: Python GUI框架，支持Android
- **Buildozer**: 自动化打包工具
- **P4A (python-for-android)**: Python到Android的编译工具

### 方案2: 使用 BeeWare
- **Toga**: Python原生GUI工具包
- **Briefcase**: 应用打包工具

### 方案3: WebView方案
- 将Web API包装成WebView应用
- 使用Flask作为后端服务

## 开发步骤

### 1. 项目结构
```
GWaken-Android/
├── main.py                 # Kivy应用主入口
├── buildozer.spec          # Buildozer配置文件
├── requirements.txt        # 依赖文件
├── src/
│   ├── android/
│   └── python/
├── assets/
│   ├── icons/
│   └── splash/
└── README.md
```

### 2. 创建Kivy应用主文件
```python
# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import time
import json
from datetime import datetime
import threading

# 导入GWaken核心功能
from sleep_monitor.sleep_analysis.sleep_stage_detector import SleepStageDetector
from sleep_monitor.alarm.smart_alarm import SmartAlarm
from sleep_monitor.sensors.sensor_simulator import SensorSimulator

class GWakenApp(App):
    def build(self):
        self.title = 'GWaken - 智能睡眠监测'
        
        # 创建主布局
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题
        title = Label(text='GWaken 智能睡眠监测', size_hint_y=None, height=50)
        layout.add_widget(title)
        
        # 状态显示
        self.status_label = Label(text='就绪', size_hint_y=None, height=40)
        layout.add_widget(self.status_label)
        
        # 传感器数据
        self.sensor_data_label = Label(text='心率: -, 体动: -', size_hint_y=None, height=40)
        layout.add_widget(self.sensor_data_label)
        
        # 睡眠阶段
        self.sleep_stage_label = Label(text='睡眠阶段: -', size_hint_y=None, height=40)
        layout.add_widget(self.sleep_stage_label)
        
        # 控制按钮
        control_layout = BoxLayout(size_hint_y=None, height=50, spacing=5)
        
        self.start_button = Button(text='开始监测')
        self.start_button.bind(on_press=self.start_monitoring)
        control_layout.add_widget(self.start_button)
        
        self.stop_button = Button(text='停止监测')
        self.stop_button.bind(on_press=self.stop_monitoring)
        control_layout.add_widget(self.stop_button)
        
        layout.add_widget(control_layout)
        
        # 初始化组件
        self.config = self.load_config()
        self.detector = SleepStageDetector(self.config)
        self.alarm = SmartAlarm(self.config)
        self.sensor = SensorSimulator(self.config)
        
        self.monitoring = False
        self.monitoring_thread = None
        
        return layout
    
    def load_config(self):
        """加载配置"""
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # 默认配置
            return {
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
                }
            }
    
    def start_monitoring(self, instance):
        """开始监测"""
        if not self.monitoring:
            self.monitoring = True
            self.status_label.text = '监测中...'
            self.start_button.disabled = True
            self.monitoring_thread = threading.Thread(target=self.monitoring_loop)
            self.monitoring_thread.daemon = True
            self.monitoring_thread.start()
    
    def stop_monitoring(self, instance):
        """停止监测"""
        self.monitoring = False
        self.status_label.text = '已停止'
        self.start_button.disabled = False
    
    def monitoring_loop(self):
        """监测循环"""
        while self.monitoring:
            try:
                # 获取传感器数据
                sensor_data = self.sensor.get_sensor_data()
                
                # 检测睡眠阶段
                sleep_stage = self.detector.detect_stage(sensor_data)
                
                # 更新UI
                Clock.schedule_once(lambda dt: self.update_ui(sensor_data, sleep_stage))
                
                # 检查是否需要唤醒
                current_time = datetime.now()
                if self.alarm.should_wake_up(sleep_stage, current_time):
                    Clock.schedule_once(lambda dt: self.trigger_alarm())
                
                time.sleep(2)  # 更新间隔
                
            except Exception as e:
                print(f"监测循环错误: {e}")
                break
    
    def update_ui(self, sensor_data, sleep_stage):
        """更新UI"""
        self.sensor_data_label.text = f'心率: {sensor_data["heart_rate"]}, 体动: {sensor_data["movement"]:.2f}'
        self.sleep_stage_label.text = f'睡眠阶段: {sleep_stage}'
    
    def trigger_alarm(self):
        """触发闹钟"""
        self.status_label.text = '唤醒中...'

GWakenApp().run()
```

### 3. Buildozer配置文件
```spec
[app]
title = GWaken Sleep Monitor
package.name = g_waken
package.domain = com.anomalyai

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,txt

version = 1.0.0
requirements = python3,kivy,flask,requests,pybluez

[buildozer]
log_level = 2

[app] 
android.permissions = BLUETOOTH, BLUETOOTH_ADMIN, ACCESS_FINE_LOCATION, WAKE_LOCK, RECEIVE_BOOT_COMPLETED
android.api = 27
android.minapi = 21
android.ndk = 23b
android.sdk = 30

# 图标和启动画面
android.application.name = GWaken
android.icon.filename = %(source.dir)s/assets/icons/icon.png
android.presplash.filename = %(source.dir)s/assets/icons/splash.png
```

### 4. 依赖文件
```txt
# requirements.txt
kivy==2.1.0
flask==2.3.3
requests==2.31.0
pybluez==0.23
```

### 5. 构建脚本
```bash
#!/bin/bash
# build_apk.sh

echo "开始构建GWaken Android APK..."

# 安装buildozer
pip install buildozer

# 初始化buildozer (如果还没有spec文件)
if [ ! -f buildozer.spec ]; then
    buildozer init
fi

# 构建APK
buildozer android debug

echo "APK构建完成，位于 bin/ 目录下"
```

## 特殊考虑

### 蓝牙权限
由于需要连接红米手环2，应用需要以下权限：
- BLUETOOTH
- BLUETOOTH_ADMIN
- ACCESS_FINE_LOCATION (用于蓝牙扫描)

### 后台服务
- 睡眠监测需要在后台持续运行
- 使用Android服务确保长时间监测

### 电池优化
- 优化算法减少电池消耗
- 提供低功耗模式

## 实现步骤

### 步骤1: 准备开发环境
```bash
# 安装Docker (如果使用容器化构建)
sudo apt-get install docker.io

# 安装Buildozer
pip install buildozer

# 初始化项目
cd /path/to/gwaken
buildozer init
```

### 步骤2: 配置项目
- 复制GWaken核心代码到Android项目
- 配置buildozer.spec文件
- 准备图标和资源文件

### 步骤3: 构建APK
```bash
buildozer android debug
```

### 步骤4: 测试和部署
- 在Android设备上安装测试
- 调试蓝牙连接功能
- 优化性能

## 挑战与解决方案

### 挑战1: Python在Android上的性能
- **解决方案**: 使用Cython优化核心算法

### 挑战2: 蓝牙连接
- **解决方案**: 使用Android蓝牙API，通过JNI调用

### 挑战3: 后台运行限制
- **解决方案**: 使用Android服务和唤醒锁

## 项目文件清单

创建以下文件来实现Android应用：

1. `main.py` - Kivy应用主文件
2. `buildozer.spec` - 构建配置
3. `requirements.txt` - 依赖列表
4. `assets/icons/icon.png` - 应用图标
5. `assets/icons/splash.png` - 启动画面
6. `build_apk.sh` - 构建脚本

## 部署说明

### 开发环境要求
- Linux系统 (推荐Ubuntu 20.04+)
- Docker (用于交叉编译)
- Python 3.6+
- 至少4GB内存和10GB磁盘空间

### 构建时间
- 首次构建: 30-60分钟 (需要下载Android SDK/NDK)
- 后续构建: 5-10分钟

这样，您就可以将GWaken项目打包成Android APK，让用户在手机上直接使用智能睡眠监测功能。