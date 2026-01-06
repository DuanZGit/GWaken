# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import time
import json
from datetime import datetime
import threading
import os

# 导入GWaken核心功能
from sleep_monitor.sleep_analysis.sleep_stage_detector import SleepStageDetector
from sleep_monitor.alarm.smart_alarm import SmartAlarm

# 根据平台选择传感器
try:
    # 尝试使用Android兼容的蓝牙传感器
    from android_bluetooth_sensor import AndroidBluetoothManager
    sensor_manager = AndroidBluetoothManager
    print("使用Android兼容蓝牙传感器")
except ImportError:
    # 回退到模拟传感器
    from sleep_monitor.sensors.sensor_simulator import SensorSimulator
    print("使用模拟传感器")

class GWakenApp(App):
    def build(self):
        self.title = 'GWaken - 智能睡眠监测'
        
        # 创建主布局
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题
        title = Label(text='GWaken 智能睡眠监测', size_hint_y=None, height=50, font_size=20)
        layout.add_widget(title)
        
        # 状态显示
        self.status_label = Label(text='就绪', size_hint_y=None, height=40)
        layout.add_widget(self.status_label)
        
        # 传感器数据显示
        self.sensor_data_label = Label(text='心率: -, 体动: -', size_hint_y=None, height=40)
        layout.add_widget(self.sensor_data_label)
        
        # 睡眠阶段显示
        self.sleep_stage_label = Label(text='睡眠阶段: -', size_hint_y=None, height=40)
        layout.add_widget(self.sleep_stage_label)
        
        # 睡眠总结显示
        self.summary_label = Label(text='睡眠总结: 等待数据...', size_hint_y=None, height=40)
        layout.add_widget(self.summary_label)
        
        # 滚动视图用于显示详细信息
        scroll = ScrollView(size_hint_y=1)
        self.details_label = Label(text='详细信息将在这里显示...', text_size=(400, None), halign='left', valign='top')
        scroll.add_widget(self.details_label)
        layout.add_widget(scroll)
        
        # 控制按钮布局
        control_layout = BoxLayout(size_hint_y=None, height=50, spacing=5)
        
        self.start_button = Button(text='开始监测')
        self.start_button.bind(on_press=self.start_monitoring)
        control_layout.add_widget(self.start_button)
        
        self.stop_button = Button(text='停止监测', disabled=True)
        self.stop_button.bind(on_press=self.stop_monitoring)
        control_layout.add_widget(self.stop_button)
        
        layout.add_widget(control_layout)
        
        # 初始化组件
        self.config = self.load_config()
        self.detector = SleepStageDetector(self.config)
        self.alarm = SmartAlarm(self.config)
        
        # 根据可用的传感器模块初始化传感器
        try:
            # 尝试使用Android兼容的蓝牙传感器
            from android_bluetooth_sensor import AndroidBluetoothManager
            sensor_manager = AndroidBluetoothManager(self.config)
            self.sensor = sensor_manager.get_sensor()
            print("已初始化Android兼容蓝牙传感器")
        except ImportError:
            # 回退到模拟传感器
            from sleep_monitor.sensors.sensor_simulator import SensorSimulator
            self.sensor = SensorSimulator(self.config)
            print("已初始化模拟传感器")
        
        self.monitoring = False
        self.monitoring_thread = None
        
        return layout
    
    def load_config(self):
        """加载配置"""
        try:
            # 在Android环境中，尝试从应用目录加载配置
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
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
            self.stop_button.disabled = False
            self.monitoring_thread = threading.Thread(target=self.monitoring_loop)
            self.monitoring_thread.daemon = True
            self.monitoring_thread.start()
    
    def stop_monitoring(self, instance):
        """停止监测"""
        self.monitoring = False
        self.status_label.text = '已停止'
        self.start_button.disabled = False
        self.stop_button.disabled = True
    
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
                
                # 根据配置的采样率更新间隔
                time.sleep(self.config['sleep_detection']['sampling_rate'])
                
            except Exception as e:
                print(f"监测循环错误: {e}")
                break
    
    def update_ui(self, sensor_data, sleep_stage):
        """更新UI"""
        self.sensor_data_label.text = f'心率: {sensor_data["heart_rate"]}, 体动: {sensor_data["movement"]:.2f}'
        self.sleep_stage_label.text = f'睡眠阶段: {sleep_stage}'
        
        # 更新睡眠总结
        summary = self.detector.get_sleep_summary()
        if summary:
            self.summary_label.text = f'睡眠总结: 平均心率 {summary["avg_heart_rate"]}, 体动 {summary["avg_movement"]:.2f}'
        
        # 更新详细信息
        details_text = f'时间: {sensor_data["timestamp"]}\n'
        details_text += f'当前阶段: {sleep_stage}\n'
        details_text += f'心率: {sensor_data["heart_rate"]} BPM\n'
        details_text += f'体动: {sensor_data["movement"]:.2f}\n'
        details_text += f'睡眠阶段: {sensor_data["sleep_phase"]}\n'
        details_text += f'闹钟状态: {self.alarm.get_alarm_status()["wake_time"]}\n'
        self.details_label.text = details_text
        self.details_label.texture_update()
    
    def trigger_alarm(self):
        """触发闹钟"""
        self.status_label.text = '唤醒中...'
        self.alarm.trigger_alarm()

GWakenApp().run()