import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from douyin_scraper import DouyinHotspotScraper
import json
from main import app


class TestDouyinScraper(unittest.TestCase):
    def setUp(self):
        """设置测试环境"""
        self.scraper = DouyinHotspotScraper()
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_scrape_data_structure(self):
        """测试数据结构是否正确"""
        data = self.scraper.scrape_real_data()
        
        # 验证基本结构
        self.assertIn('update_time', data)
        self.assertIn('total_videos', data)
        self.assertIn('videos', data)
        self.assertEqual(len(data['videos']), 10)
        
        # 验证视频字段
        for video in data['videos']:
            self.assertIn('rank', video)
            self.assertIn('title', video)
            self.assertIn('author', video)
            self.assertIn('play_count', video)
            self.assertIn('like_count', video)
            self.assertIn('comment_count', video)
            self.assertIn('share_count', video)
            self.assertIn('url', video)
            self.assertIn('publish_time', video)
            self.assertIn('hot_value', video)
            
            # 验证数值类型
            self.assertIsInstance(video['rank'], int)
            self.assertIsInstance(video['play_count'], int)
            self.assertIsInstance(video['like_count'], int)
            self.assertIsInstance(video['comment_count'], int)
            self.assertIsInstance(video['share_count'], int)
            self.assertIsInstance(video['hot_value'], int)

    def test_get_formatted_report(self):
        """测试数据格式化功能"""
        data = self.scraper.scrape_real_data()
        df = self.scraper.get_formatted_report(data)
        
        # 验证DataFrame包含正确的列
        expected_columns = [
            'rank', 'title', 'author', 'play_count', 'like_count', 
            'comment_count', 'share_count', 'url', 'publish_time', 'hot_value',
            'play_count_formatted', 'like_count_formatted', 
            'comment_count_formatted', 'share_count_formatted'
        ]
        for col in expected_columns:
            self.assertIn(col, df.columns)
        
        # 验证格式化后的数字是字符串
        self.assertIsInstance(df.iloc[0]['play_count_formatted'], str)
        self.assertIsInstance(df.iloc[0]['like_count_formatted'], str)

    def test_format_number(self):
        """测试数字格式化功能"""
        # 测试百万级别
        result = self.scraper.format_number(1500000)
        self.assertEqual(result, "1.5M")
        
        # 测试万级别
        result = self.scraper.format_number(150000)
        self.assertEqual(result, "15.0万")
        
        # 测试千级别
        result = self.scraper.format_number(1500)
        self.assertEqual(result, "1500")

    def test_api_endpoints(self):
        """测试API端点"""
        # 测试主页
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('endpoints', data)
        
        # 测试热点数据API
        response = self.client.get('/api/hot')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('update_time', data)
        self.assertIn('total_videos', data)
        self.assertIn('videos', data)
        
        # 测试表格数据API
        response = self.client.get('/api/hot/table')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('columns', data)
        self.assertIn('rows', data)
        self.assertIn('update_time', data)

    def test_report_page(self):
        """测试报表页面"""
        response = self.client.get('/report')
        self.assertEqual(response.status_code, 200)
        self.assertIn('抖音热点视频排行榜'.encode('utf-8'), response.data)


if __name__ == '__main__':
    print("开始运行抖音热点数据爬取系统测试...")
    unittest.main(verbosity=2)