"""
红米手环2智能闹钟

实现智能唤醒功能，在浅睡眠阶段唤醒用户
"""
from datetime import datetime, timedelta
import time
import logging


logger = logging.getLogger(__name__)


class SmartAlarm:
    """智能闹钟类"""
    
    def __init__(self, config):
        """
        初始化闹钟
        :param config: 配置参数
        """
        self.config = config
        self.alarm_settings = config['alarm_settings']
        self.wake_time = self._parse_time_string(self.alarm_settings['wake_time'])
        self.alarm_window = self.alarm_settings['alarm_window']  # 唤醒时间窗口（分钟）
        self.alarm_duration = self.alarm_settings['alarm_duration']  # 闹钟持续时间（分钟）
        self.alarm_triggered = False
        self.sleep_start_time = None
        self.light_sleep_start_time = None
    
    def _parse_time_string(self, time_str):
        """解析时间字符串（HH:MM格式）"""
        try:
            hour, minute = map(int, time_str.split(':'))
            # 创建今天的时间对象
            now = datetime.now()
            target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # 如果目标时间已过今天，则设置为明天
            if target_time <= now:
                target_time += timedelta(days=1)
            
            return target_time
        except ValueError:
            logger.error(f"时间格式错误: {time_str}，使用默认时间")
            now = datetime.now()
            return now.replace(hour=7, minute=0, second=0, microsecond=0) + timedelta(days=1)
    
    def should_wake_up(self, sleep_stage, current_time):
        """
        判断是否应该唤醒用户
        :param sleep_stage: 当前睡眠阶段
        :param current_time: 当前时间
        :return: 是否应该唤醒
        """
        # 计算唤醒时间窗口
        window_start = self.wake_time - timedelta(minutes=self.alarm_window)
        window_end = self.wake_time
        
        # 检查是否在唤醒时间窗口内
        if not (window_start <= current_time <= window_end):
            return False
        
        # 检查当前睡眠阶段
        if sleep_stage == 'light_sleep':
            # 在浅睡眠阶段且在唤醒窗口内，可以唤醒
            logger.info(f"在浅睡眠阶段 {current_time.strftime('%H:%M')} 检测到唤醒条件")
            return True
        elif sleep_stage == 'rem_sleep':
            # REM睡眠阶段，如果接近目标唤醒时间也考虑唤醒
            time_to_target = (self.wake_time - current_time).total_seconds() / 60
            if time_to_target <= 5:  # 距离目标唤醒时间5分钟内
                logger.info(f"在REM睡眠阶段接近目标唤醒时间，{current_time.strftime('%H:%M')} 检测到唤醒条件")
                return True
        elif sleep_stage == 'awake':
            # 如果用户已经清醒，检查是否在唤醒时间附近
            time_diff = abs((current_time - self.wake_time).total_seconds()) / 60
            if time_diff <= 5:  # 在目标时间前后5分钟内
                logger.info(f"用户已清醒且在唤醒时间附近，{current_time.strftime('%H:%M')}")
                return True
        
        return False
    
    def trigger_alarm(self):
        """触发闹钟"""
        if self.alarm_triggered:
            return
        
        logger.info("闹钟触发！开始智能唤醒...")
        
        # 模拟闹钟渐进式唤醒（实际应用中会通过红米手环2震动实现）
        try:
            self._progressive_awakening()
        except Exception as e:
            logger.error(f"闹钟触发失败: {e}")
        finally:
            self.alarm_triggered = True
    
    def _progressive_awakening(self):
        """渐进式唤醒"""
        logger.info("开始渐进式唤醒...")
        
        # 模拟红米手环2的震动模式
        for i in range(self.alarm_duration):
            if i == 0:
                # 初始轻柔震动
                logger.info("轻柔唤醒震动")
                time.sleep(0.5)
            elif i == 1:
                # 稍强震动
                logger.info("增强震动唤醒")
                time.sleep(0.5)
            else:
                # 持续提醒
                logger.info("持续唤醒提醒")
                time.sleep(1)
            
            # 检查是否用户已响应（模拟）
            if self._check_user_response():
                logger.info("检测到用户响应，停止唤醒")
                break
    
    def _check_user_response(self):
        """检查用户是否响应（模拟）"""
        # 模拟用户响应检测（实际应用中会通过传感器检测）
        import random
        return random.random() < 0.3  # 30%概率用户响应
    
    def set_sleep_start_time(self, start_time):
        """设置睡眠开始时间"""
        self.sleep_start_time = start_time
    
    def get_alarm_status(self):
        """获取闹钟状态"""
        return {
            'wake_time': self.wake_time.strftime('%H:%M'),
            'alarm_window': self.alarm_window,
            'alarm_triggered': self.alarm_triggered,
            'current_time': datetime.now().strftime('%H:%M:%S')
        }
    
    def update_wake_time(self, new_time_str):
        """更新唤醒时间"""
        self.wake_time = self._parse_time_string(new_time_str)
        logger.info(f"唤醒时间已更新为: {new_time_str}")