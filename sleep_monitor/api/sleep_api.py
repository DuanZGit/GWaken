"""
红米手环2睡眠监测API接口

提供与小米运动健康App或设备同步的接口
"""
from flask import Flask, request, jsonify, render_template_string
import json
import logging
from datetime import datetime, timedelta
import os
import importlib

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 全局实例
sensor = None
detector = None
alarm = None
config = None

def init_system():
    """初始化系统组件"""
    global sensor, detector, alarm, config
    
    # 加载配置
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        logger.warning("配置文件 config.json 未找到，使用默认配置")
        config = {
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
                "api_base_url": "http://localhost:5000/api",
                "access_token": "",
                "device_id": "",
                "bluetooth_address": "",
                "device_name": "Redmi Band 2",
                "sensor_type": "bluetooth"
            }
        }
    
    # 根据配置决定使用哪种传感器
    device_settings = config.get('device_settings', {})
    preferred_sensor_type = device_settings.get('sensor_type', 'bluetooth')
    
    # 动态导入传感器模块 - 使用相对导入
    if preferred_sensor_type == 'bluetooth':
        from ..sensors.bluetooth_sensor import BluetoothSensor
        sensor = BluetoothSensor(config)
    elif preferred_sensor_type == 'hardware':
        from ..sensors.hardware_sensor import HardwareSensor
        sensor = HardwareSensor(config)
    else:  # 默认使用蓝牙
        from ..sensors.bluetooth_sensor import BluetoothSensor
        sensor = BluetoothSensor(config)
    
    from ..sleep_analysis.sleep_stage_detector import SleepStageDetector
    from ..alarm.smart_alarm import SmartAlarm
    
    detector = SleepStageDetector(config)
    alarm = SmartAlarm(config)

