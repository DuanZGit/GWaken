"""
红米手环2传感器数据模拟器

模拟红米手环2的心率和体动传感器数据
"""
import random
from datetime import datetime, timedelta
import json


class SensorSimulator:
    """传感器数据模拟器"""
    
    def __init__(self, config):
        """
        初始化模拟器
        :param config: 配置参数
        """
        self.config = config
        self.sleep_phase = "awake"  # 当前睡眠阶段
        self.last_heart_rate = 75  # 上次心率值
        self.sleep_start_time = None
        self.current_time_offset = 0  # 当前时间偏移量（秒）
        
        # 睡眠阶段时间分布（秒）
        self.sleep_phase_durations = {
            "awake": 300,  # 入睡前清醒期，5分钟
            "light_sleep": 1200,  # 浅睡眠期，20分钟
            "deep_sleep": 1800,  # 深睡眠期，30分钟
            "rem_sleep": 900  # REM睡眠期，15分钟
        }
        
        # 睡眠阶段心率范围（BPM）
        self.heart_rate_ranges = {
            "awake": (70, 85),
            "light_sleep": (65, 75),
            "deep_sleep": (55, 65),
            "rem_sleep": (65, 75)
        }
        
        # 睡眠阶段体动范围（任意单位）
        self.movement_ranges = {
            "awake": (5, 15),
            "light_sleep": (2, 8),
            "deep_sleep": (0, 3),
            "rem_sleep": (3, 10)
        }
    
    def get_sensor_data(self):
        """
        获取模拟传感器数据
        :return: 包含心率和体动数据的字典
        """
        # 更新睡眠阶段（模拟睡眠周期）
        self._update_sleep_phase()
        
        # 生成心率数据（模拟红米手环2心率传感器）
        heart_rate = self._generate_heart_rate()
        
        # 生成体动数据（模拟加速度计）
        movement = self._generate_movement()
        
        # 模拟传感器噪声
        heart_rate = self._add_sensor_noise(heart_rate, 2)  # 心率噪声±2
        movement = max(0, self._add_sensor_noise(movement, 1))  # 体动噪声±1
        
        # 确保心率在合理范围内
        heart_rate = max(40, min(120, heart_rate))
        movement = max(0, movement)
        
        sensor_data = {
            'timestamp': datetime.now().isoformat(),
            'heart_rate': round(heart_rate, 1),
            'movement': round(movement, 2),
            'sleep_phase': self.sleep_phase
        }
        
        # 增加时间偏移
        self.current_time_offset += self.config['sleep_detection']['sampling_rate']
        
        return sensor_data
    
    def _update_sleep_phase(self):
        """更新当前睡眠阶段"""
        # 模拟睡眠周期：清醒 -> 浅睡 -> 深睡 -> 浅睡 -> REM
        total_time = self.current_time_offset
        
        # 简化的睡眠周期模拟
        if total_time < self.sleep_phase_durations['awake']:
            self.sleep_phase = "awake"
        elif total_time < self.sleep_phase_durations['awake'] + self.sleep_phase_durations['light_sleep']:
            self.sleep_phase = "light_sleep"
        elif total_time < self.sleep_phase_durations['awake'] + self.sleep_phase_durations['light_sleep'] + self.sleep_phase_durations['deep_sleep']:
            self.sleep_phase = "deep_sleep"
        elif total_time < self.sleep_phase_durations['awake'] + self.sleep_phase_durations['light_sleep'] + self.sleep_phase_durations['deep_sleep'] + self.sleep_phase_durations['rem_sleep']:
            # 根据时间在周期内循环
            cycle_time = (total_time - (self.sleep_phase_durations['awake'] + self.sleep_phase_durations['light_sleep'] + self.sleep_phase_durations['deep_sleep'])) % (self.sleep_phase_durations['light_sleep'] + self.sleep_phase_durations['rem_sleep'])
            if cycle_time < self.sleep_phase_durations['light_sleep']:
                self.sleep_phase = "light_sleep"
            else:
                self.sleep_phase = "rem_sleep"
        else:
            # 循环睡眠周期
            cycle_time = (total_time - self.sleep_phase_durations['awake']) % (self.sleep_phase_durations['light_sleep'] + self.sleep_phase_durations['deep_sleep'] + self.sleep_phase_durations['rem_sleep'])
            if cycle_time < self.sleep_phase_durations['light_sleep']:
                self.sleep_phase = "light_sleep"
            elif cycle_time < self.sleep_phase_durations['light_sleep'] + self.sleep_phase_durations['deep_sleep']:
                self.sleep_phase = "deep_sleep"
            else:
                self.sleep_phase = "light_sleep"
    
    def _generate_heart_rate(self):
        """根据睡眠阶段生成心率数据"""
        hr_range = self.heart_rate_ranges[self.sleep_phase]
        base_hr = random.uniform(hr_range[0], hr_range[1])
        
        # 添加生理变化（心率变异性）
        variation = random.uniform(-3, 3)
        heart_rate = base_hr + variation
        
        # 确保心率变化不会过于剧烈
        max_change = 5  # 每分钟最大变化
        if self.last_heart_rate is not None:
            change = heart_rate - self.last_heart_rate
            if abs(change) > max_change:
                if change > 0:
                    heart_rate = self.last_heart_rate + max_change
                else:
                    heart_rate = self.last_heart_rate - max_change
        
        self.last_heart_rate = heart_rate
        return heart_rate
    
    def _generate_movement(self):
        """根据睡眠阶段生成体动数据"""
        move_range = self.movement_ranges[self.sleep_phase]
        movement = random.uniform(move_range[0], move_range[1])
        
        # 模拟翻身等突发动作
        if self.sleep_phase != "awake" and random.random() < 0.05:  # 5%概率有较大动作
            movement = random.uniform(move_range[1], move_range[1] * 2)
        
        return movement
    
    def _add_sensor_noise(self, value, noise_level):
        """为传感器数据添加噪声"""
        noise = random.uniform(-noise_level, noise_level)
        return value + noise
    
    def set_sleep_start_time(self, start_time):
        """设置睡眠开始时间"""
        self.sleep_start_time = start_time
    
    def get_device_info(self):
        """获取设备信息"""
        return {
            'connected': True,
            'device_model': 'Sensor Simulator',
            'device_address': 'N/A',
            'device_name': '模拟传感器',
            'use_simulation': True,
            'bluetooth_available': False
        }