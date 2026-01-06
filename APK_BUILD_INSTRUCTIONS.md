# GWaken Android APK 构建说明

## 项目文件位置

所有Android应用相关文件都位于 `/work/sleep/GWaken-Android/` 目录中：

- `main.py` - Kivy主应用入口文件
- `android_bluetooth_sensor.py` - Android兼容蓝牙传感器模块
- `buildozer.spec` - Buildozer构建配置文件
- `requirements.txt` - Python依赖文件
- `build_apk.sh` - 自动化构建脚本
- `assets/icons/icon.png` - 应用图标
- `assets/icons/splash.png` - 启动画面
- `config.json` - 应用配置文件

## 构建环境要求

在构建APK之前，需要确保系统满足以下要求：

### 系统要求
- Linux系统（推荐Ubuntu 18.04+）
- 至少4GB RAM
- 至少10GB可用磁盘空间
- Python 3.6+

### 安装依赖
```bash
# 安装系统依赖
sudo apt update
sudo apt install -y python3-pip build-essential git zip unzip openjdk-8-jdk

# 安装Buildozer
pip3 install buildozer

# 在Docker环境中运行（推荐）
sudo apt install docker.io
```

## 构建方法

### 方法1：使用构建脚本（推荐）
```bash
cd /work/sleep/GWaken-Android
chmod +x build_apk.sh
./build_apk.sh
```

### 方法2：直接使用Buildozer
```bash
cd /work/sleep/GWaken-Android
buildozer android debug
```

### 方法3：在Docker容器中构建（最推荐）
```bash
cd /work/sleep/GWaken-Android
buildozer android debug --verbose
```

## 构建过程说明

1. **首次构建**：大约需要30-60分钟，因为需要下载Android SDK、NDK等工具
2. **后续构建**：通常在5-10分钟内完成
3. **输出文件**：APK文件将生成在 `GWaken-Android/bin/` 目录中

## APK文件位置

构建成功后，APK文件将位于：
```
/work/sleep/GWaken-Android/bin/
```

文件名格式通常为：
```
GWaken-Android-1.0.0-debug.apk
```

## 测试APK

1. 将APK文件传输到Android设备
2. 在设备上安装APK（可能需要允许安装未知来源的应用）
3. 运行应用并测试功能

## 常见问题

### 1. 权限问题
如果遇到权限错误，在构建时使用 `--allow-unrelated-histories` 参数

### 2. 内存不足
构建过程需要较多内存，如果遇到内存不足错误，请确保有至少4GB可用内存

### 3. 网络问题
构建过程需要下载大量文件，确保网络连接稳定

### 4. 构建失败
如果构建失败，请检查错误信息并：
- 确保所有依赖已正确安装
- 检查网络连接
- 确保有足够的磁盘空间

## 应用功能

构建的APK包含以下功能：
- 实时睡眠阶段监测（清醒、浅睡、深睡、REM睡眠）
- 智能唤醒功能
- 心率和体动数据可视化
- 蓝牙传感器数据接入（支持红米手环2）
- 移动优化的用户界面

## 自定义配置

如需自定义应用信息，可修改 `buildozer.spec` 文件中的以下参数：
- `title` - 应用名称
- `package.name` - 包名
- `version` - 应用版本
- `android.permissions` - 应用权限

## 故障排除

如果构建过程中遇到问题：

1. 检查 `buildozer.spec` 配置是否正确
2. 确保所有系统依赖已安装
3. 查看Buildozer日志获取详细错误信息
4. 尝试清理构建缓存：`buildozer android clean`

## 支持

如需帮助，请参考：
- [Buildozer官方文档](https://buildozer.readthedocs.io/)
- [Kivy官方文档](https://kivy.org/doc/stable/)
- 项目README文件