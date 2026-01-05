"""
红米手环2睡眠阶段检测器

基于心率和体动数据检测睡眠阶段
"""
import statistics
from datetime import datetime, timedelta


class SleepStageDetector:
    """睡眠阶段检测器"""
    
    def __init__(self, config):
        """
        初始化检测器
        :param config: 配置参数
        """
        self.config = config
        self.sleep_detection = config['sleep_detection']
        self.recent_data = []  # 存储最近的传感器数据
        self.max_data_points = 10  # 保留最近10个数据点用于分析
        
        # 睡眠阶段阈值
        self.deep_sleep_hr_threshold = self.sleep_detection['deep_sleep_hr_threshold']
        self.light_sleep_hr_threshold = self.sleep_detection['light_sleep_hr_threshold']
        self.movement_threshold = self.sleep_detection['movement_threshold']
    
    def detect_stage(self, sensor_data):
        """
        检测当前睡眠阶段
        :param sensor_data: 传感器数据，包含heart_rate和movement
        :return: 睡眠阶段 ('awake', 'light_sleep', 'deep_sleep', 'rem_sleep')
        """
        # 添加当前数据到历史记录
        self.recent_data.append({
            'timestamp': sensor_data['timestamp'],
            'heart_rate': sensor_data['heart_rate'],
            'movement': sensor_data['movement']
        })
        
        # 保持历史数据不超过最大数量
        if len(self.recent_data) > self.max_data_points:
            self.recent_data.pop(0)
        
        # 基于心率和体动检测睡眠阶段
        heart_rate = sensor_data['heart_rate']
        movement = sensor_data['movement']
        
        # 分析最近数据的心率趋势
        hr_trend = self._analyze_heart_rate_trend()
        movement_avg = self._calculate_average_movement()
        
        # 睡眠阶段判断逻辑
        # 考虑到红米手环2的传感器精度，使用相对宽松的判断标准
        if movement > self.movement_threshold * 1.5:  # 体动较大，可能清醒或翻身
            return 'awake'
        elif heart_rate < self.deep_sleep_hr_threshold and movement < self.movement_threshold * 0.5:
            # 心率低且体动很少，深睡眠
            return 'deep_sleep'
        # 优先检测REM睡眠特征，即使心率接近或略高于浅睡阈值
        elif self._is_rem_indication(heart_rate, movement, hr_trend):
            return 'rem_sleep'
        elif heart_rate < self.light_sleep_hr_threshold and movement < self.movement_threshold:
            # 心率较低且体动较少，浅睡眠
            return 'light_sleep'
        elif heart_rate >= self.light_sleep_hr_threshold:
            # 心率较高，可能清醒或即将醒来
            return 'awake'
        else:
            # 其他情况归类为浅睡眠
            return 'light_sleep'
    
    def _analyze_heart_rate_trend(self):
        """分析心率趋势"""
        if len(self.recent_data) < 2:
            return 0
        
        recent_hrs = [data['heart_rate'] for data in self.recent_data[-5:]]  # 最近5个数据点
        if len(recent_hrs) < 2:
            return 0
        
        # 计算心率变化趋势
        first_hr = recent_hrs[0]
        last_hr = recent_hrs[-1]
        trend = last_hr - first_hr
        
        return trend
    
    def _calculate_average_movement(self):
        """计算平均体动"""
        if not self.recent_data:
            return 0
        
        movements = [data['movement'] for data in self.recent_data[-5:]]  # 最近5个数据点
        return statistics.mean(movements) if movements else 0
    
    def _is_rem_indication(self, heart_rate, movement, hr_trend):
        """判断是否为REM睡眠指示"""
        # REM睡眠通常特征：心率变化较大，体动中等，心率趋势不稳定
        if len(self.recent_data) < 5:
            return False
        
        # 获取最近的心率数据
        recent_hrs = [data['heart_rate'] for data in self.recent_data[-5:]]
        hr_variability = statistics.stdev(recent_hrs) if len(set(recent_hrs)) > 1 else 0
        
        # REM睡眠的特征判断
        rem_indicators = [
            hr_variability > 3,  # 心率变化较大
            abs(hr_trend) > 2,   # 心率趋势不稳定
            movement > self.movement_threshold * 0.3 and movement < self.movement_threshold  # 中等体动
        ]
        
        # 如果满足至少2个REM特征，则认为是REM睡眠
        # 但要确保心率和体动水平适合REM睡眠（不会过高到被判定为清醒）
        if sum(rem_indicators) >= 2:
            # 额外检查：REM睡眠的心率不应太高，避免被误判为清醒
            if heart_rate < self.light_sleep_hr_threshold + 5:  # 允许稍微高一点，但仍低于清醒阈值
                return True
        
        return False
    
    def get_sleep_summary(self):
        """获取睡眠总结"""
        if not self.recent_data:
            return {}
        
        heart_rates = [data['heart_rate'] for data in self.recent_data]
        movements = [data['movement'] for data in self.recent_data]
        
        summary = {
            'avg_heart_rate': round(statistics.mean(heart_rates), 2),
            'max_heart_rate': max(heart_rates),
            'min_heart_rate': min(heart_rates),
            'avg_movement': round(statistics.mean(movements), 2),
            'data_points': len(self.recent_data)
        }
        
        return summary