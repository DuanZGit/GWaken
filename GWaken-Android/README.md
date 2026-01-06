# GWaken Android - 智能睡眠监测应用

## 项目概述

GWaken Android是基于原始GWaken智能睡眠监测系统的Android应用版本。该应用使用Kivy框架开发，能够监测用户的睡眠阶段并提供智能唤醒功能。

## 功能特性

- 实时睡眠阶段监测（清醒、浅睡、深睡、REM睡眠）
- 基于睡眠周期的智能唤醒
- 心率和体动数据可视化
- 蓝牙传感器数据接入（支持红米手环2）
- Android平台优化的UI界面

## 技术架构

- **UI框架**: Kivy
- **后端逻辑**: Python (继承原GWaken系统)
- **蓝牙接入**: Android JNI/Bluetooth API (通过Kivy)
- **构建工具**: Buildozer
- **平台**: Android (API 21+)

## 项目结构

```
GWaken-Android/
├── main.py                 # Kivy应用主入口
├── android_bluetooth_sensor.py  # Android兼容蓝牙传感器模块
├── buildozer.spec          # Buildozer配置文件
├── requirements.txt        # Python依赖
├── config.json             # 应用配置
├── build_apk.sh            # 构建脚本
├── assets/
│   └── icons/
│       ├── icon.png        # 应用图标
│       └── splash.png      # 启动画面
└── README.md
```

## Android蓝牙适配

由于Android 6.0+的权限和蓝牙API限制，应用使用了以下策略：

1. **权限管理**: 请求必要的蓝牙权限（BLUETOOTH, BLUETOOTH_ADMIN, ACCESS_FINE_LOCATION）
2. **平台检测**: 自动检测运行平台并选择合适的传感器实现
3. **回退机制**: 当蓝牙不可用时，使用高质量的模拟数据
4. **后台服务**: 支持后台持续监测

## 构建说明

### 环境要求
- Linux系统 (推荐Ubuntu 20.04+)
- Python 3.6+
- Docker (用于交叉编译)
- 至少4GB内存和10GB磁盘空间

### 构建步骤

1. 安装Buildozer:
```bash
pip install buildozer
```

2. 初始化项目 (如果需要):
```bash
buildozer init
```

3. 构建APK:
```bash
buildozer android debug
```

生成的APK文件将位于 `bin/` 目录中。

### 注意事项

- 首次构建需要下载Android SDK/NDK，可能需要30-60分钟
- 后续构建通常在5-10分钟内完成
- 构建过程需要稳定的网络连接

## 配置说明

应用使用与原GWaken系统兼容的配置文件格式，主要配置项包括：

- `sleep_detection`: 睡眠检测参数
- `alarm_settings`: 闹钟设置
- `device_settings`: 设备配置

## 传感器数据模拟

在以下情况下，应用将使用高质量的模拟数据：
- 蓝牙权限被拒绝
- 目标设备不可用
- Android平台上蓝牙API限制

模拟数据考虑了昼夜节律和睡眠周期的特征，确保应用功能完整性。

## 部署与测试

1. 构建完成后，将APK安装到Android设备
2. 首次运行时允许所需的蓝牙权限
3. 应用会自动检测并连接到红米手环2
4. 如需手动配置设备地址，可在配置文件中修改

## 维护与更新

项目继承了原始GWaken系统的所有核心算法和逻辑，确保睡眠检测的准确性。Android特定的优化主要集中在UI和蓝牙连接方面。

## 许可证

遵循原始GWaken项目的许可证协议。