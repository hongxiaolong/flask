import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from douyin_scraper import DouyinScraper
from xiaohongshu_scraper import XiaohongshuScraper
from kuaishou_scraper import KuaishouScraper
from platform_manager import platform_manager
import json
from main import app


class TestMultiPlatformScraper(unittest.TestCase):
    def setUp(self):
        """设置测试环境"""
        self.douyin_scraper = DouyinScraper()
        self.xiaohongshu_scraper = XiaohongshuScraper()
        self.kuaishou_scraper = KuaishouScraper()
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_douyin_data_structure(self):
        """测试抖音数据结构是否正确"""
        data = self.douyin_scraper.scrape_real_data()
        
        # 验证基本结构
        self.assertIn('update_time', data)
        self.assertIn('total_videos', data)
        self.assertIn('platform', data)
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

    def test_xiaohongshu_data_structure(self):
        """测试小红书数据结构是否正确"""
        data = self.xiaohongshu_scraper.scrape_real_data()
        
        # 验证基本结构
        self.assertIn('update_time', data)
        self.assertIn('total_videos', data)
        self.assertIn('platform', data)
        self.assertIn('videos', data)
        self.assertEqual(len(data['videos']), 10)
        
        # 验证视频字段（小红书笔记）
        for video in data['videos']:
            self.assertIn('rank', video)
            self.assertIn('title', video)
            self.assertIn('author', video)
            self.assertIn('play_count', video)  # 浏览量
            self.assertIn('like_count', video)  # 点赞数
            self.assertIn('comment_count', video)  # 评论数
            self.assertIn('share_count', video)  # 分享数
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

    def test_kuaishou_data_structure(self):
        """测试快手数据结构是否正确"""
        data = self.kuaishou_scraper.scrape_real_data()
        
        # 验证基本结构
        self.assertIn('update_time', data)
        self.assertIn('total_videos', data)
        self.assertIn('platform', data)
        self.assertIn('videos', data)
        self.assertEqual(len(data['videos']), 10)
        
        # 验证视频字段
        for video in data['videos']:
            self.assertIn('rank', video)
            self.assertIn('title', video)
            self.assertIn('author', video)
            self.assertIn('play_count', video)  # 播放量
            self.assertIn('like_count', video)  # 点赞数
            self.assertIn('comment_count', video)  # 评论数
            self.assertIn('share_count', video)  # 分享数
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

    def test_platform_manager(self):
        """测试平台管理器功能"""
        # 测试获取单个平台数据
        douyin_data = platform_manager.get_platform_data('douyin')
        self.assertIn('platform', douyin_data)
        self.assertEqual(douyin_data['platform'], '抖音')
        
        xiaohongshu_data = platform_manager.get_platform_data('xiaohongshu')
        self.assertIn('platform', xiaohongshu_data)
        self.assertEqual(xiaohongshu_data['platform'], '小红书')
        
        kuaishou_data = platform_manager.get_platform_data('kuaishou')
        self.assertIn('platform', kuaishou_data)
        self.assertEqual(kuaishou_data['platform'], '快手')
        
        # 测试获取所有平台数据
        all_data = platform_manager.get_all_platforms_data()
        self.assertIn('douyin', all_data)
        self.assertIn('xiaohongshu', all_data)
        self.assertIn('kuaishou', all_data)
        
        # 测试聚合数据
        aggregated_data = platform_manager.get_aggregated_data()
        self.assertIn('top_videos', aggregated_data)
        self.assertIn('platform_counts', aggregated_data)
        self.assertIn('total_videos', aggregated_data)
        self.assertGreaterEqual(len(aggregated_data['top_videos']), 0)  # 可能少于10个，但不能是负数

    def test_format_number(self):
        """测试数字格式化功能"""
        # 测试百万级别
        result = self.douyin_scraper.format_number(1500000)
        self.assertEqual(result, "1.5M")
        
        # 测试万级别
        result = self.douyin_scraper.format_number(150000)
        self.assertEqual(result, "15.0万")
        
        # 测试千级别
        result = self.douyin_scraper.format_number(1500)
        self.assertEqual(result, "1500")

    def test_api_endpoints(self):
        """测试API端点"""
        # 测试主页
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('endpoints', data)
        
        # 测试抖音热点数据API
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
        
        # 测试指定平台数据API
        response = self.client.get('/api/platform/douyin')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('platform', data)
        self.assertEqual(data['platform'], '抖音')
        
        response = self.client.get('/api/platform/xiaohongshu')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('platform', data)
        self.assertEqual(data['platform'], '小红书')
        
        response = self.client.get('/api/platform/kuaishou')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('platform', data)
        self.assertEqual(data['platform'], '快手')
        
        # 测试所有平台数据API
        response = self.client.get('/api/all_platforms')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('douyin', data)
        self.assertIn('xiaohongshu', data)
        self.assertIn('kuaishou', data)
        
        # 测试聚合数据API
        response = self.client.get('/api/aggregated')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('top_videos', data)
        self.assertIn('platform_counts', data)

    def test_report_pages(self):
        """测试报表页面"""
        # 测试抖音报表页面
        response = self.client.get('/report')
        self.assertEqual(response.status_code, 200)
        self.assertIn('抖音热点视频排行榜'.encode('utf-8'), response.data)
        
        # 测试多平台报表页面
        response = self.client.get('/multi_report')
        self.assertEqual(response.status_code, 200)
        self.assertIn('多平台热点视频综合排行榜'.encode('utf-8'), response.data)


if __name__ == '__main__':
    print("开始运行多平台热点数据爬取系统测试...")
    unittest.main(verbosity=2)