@app.route('/')
def index():
    """主页"""
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>红米手环2睡眠监测系统</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
            .btn { padding: 10px 15px; margin: 5px; background: #007bff; color: white; border: none; border-radius: 3px; cursor: pointer; }
            .btn:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <h1>红米手环2睡眠监测系统</h1>
        
        <div class="section">
            <h2>系统状态</h2>
            <button class="btn" onclick="getSystemStatus()">获取系统状态</button>
            <div id="status"></div>
        </div>
        
        <div class="section">
            <h2>传感器数据</h2>
            <button class="btn" onclick="getSensorData()">获取传感器数据</button>
            <div id="sensor-data"></div>
        </div>
        
        <div class="section">
            <h2>睡眠分析</h2>
            <button class="btn" onclick="getSleepAnalysis()">获取睡眠分析</button>
            <div id="sleep-analysis"></div>
        </div>
        
        <div class="section">
            <h2>设备控制</h2>
            <button class="btn" onclick="syncDevice()">同步设备数据</button>
            <button class="btn" onclick="getDeviceInfo()">获取设备信息</button>
            <div id="device-info"></div>
        </div>
        
        <script>
            async function getSystemStatus() {
                const response = await fetch('/api/status');
                const data = await response.json();
                document.getElementById('status').innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            }
            
            async function getSensorData() {
                const response = await fetch('/api/sensor_data');
                const data = await response.json();
                document.getElementById('sensor-data').innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            }
            
            async function getSleepAnalysis() {
                const response = await fetch('/api/sleep_analysis');
                const data = await response.json();
                document.getElementById('sleep-analysis').innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            }
            
            async function syncDevice() {
                const response = await fetch('/api/device/sync', { method: 'POST' });
                const data = await response.json();
                document.getElementById('device-info').innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            }
            
            async function getDeviceInfo() {
                const response = await fetch('/api/device/info');
                const data = await response.json();
                document.getElementById('device-info').innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            }
        </script>
    </body>
    </html>
    ''')

@app.route('/api/status')
def get_status():
    """获取系统状态"""
    global sensor, detector, alarm
    
    if not all([sensor, detector, alarm]):
        init_system()
    
    return jsonify({
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'components': {
            'sensor': sensor.get_device_info() if sensor else None,
            'detector': 'initialized' if detector else 'not initialized',
            'alarm': alarm.get_alarm_status() if alarm else None
        }
    })

@app.route('/api/sensor_data')
def get_sensor_data():
    """获取传感器数据"""
    global sensor
    
    if not sensor:
        init_system()
    
    data = sensor.get_sensor_data()
    return jsonify(data)

@app.route('/api/sleep_analysis', methods=['POST'])
def get_sleep_analysis():
    """获取睡眠阶段分析"""
    global detector
    
    if not detector:
        init_system()
    
    # 从请求获取传感器数据
    sensor_data = request.json or sensor.get_sensor_data() if sensor else {
        'timestamp': datetime.now().isoformat(),
        'heart_rate': 68,
        'movement': 2.5
    }
    
    # 检测睡眠阶段
    sleep_stage = detector.detect_stage(sensor_data)
    
    # 获取睡眠总结
    summary = detector.get_sleep_summary()
    
    return jsonify({
        'sleep_stage': sleep_stage,
        'sensor_data': sensor_data,
        'summary': summary,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/alarm/check', methods=['POST'])
def check_alarm():
    """检查是否应该唤醒"""
    global alarm
    
    if not alarm:
        init_system()
    
    # 获取当前睡眠阶段和时间
    data = request.json or {}
    sleep_stage = data.get('sleep_stage', 'awake')
    current_time_str = data.get('current_time')
    
    if current_time_str:
        current_time = datetime.fromisoformat(current_time_str.replace('Z', '+00:00'))
    else:
        current_time = datetime.now()
    
    should_wake = alarm.should_wake_up(sleep_stage, current_time)
    
    return jsonify({
        'should_wake_up': should_wake,
        'current_time': current_time.isoformat(),
        'sleep_stage': sleep_stage,
        'alarm_status': alarm.get_alarm_status() if alarm else None
    })

@app.route('/api/alarm/trigger', methods=['POST'])
def trigger_alarm():
    """触发闹钟"""
    global alarm
    
    if not alarm:
        init_system()
    
    alarm.trigger_alarm()
    
    return jsonify({
        'success': True,
        'message': '闹钟已触发',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/device/info')
def get_device_info():
    """获取设备信息"""
    global sensor
    
    if not sensor:
        init_system()
    
    return jsonify(sensor.get_device_info())

@app.route('/api/device/sync', methods=['POST'])
def sync_device():
    """同步设备数据"""
    global sensor
    
    if not sensor:
        init_system()
    
    success = sensor.sync_data()
    
    return jsonify({
        'success': success,
        'timestamp': datetime.now().isoformat(),
        'message': '设备数据同步成功' if success else '设备数据同步失败'
    })

@app.route('/api/heart_rate')
def get_heart_rate():
    """获取心率数据（用于模拟API接口）"""
    global sensor
    
    if not sensor:
        init_system()
    
    sensor_data = sensor.get_sensor_data()
    return jsonify({
        'timestamp': sensor_data['timestamp'],
        'heart_rate': sensor_data['heart_rate'],
        'device_id': sensor_data.get('device_id', 'default')
    })

@app.route('/api/movement')
def get_movement():
    """获取体动数据（用于模拟API接口）"""
    global sensor
    
    if not sensor:
        init_system()
    
    sensor_data = sensor.get_sensor_data()
    return jsonify({
        'timestamp': sensor_data['timestamp'],
        'movement': sensor_data['movement'],
        'device_id': sensor_data.get('device_id', 'default')
    })

@app.route('/api/sleep_data')
def get_sleep_data():
    """获取睡眠数据（用于模拟API接口）"""
    global sensor, detector
    
    if not all([sensor, detector]):
        init_system()
    
    sensor_data = sensor.get_sensor_data()
    sleep_stage = detector.detect_stage(sensor_data)
    
    return jsonify({
        'timestamp': sensor_data['timestamp'],
        'heart_rate': sensor_data['heart_rate'],
        'movement': sensor_data['movement'],
        'sleep_stage': sleep_stage,
        'device_id': sensor_data.get('device_id', 'default')
    })

@app.route('/api/bluetooth/devices')
def get_bluetooth_devices():
    """搜索可用的蓝牙设备"""
    try:
        import bluetooth
        logger.info("搜索附近的蓝牙设备...")
        nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True)
        
        devices = []
        for addr, name in nearby_devices:
            device_info = {
                'address': addr,
                'name': name,
                'is_redmi_band': 'Redmi' in name or 'Mi Band' in name or 'Band' in name
            }
            devices.append(device_info)
        
        return jsonify({
            'success': True,
            'devices': devices,
            'timestamp': datetime.now().isoformat()
        })
    except ImportError:
        return jsonify({
            'success': False,
            'message': '蓝牙库未安装',
            'devices': []
        }), 400
    except Exception as e:
        logger.error(f"搜索蓝牙设备失败: {e}")
        return jsonify({
            'success': False,
            'message': str(e),
            'devices': []
        }), 500


@app.route('/api/bluetooth/connect', methods=['POST'])
def connect_bluetooth():
    """连接到蓝牙设备"""
    global sensor
    
    data = request.json or {}
    device_address = data.get('device_address')
    device_name = data.get('device_name', 'Redmi Band 2')
    
    if not device_address:
        return jsonify({
            'success': False,
            'message': '需要提供设备地址'
        }), 400
    
    try:
        # 创建新的蓝牙传感器
        new_config = config or {
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
                "bluetooth_address": device_address,
                "device_name": device_name
            }
        }
        
        new_config['device_settings']['bluetooth_address'] = device_address
        new_config['device_settings']['device_name'] = device_name
        
        # 创建蓝牙传感器
        sensor = BluetoothSensor(new_config)
        
        return jsonify({
            'success': True,
            'message': '蓝牙设备连接成功',
            'device_info': sensor.get_device_info(),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"连接蓝牙设备失败: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


def run_api_server(host='0.0.0.0', port=5000):
    """运行API服务器"""
    init_system()
    logger.info(f"启动睡眠监测API服务器在 {host}:{port}")
    app.run(host=host, port=port, debug=False)

if __name__ == '__main__':
    init_system()
    logger.info("启动睡眠监测API服务器在 http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)