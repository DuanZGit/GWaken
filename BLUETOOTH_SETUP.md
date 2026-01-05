# 红米手环2蓝牙连接设置指南

## 安卓手机蓝牙连接步骤

### 1. 准备工作
1. 确保红米手环2已充电并开机
2. 在安卓手机上打开"小米运动健康"App并连接手环
3. 确保手环的蓝牙功能已启用

### 2. 配置文件设置
编辑 `sleep_monitor/config.json`：
```json
{
  "device_settings": {
    "sensor_type": "bluetooth",
    "device_model": "Redmi Band 2", 
    "device_name": "Redmi Band 2",
    "bluetooth_address": "",  // 留空，程序会自动搜索
    "max_battery_usage": 20,
    "data_sync_interval": 300
  }
}
```

### 3. 运行系统

#### 方式一：直接运行监测程序
```bash
cd /work/sleep
PYTHONPATH=. python3 -m sleep_monitor.main
```

#### 方式二：启动Web API（推荐）
```bash
cd /work/sleep
PYTHONPATH=. python3 -m sleep_monitor.run_api 5000
```

### 4. 通过API连接手环

#### 步骤1：搜索可用设备
```bash
curl -X GET http://localhost:5000/api/bluetooth/devices
```

响应示例：
```json
{
  "success": true,
  "devices": [
    {
      "address": "AA:BB:CC:DD:EE:FF",
      "name": "Redmi Band 2",
      "is_redmi_band": true
    }
  ],
  "timestamp": "2023-12-07T21:00:00.000000"
}
```

#### 步骤2：连接到手环
```bash
curl -X POST http://localhost:5000/api/bluetooth/connect \
  -H "Content-Type: application/json" \
  -d '{
    "device_address": "AA:BB:CC:DD:EE:FF",
    "device_name": "Redmi Band 2"
  }'
```

### 5. 使用Web界面（推荐）

1. 启动API服务：`python3 -m sleep_monitor.run_api`
2. 在浏览器中访问：`http://<your-server-ip>:5000`
3. 点击"获取系统状态"检查连接
4. 使用"搜索设备"功能查找手环
5. 手动连接到手环设备

### 6. 数据监测

连接成功后，系统会：
- 实时获取心率和体动数据
- 检测睡眠阶段（深睡、浅睡、REM、清醒）
- 在浅睡眠阶段智能唤醒
- 记录睡眠质量数据

### 7. 故障排除

#### 常见问题：

1. **无法搜索到设备**：
   - 确保手环在手机蓝牙范围内（<10米）
   - 确保手环蓝牙未被其他设备连接
   - 检查系统蓝牙服务是否运行

2. **连接失败**：
   - 检查设备地址是否正确
   - 确认手环未被其他应用独占连接
   - 重启手环和手机蓝牙

3. **数据读取异常**：
   - 系统会自动回退到模拟模式
   - 检查蓝牙信号强度
   - 确认手环传感器正常工作

### 8. 安全注意事项

- 连接仅在局域网内进行，确保网络安全
- 设备配对码不会被存储
- 所有健康数据仅在本地处理

### 9. 高级配置

如需手动指定蓝牙地址，请先使用搜索功能获取地址：
```bash
# 在系统中搜索设备
sudo hcitool scan
```

然后在配置文件中指定：
```json
{
  "device_settings": {
    "bluetooth_address": "AA:BB:CC:DD:EE:FF",
    "device_name": "Redmi Band 2"
  }
}
```

### 10. 优化建议

- 在睡眠监测期间保持手机与手环的距离稳定
- 避免在监测期间使用其他蓝牙应用
- 定期同步手环固件以获得最佳兼容性