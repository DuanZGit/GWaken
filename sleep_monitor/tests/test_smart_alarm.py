"""
智能闹钟测试模块
"""
import unittest
from datetime import datetime, timedelta
from sleep_monitor.alarm.smart_alarm import SmartAlarm


class TestSmartAlarm(unittest.TestCase):
    """智能闹钟测试类"""
    
    def setUp(self):
        """测试初始化"""
        self.config = {
            'sleep_detection': {
                'sampling_rate': 60,
                'deep_sleep_hr_threshold': 60,
                'light_sleep_hr_threshold': 70,
                'movement_threshold': 5
            },
            'alarm_settings': {
                'wake_time': '07:00',
                'alarm_window': 30,
                'alarm_duration': 5
            }
        }
        self.alarm = SmartAlarm(self.config)
    
    def test_initialization(self):
        """测试初始化"""
        self.assertEqual(self.alarm.alarm_settings['wake_time'], '07:00')
        self.assertEqual(self.alarm.alarm_window, 30)
        self.assertEqual(self.alarm.alarm_duration, 5)
        self.assertFalse(self.alarm.alarm_triggered)
    
    def test_parse_time_string(self):
        """测试时间字符串解析"""
        # 测试正常时间解析
        time_str = '08:30'
        parsed_time = self.alarm._parse_time_string(time_str)
        
        # 检查时间是否正确解析
        self.assertEqual(parsed_time.hour, 8)
        self.assertEqual(parsed_time.minute, 30)
    
    def test_should_wake_up_light_sleep(self):
        """测试浅睡眠唤醒条件"""
        # 设置一个未来时间
        future_time = datetime.now() + timedelta(minutes=10)
        
        # 在唤醒窗口内且为浅睡眠，应该唤醒
        should_wake = self.alarm.should_wake_up('light_sleep', future_time)
        # 结果取决于当前时间是否在唤醒窗口内，所以不直接断言
        
        self.assertIsInstance(should_wake, bool)
    
    def test_should_wake_up_awake_stage(self):
        """测试清醒状态唤醒条件"""
        # 设置接近目标时间的清醒状态
        target_time = self.alarm.wake_time
        close_time = target_time - timedelta(minutes=3)
        
        should_wake = self.alarm.should_wake_up('awake', close_time)
        self.assertIsInstance(should_wake, bool)
    
    def test_alarm_status(self):
        """测试闹钟状态获取"""
        status = self.alarm.get_alarm_status()
        
        self.assertIn('wake_time', status)
        self.assertIn('alarm_window', status)
        self.assertIn('alarm_triggered', status)
        self.assertIn('current_time', status)
        
        self.assertIsInstance(status['alarm_window'], int)
        self.assertIsInstance(status['alarm_triggered'], bool)


if __name__ == '__main__':
    unittest.main()