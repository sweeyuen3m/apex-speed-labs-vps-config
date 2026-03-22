#!/usr/bin/env python3
"""
Twitter自动发布系统 - API版本
全自动发布高吸引力Twitter内容
"""

import os
import sys
import json
import random
import logging
from datetime import datetime
import requests
from mastodon import Mastodon

# 配置日志
LOG_DIR = "/root/apex-automation/logs"
DATA_DIR = "/root/apex-automation/data"
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/twitter.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 加载配置
def load_config():
    env_file = "/root/apex-automation/.env"
    config = {}
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    config[key] = value
    return config

# Twitter内容模板
TWITTER_CONTENT = {
    "ai_tips": [
        "I just saved 10 hours this week using AI automation. Here's how:\n\n1. Auto-reply to common questions\n2. Generate content ideas\n3. Automate data entry\n\nThe ROI is insane.",
        "Stop manually doing what AI can do for free.\n\nMy top 3 free AI tools:\n1. ChatGPT - writing\n2. Claude - analysis\n3. Gemini - research\n\nWhat's your favorite?",
        "Hot take: AI won't replace you.\n\nPeople using AI will replace people not using AI.\n\nStart learning today.",
        "5 AI tools that made me $5000 this month:\n\n1. Claude - client work\n2. Midjourney - content\n3. NotebookLM - research\n4. Gemini - brainstorming\n5. Perplexity - SEO\n\nDM me for the full guide.",
    ],
    "business": [
        "My 30-day challenge:\n\nDay 1: Built an AI chatbot\nDay 7: Got first paying customer\nDay 14: Hit $1000 revenue\nDay 30: System running on autopilot\n\nYou can do this too.",
        "I turned $500 into $10,000 in 3 months.\n\nNot by working harder.\n\nBy automating everything.\n\nThe secret: Let AI do the work.",
        "The best time to start was 6 months ago.\n\nThe second best time is NOW.\n\nStop waiting for perfect conditions.\n\nShip it.",
    ],
    "motivation": [
        "Everyone wants to be an entrepreneur until they see the 4am work sessions.\n\nThen they go back to Netflix.\n\nYour choice.",
        "I failed 3 businesses before this one.\n\nEach failure taught me:\n- What NOT to do\n- Who NOT to partner with\n- What REALLY matters\n\nFailure is the tuition.",
        "Money doesn't solve your problems.\n\nBut it solves the problems that are distracting you from your real problems.",
        "Your network IS your net worth.\n\nMine grew 10x after I started helping people for free.\n\nGive value first.",
    ],
    "ai_news": [
        "Just tested the new Claude 3.5.\n\nIt's scary good at:\n- Writing code\n- Analyzing documents\n- Creative writing\n\nThe future is here.",
        "OpenAI just dropped something new.\n\nThe pace of AI development is accelerating.\n\nStay ahead: Learn AI tools NOW.",
        "AI startup funding hit $50B this year.\n\nThe gold rush is ON.\n\nBut the real money is in AI SERVICES.\n\nNot the models themselves.",
    ]
}

# 内容发布策略
def get_random_content():
    """获取随机内容"""
    category = random.choice(list(TWITTER_CONTENT.keys()))
    content = random.choice(TWITTER_CONTENT[category])
    return content, category

def post_to_twitter(content, config):
    """发布到Twitter (使用Mastodon API模拟)"""
    try:
        # 由于Twitter API需要OAuth，这里我们记录内容供后续发布
        logger.info(f"准备发布内容: {content[:50]}...")
        
        # 保存到发布队列
        queue_file = f"{DATA_DIR}/twitter_queue.json"
        queue = []
        if os.path.exists(queue_file):
            with open(queue_file, 'r') as f:
                queue = json.load(f)
        
        queue.append({
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'status': 'pending'
        })
        
        with open(queue_file, 'w') as f:
            json.dump(queue, f, indent=2)
        
        logger.info(f"✅ 内容已加入发布队列")
        return True
        
    except Exception as e:
        logger.error(f"发布失败: {e}")
        return False

def post_to_mastodon(content, config):
    """发布到Mastodon (作为Twitter替代)"""
    try:
        # Mastodon配置
        api_base_url = config.get('MASTODON_URL', 'https://mastodon.social')
        access_token = config.get('MASTODON_TOKEN', '')
        
        if not access_token:
            logger.warning("Mastodon Token未配置")
            return False
        
        mastodon = Mastodon(
            access_token=access_token,
            api_base_url=api_base_url
        )
        
        result = mastodon.toot(content)
        logger.info(f"✅ 已发布到Mastodon: {result['url']}")
        return True
        
    except Exception as e:
        logger.error(f"Mastodon发布失败: {e}")
        return False

def main():
    """主函数"""
    logger.info("="*50)
    logger.info("Twitter自动发布系统启动")
    logger.info("="*50)
    
    config = load_config()
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'posts_scheduled': 0,
        'posts_published': 0,
        'posts_failed': 0,
        'content': []
    }
    
    # 生成并安排内容
    num_posts = 3  # 每次发布3条
    
    for i in range(num_posts):
        content, category = get_random_content()
        
        # 尝试发布
        success = post_to_twitter(content, config)
        
        if success:
            results['posts_scheduled'] += 1
        else:
            results['posts_failed'] += 1
        
        results['content'].append({
            'category': category,
            'content': content,
            'success': success
        })
        
        # 随机延迟
        delay = random.randint(5, 15)
        logger.info(f"等待 {delay} 秒...")
        import time
        time.sleep(delay)
    
    # 保存结果
    result_file = f"{LOG_DIR}/twitter_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(result_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info("="*50)
    logger.info(f"任务完成! 安排 {results['posts_scheduled']} 条内容")
    logger.info("="*50)
    
    return results

if __name__ == "__main__":
    main()
