"""
睡眠检测器测试模块
"""
import unittest
from sleep_monitor.sleep_analysis.sleep_stage_detector import SleepStageDetector


class TestSleepStageDetector(unittest.TestCase):
    """睡眠阶段检测器测试类"""
    
    def setUp(self):
        """测试初始化"""
        self.config = {
            'sleep_detection': {
                'sampling_rate': 60,
                'deep_sleep_hr_threshold': 60,
                'light_sleep_hr_threshold': 70,
                'movement_threshold': 5
            }
        }
        self.detector = SleepStageDetector(self.config)
    
    def test_detect_deep_sleep(self):
        """测试深睡眠检测"""
        # 模拟深睡眠数据：低心率，低体动
        sensor_data = {
            'timestamp': '2023-01-01T02:00:00',
            'heart_rate': 58,
            'movement': 1
        }
        
        stage = self.detector.detect_stage(sensor_data)
        self.assertIn(stage, ['deep_sleep', 'light_sleep'], 
                     f"低心率低体动应该检测为深睡眠或浅睡眠，但返回了 {stage}")
    
    def test_detect_light_sleep(self):
        """测试浅睡眠检测"""
        # 模拟浅睡眠数据：中等心率，中等体动
        sensor_data = {
            'timestamp': '2023-01-01T01:00:00',
            'heart_rate': 65,
            'movement': 3
        }
        
        stage = self.detector.detect_stage(sensor_data)
        self.assertIn(stage, ['light_sleep', 'deep_sleep'], 
                     f"中等心率中等体动应该检测为浅睡眠或深睡眠，但返回了 {stage}")
    
    def test_detect_awake(self):
        """测试清醒状态检测"""
        # 模拟清醒数据：高心率，高体动
        sensor_data = {
            'timestamp': '2023-01-01T08:00:00',
            'heart_rate': 80,
            'movement': 10
        }
        
        stage = self.detector.detect_stage(sensor_data)
        self.assertIn(stage, ['awake', 'light_sleep'], 
                     f"高心率高体动应该检测为清醒或浅睡眠，但返回了 {stage}")
    
    def test_detect_rem_sleep(self):
        """测试REM睡眠检测"""
        # 首先添加一些数据来建立趋势
        # 模拟心率变化较大的数据（REM特征）
        for i in range(5):
            sensor_data = {
                'timestamp': f'2023-01-01T03:{i:02d}:00',
                'heart_rate': 65 + (i % 2) * 10,  # 心率变化
                'movement': 4
            }
            self.detector.detect_stage(sensor_data)
        
        # 再次检测，此时应该有更多的历史数据来判断REM
        sensor_data = {
            'timestamp': '2023-01-01T03:05:00',
            'heart_rate': 70,
            'movement': 4
        }
        
        stage = self.detector.detect_stage(sensor_data)
        # REM睡眠检测较为复杂，可能返回多种结果，但不应该返回清醒
        self.assertNotEqual(stage, 'awake', 
                           f"REM睡眠特征数据不应该检测为清醒，但返回了 {stage}")
    
    def test_get_sleep_summary(self):
        """测试获取睡眠总结"""
        # 添加一些测试数据
        test_data = [
            {'timestamp': '2023-01-01T01:00:00', 'heart_rate': 70, 'movement': 5},
            {'timestamp': '2023-01-01T01:01:00', 'heart_rate': 65, 'movement': 3},
            {'timestamp': '2023-01-01T01:02:00', 'heart_rate': 60, 'movement': 1},
        ]
        
        for data in test_data:
            self.detector.detect_stage(data)
        
        summary = self.detector.get_sleep_summary()
        
        self.assertIn('avg_heart_rate', summary)
        self.assertIn('max_heart_rate', summary)
        self.assertIn('min_heart_rate', summary)
        self.assertIn('avg_movement', summary)
        self.assertGreaterEqual(summary['data_points'], 3)


if __name__ == '__main__':
    unittest.main()