"""
数据记录器

记录和管理睡眠监测数据
"""
import json
import csv
from datetime import datetime
import os
from typing import List, Dict, Optional


class DataLogger:
    """数据记录器"""
    
    def __init__(self, data_dir="data"):
        """
        初始化数据记录器
        :param data_dir: 数据存储目录
        """
        self.data_dir = data_dir
        self.ensure_data_dir()
    
    def ensure_data_dir(self):
        """确保数据目录存在"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def log_sleep_data(self, data: Dict, filename: Optional[str] = None):
        """
        记录睡眠数据
        :param data: 睡眠数据
        :param filename: 文件名（可选，默认使用日期命名）
        """
        if filename is None:
            date_str = datetime.now().strftime("%Y%m%d")
            filename = f"sleep_data_{date_str}.json"
        
        filepath = os.path.join(self.data_dir, filename)
        
        # 读取现有数据
        existing_data = []
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                existing_data = []
        
        # 添加新数据
        existing_data.append(data)
        
        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)
    
    def log_sleep_data_csv(self, data_list: List[Dict], filename: Optional[str] = None):
        """
        以CSV格式记录睡眠数据
        :param data_list: 睡眠数据列表
        :param filename: 文件名
        """
        if not data_list:
            return
        
        if filename is None:
            date_str = datetime.now().strftime("%Y%m%d")
            filename = f"sleep_data_{date_str}.csv"
        
        filepath = os.path.join(self.data_dir, filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = data_list[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for data in data_list:
                writer.writerow(data)
    
    def load_sleep_data(self, filename: Optional[str] = None):
        """
        加载睡眠数据
        :param filename: 文件名
        :return: 睡眠数据列表
        """
        if filename is None:
            date_str = datetime.now().strftime("%Y%m%d")
            filename = f"sleep_data_{date_str}.json"
        
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            return []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def export_to_json(self, data: List[Dict], filename: str):
        """
        导出数据到JSON文件
        :param data: 数据列表
        :param filename: 文件名
        """
        filepath = os.path.join(self.data_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_daily_summary(self, date_str: Optional[str] = None):
        """
        获取每日睡眠总结
        :param date_str: 日期字符串（YYYYMMDD格式）
        :return: 睡眠总结
        """
        if date_str is None:
            date_str = datetime.now().strftime("%Y%m%d")
        
        filename = f"sleep_data_{date_str}.json"
        data = self.load_sleep_data(filename)
        
        if not data:
            return {}
        
        # 计算统计信息
        heart_rates = [item['heart_rate'] for item in data if 'heart_rate' in item]
        movements = [item['movement'] for item in data if 'movement' in item]
        sleep_stages = [item['sleep_stage'] for item in data if 'sleep_stage' in item]
        
        summary = {
            'date': date_str,
            'total_records': len(data),
            'avg_heart_rate': sum(heart_rates) / len(heart_rates) if heart_rates else 0,
            'max_heart_rate': max(heart_rates) if heart_rates else 0,
            'min_heart_rate': min(heart_rates) if heart_rates else 0,
            'avg_movement': sum(movements) / len(movements) if movements else 0,
            'sleep_stage_distribution': self._count_sleep_stages(sleep_stages)
        }
        
        return summary
    
    def _count_sleep_stages(self, sleep_stages: List[str]):
        """统计睡眠阶段分布"""
        stage_counts = {}
        for stage in sleep_stages:
            stage_counts[stage] = stage_counts.get(stage, 0) + 1
        return stage_counts