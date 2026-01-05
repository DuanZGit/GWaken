"""
时间工具

提供时间相关的工具函数
"""
from datetime import datetime, timedelta
import time


def format_timestamp(timestamp, format_str="%Y-%m-%d %H:%M:%S"):
    """
    格式化时间戳
    :param timestamp: 时间戳或datetime对象
    :param format_str: 格式字符串
    :return: 格式化后的时间字符串
    """
    if isinstance(timestamp, str):
        # 如果是字符串，尝试解析
        try:
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            return timestamp
    
    if isinstance(timestamp, (int, float)):
        timestamp = datetime.fromtimestamp(timestamp)
    
    return timestamp.strftime(format_str)


def time_diff_minutes(start_time, end_time):
    """
    计算两个时间之间的分钟差
    :param start_time: 开始时间
    :param end_time: 结束时间
    :return: 分钟差
    """
    if isinstance(start_time, str):
        start_time = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
    if isinstance(end_time, str):
        end_time = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
    
    diff = end_time - start_time
    return int(diff.total_seconds() / 60)


def is_night_time(check_time=None):
    """
    判断是否为夜间时间（用于睡眠监测）
    :param check_time: 要检查的时间，默认为当前时间
    :return: 是否为夜间
    """
    if check_time is None:
        check_time = datetime.now()
    
    hour = check_time.hour
    # 定义夜间时间为21:00到09:00
    return hour >= 21 or hour < 9


def get_sleep_cycle_times(start_time, duration_minutes=480):
    """
    计算睡眠周期时间
    :param start_time: 睡眠开始时间
    :param duration_minutes: 睡眠持续时间（分钟），默认8小时
    :return: 睡眠周期时间点列表
    """
    if isinstance(start_time, str):
        start_time = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
    
    cycle_times = []
    # 一个睡眠周期约为90分钟
    cycle_length = 90
    
    for i in range(0, duration_minutes, cycle_length):
        cycle_time = start_time + timedelta(minutes=i)
        cycle_times.append(cycle_time)
    
    return cycle_times


def get_optimal_wake_time(sleep_start_time, min_sleep_hours=6, max_sleep_hours=9):
    """
    计算最佳唤醒时间（在浅睡眠阶段）
    :param sleep_start_time: 睡眠开始时间
    :param min_sleep_hours: 最小睡眠小时数
    :param max_sleep_hours: 最大睡眠小时数
    :return: 最佳唤醒时间列表
    """
    if isinstance(sleep_start_time, str):
        sleep_start_time = datetime.fromisoformat(sleep_start_time.replace('Z', '+00:00'))
    
    optimal_times = []
    
    # 计算可能的唤醒时间点（在睡眠周期结束时，通常是浅睡眠阶段）
    for hour in range(min_sleep_hours, max_sleep_hours + 1):
        # 每个周期约90分钟，但为了简单计算，我们使用整小时
        for cycle in range(1, 6):  # 最多考虑5个周期
            cycle_duration = (cycle * 90)  # 90分钟一个周期
            if cycle_duration / 60 <= hour:  # 确保周期在睡眠时间内
                wake_time = sleep_start_time + timedelta(minutes=cycle_duration)
                
                # 检查是否在合理范围内
                min_wake_time = sleep_start_time + timedelta(hours=min_sleep_hours)
                max_wake_time = sleep_start_time + timedelta(hours=max_sleep_hours)
                
                if min_wake_time <= wake_time <= max_wake_time:
                    optimal_times.append(wake_time)
    
    return optimal_times


def timestamp_to_local(timestamp):
    """
    将时间戳转换为本地时间
    :param timestamp: 时间戳
    :return: 本地时间datetime对象
    """
    if isinstance(timestamp, str):
        return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    elif isinstance(timestamp, (int, float)):
        return datetime.fromtimestamp(timestamp)
    else:
        return timestamp


def get_time_range(start_time, end_time, interval_minutes=1):
    """
    获取时间范围内的所有时间点
    :param start_time: 开始时间
    :param end_time: 结束时间
    :param interval_minutes: 时间间隔（分钟）
    :return: 时间点列表
    """
    if isinstance(start_time, str):
        start_time = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
    if isinstance(end_time, str):
        end_time = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
    
    time_range = []
    current_time = start_time
    
    while current_time <= end_time:
        time_range.append(current_time)
        current_time += timedelta(minutes=interval_minutes)
    
    return time_range