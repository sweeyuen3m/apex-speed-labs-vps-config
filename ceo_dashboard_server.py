#!/usr/bin/env python3
"""
Apex Speed Labs - CEO Dashboard (实时版)
显示所有14个平台的自动化状态
"""

from flask import Flask, render_template_string
import os
import subprocess
from datetime import datetime
import requests

app = Flask(__name__)

# 平台配置
PLATFORMS = {
    'twitter': {'name': 'Twitter/X', 'icon': '🐦', 'log': 'twitter.log'},
    'tiktok': {'name': 'TikTok', 'icon': '🎵', 'log': 'tiktok.log'},
    'youtube': {'name': 'YouTube', 'icon': '📹', 'log': 'youtube.log'},
    'xiaohongshu': {'name': '小红书', 'icon': '📕', 'log': 'xiaohongshu.log'},
    'douyin': {'name': '抖音', 'icon': '🎬', 'log': 'douyin.log'},
    'instagram': {'name': 'Instagram', 'icon': '📸', 'log': 'instagram.log'},
    'facebook': {'name': 'Facebook', 'icon': '👥', 'log': 'facebook.log'},
    'linkedin': {'name': 'LinkedIn', 'icon': '💼', 'log': 'linkedin.log'},
    'upwork': {'name': 'Upwork', 'icon': '💻', 'log': 'upwork.log'},
    'whatsapp': {'name': 'WhatsApp', 'icon': '📱', 'log': 'whatsapp.log'},
    'wechat': {'name': 'WeChat', 'icon': '💬', 'log': 'wechat.log'},
    'usdc': {'name': 'USDC监控', 'icon': '🔗', 'log': 'usdc.log'},
}

LOG_DIR = "/root/apex-automation/logs"

def get_log_count(log_file, days=0):
    """获取日志条目数"""
    try:
        with open(f"{LOG_DIR}/{log_file}", 'r') as f:
            lines = f.readlines()
        today = datetime.now().strftime('%Y-%m-%d')
        if days == 0:
            return sum(1 for line in lines if today in line)
        else:
            return len(lines)
    except:
        return 0

def check_service(url):
    """检查服务状态"""
    try:
        resp = requests.get(url, timeout=3)
        return resp.status_code == 200
    except:
        return False

def get_stripe_balance():
    """获取Stripe余额"""
    try:
        stripe_key = os.getenv('STRIPE_SECRET_KEY', '')
        if stripe_key:
            resp = requests.get('https://api.stripe.com/v1/balance', 
                              auth=(stripe_key, ''), timeout=5)
            if resp.status_code == 200:
                return resp.json()['available'][0]['amount'] / 100
    except:
        pass
    return 0

