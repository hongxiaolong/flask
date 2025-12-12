# 多平台热点数据API服务

## 项目概述
这是一个用于获取和展示多个社交媒体平台（包括抖音、小红书、快手等）热点内容数据的Web服务。该服务提供API接口和可视化报表，帮助用户了解当前最热门的视频和内容。

## 功能特性
- 获取多个平台的热点内容数据（抖音、小红书、快手）
- 提供结构化的API接口
- 生成可视化的热点内容报表
- 支持数据格式化展示（播放量、点赞数等自动转换为易读格式）
- 提供跨平台内容聚合和对比分析
- 支持定时数据更新

## API端点

### 1. 主页
- **URL**: `/`
- **方法**: GET
- **描述**: 返回API服务的基本信息和可用端点

### 2. 抖音热点视频数据
- **URL**: `/api/hot`
- **方法**: GET
- **描述**: 获取最新的抖音热点视频数据
- **响应格式**:
```json
{
  "update_time": "2025-12-12 02:20:12",
  "total_videos": 10,
  "platform": "抖音",
  "videos": [
    {
      "rank": 1,
      "title": "视频标题",
      "author": "作者名称",
      "play_count": 1234567,
      "like_count": 98765,
      "comment_count": 4567,
      "share_count": 2345,
      "url": "视频链接",
      "publish_time": 1678886400,
      "hot_value": 95
    }
  ]
}
```

### 3. 表格格式数据（抖音）
- **URL**: `/api/hot/table`
- **方法**: GET
- **描述**: 以表格格式返回抖音热点视频数据
- **响应格式**:
```json
{
  "columns": ["rank", "title", "author", ...],
  "rows": [[1, "视频标题", "作者名", ...], ...],
  "update_time": "2025-12-12 02:20:12"
}
```

### 4. 指定平台热点数据
- **URL**: `/api/platform/<platform>`
- **方法**: GET
- **描述**: 获取指定平台的热点数据，支持 `douyin`, `xiaohongshu`, `kuaishou`
- **参数**: 
  - `platform`: 平台名称
- **响应格式**:
```json
{
  "update_time": "2025-12-12 02:20:12",
  "total_videos": 10,
  "platform": "小红书",
  "videos": [...]
}
```

### 5. 所有平台数据
- **URL**: `/api/all_platforms`
- **方法**: GET
- **描述**: 获取所有平台的热点数据
- **响应格式**:
```json
{
  "douyin": {...},
  "xiaohongshu": {...},
  "kuaishou": {...}
}
```

### 6. 聚合数据
- **URL**: `/api/aggregated`
- **方法**: GET
- **描述**: 获取跨平台聚合的热点数据，按热度值统一排序
- **响应格式**:
```json
{
  "update_time": "2025-12-12 02:20:12",
  "total_videos": 30,
  "top_videos": [
    {
      "rank": 1,
      "platform": "抖音",
      "title": "视频标题",
      "author": "作者名称",
      ...
    }
  ],
  "platform_counts": {
    "抖音": 10,
    "小红书": 10,
    "快手": 10
  },
  "all_platforms_data": {...}
}
```

### 7. 抖音可视化报表页面
- **URL**: `/report`
- **方法**: GET
- **描述**: 返回抖音热点视频的交互式报表页面

### 8. 多平台综合报表页面
- **URL**: `/multi_report`
- **方法**: GET
- **描述**: 返回跨平台热点内容的综合报表页面

## 数据字段说明

| 字段 | 类型 | 描述 |
|------|------|------|
| rank | integer | 内容排名 |
| platform | string | 平台名称（聚合数据时） |
| title | string | 内容标题 |
| author | string | 发布者用户名 |
| play_count | integer | 播放/浏览次数 |
| like_count | integer | 点赞次数 |
| comment_count | integer | 评论次数 |
| share_count | integer | 分享次数 |
| url | string | 内容链接 |
| publish_time | integer | 发布时间戳 |
| hot_value | integer | 热度值 |

## 部署说明

### 本地运行
```bash
pip install -r requirements.txt
python main.py
```

### 环境变量
- `PORT`: 服务端口，默认为8080

### 部署到云平台
项目配置了Railway部署支持，可以直接部署到Railway或其他云平台。

## 注意事项
- 当前版本使用模拟数据演示功能，实际生产环境中需要接入合法的第三方API或采用合规的数据获取方式
- 请遵守相关平台的使用条款和法律法规
- 建议在生产环境中使用缓存机制减少API请求频率
- 多平台数据聚合提供更全面的热点内容视图

## 测试
运行以下命令进行单元测试：
```bash
python test_douyin_scraper.py
```

## 扩展功能
- 支持多平台数据聚合
- 支持定时任务更新数据
- 支持多种数据格式输出
- 提供跨平台数据分析功能
- 支持历史数据对比
- 提供综合热度排行榜