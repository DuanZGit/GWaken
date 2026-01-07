#!/usr/bin/env python3
"""
红米手环2智能睡眠监测系统 - Android版
"""
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.spinner import Spinner
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

class SleepMonitorApp(App):
    def build(self):
        self.title = '红米手环2智能睡眠监测系统'
        
        # 加载配置
        self.config = self.load_config()
        
        # 初始化组件
        self.init_system()
        
        # 创建主界面
        return self.create_main_layout()
    
    def load_config(self):
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
    
    def init_system(self):
        """初始化系统组件"""
        # 根据配置决定使用哪种传感器
        device_settings = self.config.get('device_settings', {})
        preferred_sensor_type = device_settings.get('sensor_type', 'bluetooth')  # 默认使用蓝牙
        
        logger.info(f"使用传感器类型: {SENSOR_TYPE} (配置要求: {preferred_sensor_type})")
        
        # 初始化传感器（按优先级选择，但优先满足配置要求）
        if SENSOR_TYPE == 'bluetooth' and preferred_sensor_type in ['bluetooth', 'auto']:
            logger.info("初始化蓝牙传感器")
            self.sensor = BluetoothSensor(self.config)
        elif SENSOR_TYPE == 'hardware' and preferred_sensor_type in ['hardware', 'api', 'auto']:
            logger.info("初始化硬件传感器")
            self.sensor = HardwareSensor(self.config)
        else:
            logger.info("初始化传感器模拟器")
            self.sensor = SensorSimulator(self.config)
        
        self.sleep_detector = SleepStageDetector(self.config)
        self.smart_alarm = SmartAlarm(self.config)
        
        # 用于更新界面的变量
        self.current_sensor_data = {}
        self.current_sleep_stage = "未知"
        self.sleep_data = []
    
    def create_main_layout(self):
        """创建主界面布局"""
        # 创建选项卡面板
        panel = TabbedPanel()
        panel.do_default_tab = True
        
        # 状态选项卡
        status_tab = TabbedPanelItem(text='状态')
        status_layout = self.create_status_layout()
        status_tab.content = ScrollView(size_hint_y=1, do_scroll_x=False)
        status_tab.content.add_widget(status_layout)
        panel.add_widget(status_tab)
        
        # 监测选项卡
        monitor_tab = TabbedPanelItem(text='监测')
        monitor_layout = self.create_monitor_layout()
        monitor_tab.content = ScrollView(size_hint_y=1, do_scroll_x=False)
        monitor_tab.content.add_widget(monitor_layout)
        panel.add_widget(monitor_tab)
        
        # 配置选项卡
        config_tab = TabbedPanelItem(text='配置')
        config_layout = self.create_config_layout()
        config_tab.content = ScrollView(size_hint_y=1, do_scroll_x=False)
        config_tab.content.add_widget(config_layout)
        panel.add_widget(config_tab)
        
        # 闹钟选项卡
        alarm_tab = TabbedPanelItem(text='闹钟')
        alarm_layout = self.create_alarm_layout()
        alarm_tab.content = ScrollView(size_hint_y=1, do_scroll_x=False)
        alarm_tab.content.add_widget(alarm_layout)
        panel.add_widget(alarm_tab)
        
        return panel
    
    def create_status_layout(self):
        """创建状态页面"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 系统状态标签
        self.status_label = Label(text='系统状态: 初始化中...', size_hint_y=None, height=40)
        layout.add_widget(self.status_label)
        
        # 传感器状态
        self.sensor_status_label = Label(text='传感器状态: 未知', size_hint_y=None, height=40)
        layout.add_widget(self.sensor_status_label)
        
        # 当前睡眠阶段
        self.sleep_stage_label = Label(text='当前睡眠阶段: 未知', size_hint_y=None, height=40)
        layout.add_widget(self.sleep_stage_label)
        
        # 心率数据
        self.heart_rate_label = Label(text='心率: 未知', size_hint_y=None, height=40)
        layout.add_widget(self.heart_rate_label)
        
        # 体动数据
        self.movement_label = Label(text='体动: 未知', size_hint_y=None, height=40)
        layout.add_widget(self.movement_label)
        
        # 开始监测按钮
        self.start_monitor_btn = Button(text='开始监测', size_hint_y=None, height=50)
        self.start_monitor_btn.bind(on_press=self.start_monitoring)
        layout.add_widget(self.start_monitor_btn)
        
        # 停止监测按钮
        self.stop_monitor_btn = Button(text='停止监测', size_hint_y=None, height=50)
        self.stop_monitor_btn.bind(on_press=self.stop_monitoring)
        self.stop_monitor_btn.disabled = True
        layout.add_widget(self.stop_monitor_btn)
        
        # 启动定时器更新状态
        Clock.schedule_interval(self.update_status, 1.0)
        
        return layout
    
    def create_monitor_layout(self):
        """创建监测页面"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 监测数据显示
        self.monitor_data_label = Label(text='监测数据将显示在这里...', size_hint_y=None, height=300)
        layout.add_widget(self.monitor_data_label)
        
        # 睡眠阶段历史
        self.sleep_history_label = Label(text='睡眠阶段历史:\n暂无数据', size_hint_y=None, height=200)
        layout.add_widget(self.sleep_history_label)
        
        # 刷新按钮
        refresh_btn = Button(text='刷新数据', size_hint_y=None, height=50)
        refresh_btn.bind(on_press=self.refresh_monitor_data)
        layout.add_widget(refresh_btn)
        
        return layout
    
    def create_config_layout(self):
        """创建配置页面"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 睡眠检测配置
        config_grid = GridLayout(cols=2, spacing=10, size_hint_y=None, height=300)
        
        config_grid.add_widget(Label(text='采样率(秒):'))
        self.sampling_rate_input = TextInput(text=str(self.config['sleep_detection']['sampling_rate']), multiline=False)
        config_grid.add_widget(self.sampling_rate_input)
        
        config_grid.add_widget(Label(text='深睡心率阈值:'))
        self.deep_sleep_threshold_input = TextInput(text=str(self.config['sleep_detection']['deep_sleep_hr_threshold']), multiline=False)
        config_grid.add_widget(self.deep_sleep_threshold_input)
        
        config_grid.add_widget(Label(text='浅睡心率阈值:'))
        self.light_sleep_threshold_input = TextInput(text=str(self.config['sleep_detection']['light_sleep_hr_threshold']), multiline=False)
        config_grid.add_widget(self.light_sleep_threshold_input)
        
        config_grid.add_widget(Label(text='体动阈值:'))
        self.movement_threshold_input = TextInput(text=str(self.config['sleep_detection']['movement_threshold']), multiline=False)
        config_grid.add_widget(self.movement_threshold_input)
        
        layout.add_widget(config_grid)
        
        # 保存配置按钮
        save_config_btn = Button(text='保存配置', size_hint_y=None, height=50)
        save_config_btn.bind(on_press=self.save_config)
        layout.add_widget(save_config_btn)
        
        # 加载配置按钮
        load_config_btn = Button(text='加载配置', size_hint_y=None, height=50)
        load_config_btn.bind(on_press=self.load_config_from_file)
        layout.add_widget(load_config_btn)
        
        return layout
    
    def create_alarm_layout(self):
        """创建闹钟页面"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 闹钟设置
        alarm_grid = GridLayout(cols=2, spacing=10, size_hint_y=None, height=200)
        
        alarm_grid.add_widget(Label(text='唤醒时间:'))
        self.wake_time_input = TextInput(text=self.config['alarm_settings']['wake_time'], multiline=False)
        alarm_grid.add_widget(self.wake_time_input)
        
        alarm_grid.add_widget(Label(text='唤醒时间窗口(分钟):'))
        self.alarm_window_input = TextInput(text=str(self.config['alarm_settings']['alarm_window']), multiline=False)
        alarm_grid.add_widget(self.alarm_window_input)
        
        alarm_grid.add_widget(Label(text='闹钟持续时间(分钟):'))
        self.alarm_duration_input = TextInput(text=str(self.config['alarm_settings']['alarm_duration']), multiline=False)
        alarm_grid.add_widget(self.alarm_duration_input)
        
        layout.add_widget(alarm_grid)
        
        # 闹钟状态
        self.alarm_status_label = Label(text='闹钟状态: 未设置', size_hint_y=None, height=40)
        layout.add_widget(self.alarm_status_label)
        
        # 触发闹钟按钮
        trigger_alarm_btn = Button(text='测试闹钟', size_hint_y=None, height=50)
        trigger_alarm_btn.bind(on_press=self.test_alarm)
        layout.add_widget(trigger_alarm_btn)
        
        # 保存闹钟设置按钮
        save_alarm_btn = Button(text='保存闹钟设置', size_hint_y=None, height=50)
        save_alarm_btn.bind(on_press=self.save_alarm_config)
        layout.add_widget(save_alarm_btn)
        
        return layout
    
    def update_status(self, dt):
        """更新状态显示"""
        try:
            # 获取传感器数据
            sensor_data = self.sensor.get_sensor_data()
            self.current_sensor_data = sensor_data
            
            # 检测睡眠阶段
            sleep_stage = self.sleep_detector.detect_stage(sensor_data)
            self.current_sleep_stage = sleep_stage
            
            # 更新UI
            self.status_label.text = f'系统状态: 运行中'
            device_info = self.sensor.get_device_info()
            device_name = device_info.get("device_name", device_info.get("name", "未知设备"))
            self.sensor_status_label.text = f'传感器状态: 已连接 - {device_name}'
            self.sleep_stage_label.text = f'当前睡眠阶段: {sleep_stage}'
            self.heart_rate_label.text = f'心率: {sensor_data["heart_rate"]} BPM'
            self.movement_label.text = f'体动: {sensor_data["movement"]}'
            
            # 记录睡眠数据
            self.sleep_data.append({
                'timestamp': datetime.now().isoformat(),
                'heart_rate': sensor_data['heart_rate'],
                'movement': sensor_data['movement'],
                'sleep_stage': sleep_stage
            })
            
            # 检查是否需要唤醒
            current_time = datetime.now()
            if self.smart_alarm.should_wake_up(sleep_stage, current_time):
                self.trigger_alarm(None)
                
        except Exception as e:
            logger.error(f"更新状态时出错: {e}")
    
    def start_monitoring(self, instance):
        """开始监测"""
        logger.info("开始睡眠监测")
        self.start_monitor_btn.disabled = True
        self.stop_monitor_btn.disabled = False
    
    def stop_monitoring(self, instance):
        """停止监测"""
        logger.info("停止睡眠监测")
        self.start_monitor_btn.disabled = False
        self.stop_monitor_btn.disabled = True
    
    def refresh_monitor_data(self, instance):
        """刷新监测数据"""
        # 更新监测数据显示
        if self.current_sensor_data:
            data_str = f"时间: {self.current_sensor_data.get('timestamp', '未知')}\n"
            data_str += f"心率: {self.current_sensor_data.get('heart_rate', '未知')} BPM\n"
            data_str += f"体动: {self.current_sensor_data.get('movement', '未知')}\n"
            data_str += f"睡眠阶段: {self.current_sleep_stage}\n"
            data_str += f"设备信息: {self.sensor.get_device_info()}"
            self.monitor_data_label.text = data_str
        
        # 更新睡眠历史
        if self.sleep_data:
            history_str = "睡眠阶段历史:\n"
            # 显示最近10个数据点
            recent_data = self.sleep_data[-10:]
            for data in recent_data:
                history_str += f"{data['timestamp'].split('T')[1][:8]} - {data['sleep_stage']} (HR: {data['heart_rate']})\n"
            self.sleep_history_label.text = history_str
    
    def save_config(self, instance):
        """保存配置"""
        try:
            # 更新配置
            self.config['sleep_detection']['sampling_rate'] = int(self.sampling_rate_input.text)
            self.config['sleep_detection']['deep_sleep_hr_threshold'] = int(self.deep_sleep_threshold_input.text)
            self.config['sleep_detection']['light_sleep_hr_threshold'] = int(self.light_sleep_threshold_input.text)
            self.config['sleep_detection']['movement_threshold'] = float(self.movement_threshold_input.text)
            
            # 重新初始化睡眠检测器
            self.sleep_detector = SleepStageDetector(self.config)
            
            # 显示成功消息
            popup = Popup(title='配置保存',
                         content=Label(text='配置已成功保存'),
                         size_hint=(0.8, 0.4))
            popup.open()
            
        except ValueError:
            popup = Popup(title='错误',
                         content=Label(text='请检查输入值，确保它们是有效的数字'),
                         size_hint=(0.8, 0.4))
            popup.open()
    
    def load_config_from_file(self, instance):
        """从文件加载配置"""
        try:
            self.config = self.load_config()
            
            # 更新界面显示
            self.sampling_rate_input.text = str(self.config['sleep_detection']['sampling_rate'])
            self.deep_sleep_threshold_input.text = str(self.config['sleep_detection']['deep_sleep_hr_threshold'])
            self.light_sleep_threshold_input.text = str(self.config['sleep_detection']['light_sleep_hr_threshold'])
            self.movement_threshold_input.text = str(self.config['sleep_detection']['movement_threshold'])
            
            # 重新初始化
            self.init_system()
            
            popup = Popup(title='配置加载',
                         content=Label(text='配置已从文件重新加载'),
                         size_hint=(0.8, 0.4))
            popup.open()
            
        except Exception as e:
            popup = Popup(title='错误',
                         content=Label(text=f'加载配置失败: {str(e)}'),
                         size_hint=(0.8, 0.4))
            popup.open()
    
    def test_alarm(self, instance):
        """测试闹钟"""
        self.smart_alarm.trigger_alarm()
        self.alarm_status_label.text = f'闹钟状态: 已触发 ({datetime.now().strftime("%H:%M:%S")})'
    
    def trigger_alarm(self, instance):
        """触发闹钟"""
        self.smart_alarm.trigger_alarm()
        self.alarm_status_label.text = f'闹钟状态: 已触发 ({datetime.now().strftime("%H:%M:%S")})'
    
    def save_alarm_config(self, instance):
        """保存闹钟配置"""
        try:
            self.config['alarm_settings']['wake_time'] = self.wake_time_input.text
            self.config['alarm_settings']['alarm_window'] = int(self.alarm_window_input.text)
            self.config['alarm_settings']['alarm_duration'] = int(self.alarm_duration_input.text)
            
            # 重新初始化闹钟
            self.smart_alarm = SmartAlarm(self.config)
            
            popup = Popup(title='闹钟配置保存',
                         content=Label(text='闹钟配置已成功保存'),
                         size_hint=(0.8, 0.4))
            popup.open()
            
        except ValueError:
            popup = Popup(title='错误',
                         content=Label(text='请检查输入值，确保时间格式正确且数字有效'),
                         size_hint=(0.8, 0.4))
            popup.open()

if __name__ == '__main__':
    SleepMonitorApp().run()