import schedule
import time
import threading
from datetime import datetime
from platform_manager import platform_manager
import json
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataUpdater:
    def __init__(self):
        self.data_file = 'all_platforms_hot_data.json'
        self.lock = threading.Lock()
        self.last_update_time = None
        
    def update_data(self):
        """更新所有平台热点数据"""
        logger.info(f"[{datetime.now()}] 开始更新所有平台热点数据...")
        try:
            with self.lock:
                # 获取所有平台的数据
                all_data = platform_manager.get_all_platforms_data()
                
                # 保存到本地文件
                with open(self.data_file, 'w', encoding='utf-8') as f:
                    json.dump(all_data, f, ensure_ascii=False, indent=2)
                
                self.last_update_time = datetime.now()
                logger.info(f"[{datetime.now()}] 所有平台数据更新完成，共 {len(all_data)} 个平台的数据")
                
        except Exception as e:
            logger.error(f"[{datetime.now()}] 数据更新失败: {e}")
    
    def load_cached_data(self):
        """加载缓存的数据"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"加载缓存数据失败: {e}")
        
        # 如果加载失败，获取新数据
        self.update_data()
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def start_scheduler(self):
        """启动定时任务"""
        # 每30分钟更新一次数据
        schedule.every(30).minutes.do(self.update_data)
        
        # 同时每小时更新一次
        schedule.every().hour.do(self.update_data)
        
        logger.info("数据更新定时任务已启动...")
        
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
        
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
    
    def get_latest_data(self):
        """获取最新数据"""
        try:
            with self.lock:
                if os.path.exists(self.data_file):
                    # 检查文件修改时间
                    mod_time = datetime.fromtimestamp(os.path.getmtime(self.data_file))
                    if (datetime.now() - mod_time).seconds < 3600:  # 1小时内
                        with open(self.data_file, 'r', encoding='utf-8') as f:
                            return json.load(f)
                
                # 如果数据过旧或不存在，更新数据
                self.update_data()
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"获取最新数据失败: {e}")
            return self.load_cached_data()

# 全局实例
updater = DataUpdater()

if __name__ == "__main__":
    # 初始化并立即更新一次数据
    updater.update_data()
    
    # 启动定时任务
    updater.start_scheduler()
    
    # 保持程序运行
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        logger.info("\n数据更新服务已停止")