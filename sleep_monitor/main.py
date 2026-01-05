#!/usr/bin/env python3
"""
红米手环2智能睡眠监测系统主程序

本程序实现睡眠阶段检测和智能唤醒功能
 """
import time
import json
import logging
from datetime import datetime

# 按优先级尝试导入传感器模块
SENSOR_TYPE = None
sensor_module = None

# 首先尝试导入蓝牙传感器（最高优先级）
try:
    from sleep_monitor.sensors.bluetooth_sensor import BluetoothSensor
    SENSOR_TYPE = 'bluetooth'
    sensor_module = BluetoothSensor
    print("蓝牙传感器模块已加载")
except ImportError as e:
    print(f"蓝牙传感器模块不可用: {e}")

# 如果蓝牙不可用，尝试硬件传感器
if SENSOR_TYPE is None:
    try:
        from sleep_monitor.sensors.hardware_sensor import HardwareSensor
        SENSOR_TYPE = 'hardware'
        sensor_module = HardwareSensor
        print("硬件传感器模块已加载")
    except ImportError as e:
        print(f"硬件传感器模块不可用: {e}")

# 如果都不行，使用模拟器
if SENSOR_TYPE is None:
    from sleep_monitor.sensors.sensor_simulator import SensorSimulator
    SENSOR_TYPE = 'simulation'
    sensor_module = SensorSimulator
    print("使用传感器模拟器")

from sleep_monitor.sleep_analysis.sleep_stage_detector import SleepStageDetector
from sleep_monitor.alarm.smart_alarm import SmartAlarm


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_config():
    """加载配置文件"""
    import os
    from pathlib import Path
    
    # 首先尝试在当前目录查找
    config_paths = [
        'config.json',  # 当前目录
        os.path.join(os.path.dirname(__file__), 'config.json'),  # sleep_monitor目录
    ]
    
    for config_path in config_paths:
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                logger.info(f"成功加载配置文件: {config_path}")
                return json.load(f)
        except FileNotFoundError:
            continue
    
    logger.warning("配置文件 config.json 未找到，使用默认配置")
    return {
        "sleep_detection": {
            "sampling_rate": 60,  # 采样率（秒）
            "deep_sleep_hr_threshold": 60,  # 深度睡眠心率阈值
            "light_sleep_hr_threshold": 70,  # 浅度睡眠心率阈值
            "movement_threshold": 5  # 体动阈值
        },
        "alarm_settings": {
            "wake_time": "07:00",  # 默认唤醒时间
            "alarm_window": 30,  # 唤醒时间窗口（分钟）
            "alarm_duration": 5  # 闹钟持续时间（分钟）
        }
    }


def main():
    """主程序入口"""
    logger.info("红米手环2智能睡眠监测系统启动")
    
    # 加载配置
    config = load_config()
    
    # 根据配置决定使用哪种传感器
    device_settings = config.get('device_settings', {})
    preferred_sensor_type = device_settings.get('sensor_type', 'bluetooth')  # 默认使用蓝牙
    
    logger.info(f"使用传感器类型: {SENSOR_TYPE} (配置要求: {preferred_sensor_type})")
    
    # 初始化传感器（按优先级选择，但优先满足配置要求）
    if SENSOR_TYPE == 'bluetooth' and preferred_sensor_type in ['bluetooth', 'auto']:
        logger.info("初始化蓝牙传感器")
        sensor = BluetoothSensor(config)
    elif SENSOR_TYPE == 'hardware' and preferred_sensor_type in ['hardware', 'api', 'auto']:
        logger.info("初始化硬件传感器")
        sensor = HardwareSensor(config)
    else:
        logger.info("初始化传感器模拟器")
        sensor = SensorSimulator(config)
    
    sleep_detector = SleepStageDetector(config)
    smart_alarm = SmartAlarm(config)
    
    logger.info("系统初始化完成，开始监测睡眠...")
    
    try:
        # 模拟睡眠监测过程
        sleep_data = []
        current_time = datetime.now()
        
        # 模拟一晚的睡眠数据（实际应用中会从手环获取）
        for i in range(480):  # 模拟8小时睡眠，每分钟采集一次数据
            # 获取传感器数据（真实或模拟）
            sensor_data = sensor.get_sensor_data()
            
            # 检测睡眠阶段
            sleep_stage = sleep_detector.detect_stage(sensor_data)
            
            # 记录数据
            sleep_data.append({
                'timestamp': datetime.now().isoformat(),
                'heart_rate': sensor_data['heart_rate'],
                'movement': sensor_data['movement'],
                'sleep_stage': sleep_stage
            })
            
            # 检查是否需要唤醒
            if smart_alarm.should_wake_up(sleep_stage, current_time):
                logger.info(f"检测到浅睡眠阶段，在 {current_time.strftime('%H:%M')} 唤醒用户")
                smart_alarm.trigger_alarm()
                break
            
            # 模拟时间流逝
            time.sleep(0.01)  # 加速模拟
            current_time = datetime.fromtimestamp(current_time.timestamp() + 60)  # 增加1分钟
            
            if i % 60 == 0:  # 每小时报告一次
                logger.info(f"睡眠监测进行中... 当前阶段: {sleep_stage}")
    
    except KeyboardInterrupt:
        logger.info("用户中断程序")
    except Exception as e:
        logger.error(f"程序运行出错: {e}")
    
    logger.info("睡眠监测完成")


if __name__ == "__main__":
    main()