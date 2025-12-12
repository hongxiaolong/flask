import logging
from typing import Dict, List
from douyin_scraper import DouyinScraper
from xiaohongshu_scraper import XiaohongshuScraper
from kuaishou_scraper import KuaishouScraper
from platform_base import BasePlatformScraper

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlatformManager:
    """多平台管理器"""
    
    def __init__(self):
        self.platforms: Dict[str, BasePlatformScraper] = {}
        self._initialize_platforms()
    
    def _initialize_platforms(self):
        """初始化各平台爬虫实例"""
        self.platforms = {
            'douyin': DouyinScraper(),
            'xiaohongshu': XiaohongshuScraper(),
            'kuaishou': KuaishouScraper()
        }
        logger.info(f"已初始化 {len(self.platforms)} 个平台爬虫")
    
    def get_platform_data(self, platform_key: str):
        """获取指定平台的数据"""
        if platform_key not in self.platforms:
            raise ValueError(f"不支持的平台: {platform_key}")
        
        scraper = self.platforms[platform_key]
        logger.info(f"开始获取 {scraper.platform_name} 数据")
        return scraper.scrape_real_data()
    
    def get_all_platforms_data(self) -> Dict:
        """获取所有平台的数据"""
        all_data = {}
        for key, scraper in self.platforms.items():
            try:
                logger.info(f"获取 {scraper.platform_name} 数据...")
                data = scraper.scrape_real_data()
                all_data[key] = data
            except Exception as e:
                logger.error(f"获取 {scraper.platform_name} 数据失败: {e}")
                # 返回空数据或错误信息
                all_data[key] = {
                    'error': f'获取 {scraper.platform_name} 数据失败',
                    'message': str(e),
                    'platform': scraper.platform_name
                }
        
        return all_data
    
    def get_aggregated_data(self) -> Dict:
        """聚合所有平台的数据"""
        all_platforms_data = self.get_all_platforms_data()
        
        # 合并所有视频/内容
        aggregated_videos = []
        platform_counts = {}
        
        for platform_key, platform_data in all_platforms_data.items():
            if 'error' not in platform_data and 'videos' in platform_data:
                # 为每个视频添加平台标识
                for video in platform_data['videos']:
                    video['platform'] = platform_data['platform']
                    aggregated_videos.append(video)
                
                platform_counts[platform_data['platform']] = len(platform_data['videos'])
        
        # 按热度值排序
        aggregated_videos.sort(key=lambda x: x.get('hot_value', 0), reverse=True)
        
        # 只取前30个最热的内容（从所有平台中）
        top_videos = aggregated_videos[:30]
        
        result = {
            'update_time': self._get_current_time(),
            'total_videos': len(aggregated_videos),
            'top_videos': top_videos[:10],  # 返回前10个
            'platform_counts': platform_counts,
            'all_platforms_data': all_platforms_data
        }
        
        return result
    
    def get_platform_names(self) -> List[str]:
        """获取所有平台名称"""
        return [scraper.platform_name for scraper in self.platforms.values()]
    
    def _get_current_time(self) -> str:
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 创建全局实例
platform_manager = PlatformManager()