import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
import time
import random
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BasePlatformScraper:
    """所有平台爬虫的基类"""
    
    def __init__(self, platform_name):
        self.platform_name = platform_name
        self.ua = UserAgent()
        self.session = requests.Session()
        # 设置默认请求头
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
    def get_hot_videos_mock(self):
        """模拟获取热点视频数据，子类需重写此方法"""
        raise NotImplementedError("子类必须实现get_hot_videos_mock方法")
    
    def scrape_real_data(self):
        """获取真实数据，子类需重写此方法"""
        raise NotImplementedError("子类必须实现scrape_real_data方法")
    
    def get_formatted_report(self, data):
        """
        格式化数据为报表格式
        """
        df = pd.DataFrame(data['videos'])
        
        # 转换时间戳为可读格式
        df['publish_time'] = pd.to_datetime(df['publish_time'], unit='s', errors='coerce')
        
        # 格式化数字
        df['play_count_formatted'] = df['play_count'].apply(self.format_number)
        df['like_count_formatted'] = df['like_count'].apply(self.format_number)
        df['comment_count_formatted'] = df['comment_count'].apply(self.format_number)
        df['share_count_formatted'] = df['share_count'].apply(self.format_number)
        
        return df
    
    def format_number(self, num):
        """
        格式化大数字为易读格式
        """
        if num >= 1000000:
            return f"{num/1000000:.1f}M"
        elif num >= 10000:
            return f"{num/10000:.1f}万"
        else:
            return str(num)