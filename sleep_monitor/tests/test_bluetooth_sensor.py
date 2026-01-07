"""
蓝牙传感器测试模块
"""
import unittest
from sleep_monitor.sensors.bluetooth_sensor import BluetoothSensor


class TestBluetoothSensor(unittest.TestCase):
    """蓝牙传感器测试类"""
    
    def setUp(self):
        """测试初始化"""
        self.config = {
            'sleep_detection': {
                'sampling_rate': 60,
                'deep_sleep_hr_threshold': 60,
                'light_sleep_hr_threshold': 70,
                'movement_threshold': 5
            },
            'device_settings': {
                'device_model': 'Redmi Band 2',
                'bluetooth_address': '',
                'device_name': 'Redmi Band 2',
                'sensor_type': 'bluetooth'
            }
        }
        self.sensor = BluetoothSensor(self.config)
    
    def test_get_sensor_data(self):
        """测试获取传感器数据"""
        data = self.sensor.get_sensor_data()
        
        self.assertIn('timestamp', data)
        self.assertIn('heart_rate', data)
        self.assertIn('movement', data)
        self.assertIn('battery_level', data)
        self.assertIn('device_status', data)
        
        # 检查数据类型
        self.assertIsInstance(data['heart_rate'], int)
        self.assertIsInstance(data['movement'], float)
        self.assertIsInstance(data['battery_level'], int)
        
        # 检查数据范围
        self.assertGreaterEqual(data['heart_rate'], 40)
        self.assertLessEqual(data['heart_rate'], 120)
        self.assertGreaterEqual(data['movement'], 0)
        self.assertLessEqual(data['battery_level'], 100)
        self.assertGreaterEqual(data['battery_level'], 0)
    
    def test_device_info(self):
        """测试获取设备信息"""
        info = self.sensor.get_device_info()
        
        self.assertIn('connected', info)
        self.assertIn('device_model', info)
        self.assertIn('device_name', info)
        self.assertIn('use_simulation', info)
        
        self.assertEqual(info['device_model'], 'Redmi Band 2')
        self.assertEqual(info['device_name'], 'Redmi Band 2')
        self.assertIsInstance(info['connected'], bool)
        self.assertIsInstance(info['use_simulation'], bool)


if __name__ == '__main__':
    unittest.main()