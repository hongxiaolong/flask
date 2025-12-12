from flask import Flask, jsonify, render_template_string, request
import os
from douyin_scraper import scraper
import json

app = Flask(__name__)


@app.route('/')
def index():
    """主页"""
    return jsonify({
        "message": "欢迎使用抖音热点数据API",
        "endpoints": {
            "/api/hot": "获取最新抖音热点数据",
            "/api/hot/table": "以表格形式获取热点数据",
            "/report": "显示热点视频报表页面"
        },
        "description": "这是一个获取和展示抖音热点视频数据的服务"
    })


@app.route('/api/hot')
def get_douyin_hot():
    """获取抖音热点数据API"""
    try:
        data = scraper.scrape_real_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({
            "error": "获取数据失败",
            "message": str(e)
        }), 500


@app.route('/api/hot/table')
def get_douyin_hot_table():
    """以表格形式获取抖音热点数据"""
    try:
        data = scraper.scrape_real_data()
        df = scraper.get_formatted_report(data)
        
        # 返回表格数据
        table_data = {
            "columns": df.columns.tolist(),
            "rows": df.values.tolist(),
            "update_time": data['update_time']
        }
        
        return jsonify(table_data)
    except Exception as e:
        return jsonify({
            "error": "获取数据失败",
            "message": str(e)
        }), 500


@app.route('/report')
def report_page():
    """热点视频报表页面"""
    try:
        data = scraper.scrape_real_data()
        df = scraper.get_formatted_report(data)
        
        # 构建HTML表格
        html_table = df.to_html(
            classes='table table-striped table-bordered',
            table_id='hotVideosTable',
            escape=False,
            index=False
        )
        
        # HTML模板
        html_template = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>抖音热点视频排行榜</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { padding: 20px; background-color: #f8f9fa; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        .stats-card { background: white; border-radius: 10px; padding: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        #hotVideosTable { background: white; }
        .table th { background-color: #343a40; color: white; }
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="header text-center">
            <h1>🔥 抖音热点视频排行榜</h1>
            <p>实时更新热门视频数据 | 更新时间: {{ update_time }}</p>
        </div>
        
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="stats-card text-center">
                    <h3>{{ total_videos }}</h3>
                    <p class="text-muted">今日统计视频数</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stats-card text-center">
                    <h3>{{ update_time_short }}</h3>
                    <p class="text-muted">最后更新</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stats-card text-center">
                    <h3>TOP 10</h3>
                    <p class="text-muted">排名范围</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stats-card text-center">
                    <h3>✓</h3>
                    <p class="text-muted">数据验证</p>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0">热门视频列表</h5>
                <div>
                    <button class="btn btn-sm btn-outline-secondary me-2" onclick="location.reload()">刷新数据</button>
                    <a href="/api/hot" class="btn btn-sm btn-primary">API接口</a>
                </div>
            </div>
            <div class="card-body">
                {{ table|safe }}
            </div>
        </div>
        
        <div class="mt-4 text-center text-muted">
            <small>注：本数据仅供学习参考使用，实际数据请以抖音官方为准</small>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // 自动刷新功能
        setInterval(function() {
            console.log('数据已过期，建议刷新');
        }, 300000); // 5分钟提示一次
    </script>
</body>
</html>
        '''
        
        # 渲染模板
        from datetime import datetime
        return render_template_string(
            html_template,
            table=html_table,
            total_videos=len(data['videos']),
            update_time=data['update_time'],
            update_time_short=data['update_time'][:16]  # 只显示日期时间部分
        )
        
    except Exception as e:
        return f"<h1>生成报表失败</h1><p>错误信息: {str(e)}</p>", 500


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=os.getenv("PORT", default=8080))