# HTML模板
DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Apex Speed Labs - CEO Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); min-height: 100vh; color: #fff; }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; padding: 30px 0; border-bottom: 2px solid rgba(255,255,255,0.1); margin-bottom: 30px; }
        .header h1 { font-size: 2.5em; background: linear-gradient(90deg, #00d4ff, #7c3aed); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .status-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .status-card { background: rgba(255,255,255,0.05); border-radius: 15px; padding: 25px; text-align: center; border: 1px solid rgba(255,255,255,0.1); }
        .status-card .icon { font-size: 3em; margin-bottom: 15px; }
        .status-card .value { font-size: 2em; font-weight: bold; color: #00d4ff; }
        .status-card.success { border-color: #00ff88; }
        .status-card.success .value { color: #00ff88; }
        .section-title { font-size: 1.5em; margin: 30px 0 20px; padding-left: 15px; border-left: 4px solid #7c3aed; }
        .platform-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }
        .platform-card { background: rgba(255,255,255,0.05); border-radius: 12px; padding: 20px; text-align: center; border: 1px solid rgba(255,255,255,0.1); }
        .platform-card .platform-icon { font-size: 2.5em; margin-bottom: 10px; }
        .platform-card .platform-name { font-size: 1.1em; font-weight: bold; margin-bottom: 10px; }
        .platform-card .stat-row { display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
        .platform-card .stat-value { color: #00d4ff; font-weight: bold; }
        .platform-card .status { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.8em; margin-top: 10px; }
        .platform-card .status.active { background: rgba(0,255,136,0.2); color: #00ff88; }
        .platform-card .status.pending { background: rgba(255,170,0,0.2); color: #ffaa00; }
        .revenue-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .revenue-card { background: linear-gradient(135deg, rgba(124,58,237,0.2), rgba(0,212,255,0.2)); border-radius: 15px; padding: 25px; border: 1px solid rgba(124,58,237,0.3); }
        .revenue-card h3 { color: #7c3aed; margin-bottom: 15px; }
        .revenue-card .amount { font-size: 2.5em; font-weight: bold; color: #00d4ff; }
        .footer { text-align: center; padding: 30px 0; margin-top: 50px; border-top: 1px solid rgba(255,255,255,0.1); color: #666; }
        .auto-badge { display: inline-block; background: linear-gradient(90deg, #00ff88, #00d4ff); color: #000; padding: 8px 20px; border-radius: 20px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Apex Speed Labs</h1>
            <p>CEO Dashboard - Money Breeding Machine v3.1</p>
            <p style="color: #00ff88; margin-top: 15px;"><span class="auto-badge">⚡ FULL AUTO MODE</span></p>
            <p style="color: #888; margin-top: 10px;">最后更新: {{ last_update }}</p>
        </div>
        
        <div class="status-grid">
            <div class="status-card success">
                <div class="icon">🖥️</div>
                <div class="value">在线</div>
                <div>VPS (167.71.120.132)</div>
            </div>
            <div class="status-card success">
                <div class="icon">☁️</div>
                <div class="value">{{ cloud_status }}</div>
                <div>云服务</div>
            </div>
            <div class="status-card success">
                <div class="icon">⚡</div>
                <div class="value">{{ total_today }}</div>
                <div>今日执行总数</div>
            </div>
            <div class="status-card">
                <div class="icon">💰</div>
                <div class="value">${{ stripe_balance }}</div>
                <div>Stripe 余额</div>
            </div>
        </div>
        
        <div class="revenue-grid">
            <div class="revenue-card">
                <h3>本周目标</h3>
                <div class="amount">$500 - $2,000</div>
            </div>
            <div class="revenue-card">
                <h3>本月目标</h3>
                <div class="amount">$3,000 - $10,000</div>
            </div>
            <div class="revenue-card">
                <h3>本季目标</h3>
                <div class="amount">$15,000 - $50,000</div>
            </div>
        </div>
        
        <h2 class="section-title">📱 社交媒体平台 (7个)</h2>
        <div class="platform-grid">
            {% for p in social_platforms %}
            <div class="platform-card">
                <div class="platform-icon">{{ p.icon }}</div>
                <div class="platform-name">{{ p.name }}</div>
                <div class="stat-row"><span>今日</span><span class="stat-value">{{ p.today }}</span></div>
                <div class="stat-row"><span>本周</span><span class="stat-value">{{ p.week }}</span></div>
                <span class="status active">自动运行</span>
            </div>
            {% endfor %}
        </div>
        
        <h2 class="section-title">💼 商业平台 (5个)</h2>
        <div class="platform-grid">
            {% for p in business_platforms %}
            <div class="platform-card">
                <div class="platform-icon">{{ p.icon }}</div>
                <div class="platform-name">{{ p.name }}</div>
                <div class="stat-row"><span>今日</span><span class="stat-value">{{ p.today }}</span></div>
                <div class="stat-row"><span>本周</span><span class="stat-value">{{ p.week }}</span></div>
                <span class="status active">自动运行</span>
            </div>
            {% endfor %}
        </div>
        
        <h2 class="section-title">💎 支付与系统 (2个)</h2>
        <div class="platform-grid">
            <div class="platform-card">
                <div class="platform-icon">💳</div>
                <div class="platform-name">Stripe</div>
                <div class="stat-row"><span>余额</span><span class="stat-value">${{ stripe_balance }}</span></div>
                <div class="stat-row"><span>总收入</span><span class="stat-value">$0</span></div>
                <span class="status active">已连接</span>
            </div>
            <div class="platform-card">
                <div class="platform-icon">🔗</div>
                <div class="platform-name">USDC监控</div>
                <div class="stat-row"><span>今日检查</span><span class="stat-value">{{ usdc_today }}</span></div>
                <div class="stat-row"><span>状态</span><span class="stat-value">监控中</span></div>
                <span class="status active">自动监控</span>
            </div>
        </div>
        
        <div class="footer">
            <p>VPS: 167.71.120.132</p>
            <p style="margin-top: 15px;"><span class="auto-badge">⚡ FULL AUTO MODE</span></p>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def dashboard():
    # 获取各平台数据
    social = ['twitter', 'tiktok', 'youtube', 'xiaohongshu', 'douyin', 'instagram', 'facebook']
    business = ['linkedin', 'upwork', 'whatsapp', 'wechat', 'usdc']
    
    social_platforms = []
    for p in social:
        info = PLATFORMS[p]
        social_platforms.append({
            'name': info['name'],
            'icon': info['icon'],
            'today': get_log_count(info['log']),
            'week': get_log_count(info['log'], 7)
        })
    
    business_platforms = []
    for p in business:
        info = PLATFORMS[p]
        business_platforms.append({
            'name': info['name'],
            'icon': info['icon'],
            'today': get_log_count(info['log']),
            'week': get_log_count(info['log'], 7)
        })
    
    usdc_today = get_log_count('usdc.log')
    total_today = sum(p['today'] for p in social_platforms + business_platforms)
    
    # 云服务状态
    apex = check_service('https://apex-brain.sweeyuen3.workers.dev')
    leads = check_service('https://leads-improvement.sweeyuen3.workers.dev')
    cloud_status = f"{'✅' if apex else '❌'}/{ '✅' if leads else '❌'}"
    
    # Stripe余额
    stripe_balance = get_stripe_balance()
    
    return render_template_string(DASHBOARD_HTML,
        last_update=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        cloud_status=cloud_status,
        total_today=total_today,
        stripe_balance=stripe_balance,
        social_platforms=social_platforms,
        business_platforms=business_platforms,
        usdc_today=usdc_today
    )

if __name__ == '__main__':
    print("🚀 CEO Dashboard 启动中...")
    print("📊 访问地址: http://167.71.120.132:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
