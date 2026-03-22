#!/usr/bin/env python3
"""
LinkedIn 自动私信脚本 (VPS 版本)
优先使用 LinkedIn API，失败时切换到 Selenium 模式
"""
import os
import sys
import time
import random
import logging
from datetime import datetime
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv('/root/apex-automation/.env')

# 添加 modules 路径
sys.path.insert(0, '/root/apex-automation/modules')
from linkedin_automation import LinkedInAutomation
from email_sender import EmailSender

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/root/apex-automation/logs/linkedin.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 配置参数
CONFIG = {
    'max_messages': 30,  # 每次最多发送30条私信
    'search_keywords': [
        'property agent Singapore',
        'real estate Singapore',
        'ERA Singapore agent',
        'PropNex Singapore',
        'OrangeTee Singapore',
        'Huttons Singapore',
        'Dennis Wee Singapore'
    ],
    'message_templates': [
        """Hi {name},

I noticed you're in Singapore's real estate industry. My team at Apex Speed Labs specializes in AI-powered lead generation for property agents.

We've been helping Singapore agents:
- Generate 300%+ more qualified property leads
- Save 20+ hours per week on manual outreach
- Close deals 50% faster

Special Offer for Singapore Property Agents:
✅ 7-day free trial (no credit card required)
✅ 70% off your first month
✅ 5 free property leads to test our system
✅ 24/7 local Singapore support

Would you be open to a quick 15-minute call to see if this could work for your business?

Best regards,
Steven Wong
CEO, Apex Speed Labs
+65 9298 4102
https://leads-improvement.sweeyuen3.workers.dev""",
    ]
}

class LinkedInAutoMessenger:
    def __init__(self):
        self.api_bot = None
        self.selenium_bot = None
        self.use_api = True  # 默认使用 API
        self.sent_count = 0
        self.failed_count = 0
        self.results = []

    def init_api_bot(self):
        """初始化 LinkedIn API Bot"""
        try:
            self.api_bot = LinkedInAutomation()
            if self.api_bot.access_token:
                logger.info("✅ LinkedIn API Bot 初始化成功")
                return True
            else:
                logger.warning("⚠️ LinkedIn Access Token 未配置，切换到 Selenium 模式")
                self.use_api = False
                return False
        except Exception as e:
            logger.error(f"❌ LinkedIn API Bot 初始化失败: {e}")
            self.use_api = False
            return False

    def init_selenium_bot(self):
        """初始化 Selenium Bot"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.binary_location = '/snap/bin/chromium'

            self.selenium_bot = webdriver.Chrome(options=chrome_options)
            logger.info("✅ Selenium Bot 初始化成功")
            return True
        except Exception as e:
            logger.error(f"❌ Selenium Bot 初始化失败: {e}")
            return False

    def send_message_api(self, recipient_urn, message):
        """使用 API 发送私信"""
        if not self.api_bot:
            return False

        try:
            success = self.api_bot.send_message(recipient_urn, message)
            if success:
                self.sent_count += 1
                return True
            else:
                self.failed_count += 1
                return False
        except Exception as e:
            logger.error(f"❌ API 发送失败: {e}")
            self.failed_count += 1
            return False

    def send_message_selenium(self, profile_url, message):
        """使用 Selenium 发送私信"""
        if not self.selenium_bot:
            return False

        try:
            # 打开用户资料页
            self.selenium_bot.get(profile_url)
            time.sleep(2)

            # 查找 Message 按钮
            try:
                message_button = WebDriverWait(self.selenium_bot, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Message')]"))
                )
                message_button.click()
                time.sleep(2)

                # 输入消息
                message_box = self.selenium_bot.find_element(By.CSS_SELECTOR, "div[contenteditable='true']")
                message_box.send_keys(message)
                time.sleep(1)

                # 发送（Enter 键）
                message_box.send_keys(Keys.ENTER)
                time.sleep(2)

                logger.info(f"✅ Selenium 发送成功: {profile_url}")
                self.sent_count += 1
                return True

            except Exception as e:
                logger.warning(f"❌ Selenium 发送失败: {e}")
                self.failed_count += 1
                return False

        except Exception as e:
            logger.error(f"❌ Selenium 异常: {e}")
            self.failed_count += 1
            return False

    def get_test_recipients(self):
        """获取测试收件人列表（模拟数据）"""
        # 注意：实际使用时需要替换为真实的用户 URN 或 URL
        recipients = []

        # 从文件读取（如果存在）
        recipients_file = '/root/apex-automation/data/linkedin_targets.json'
        if os.path.exists(recipients_file):
            with open(recipients_file, 'r', encoding='utf-8') as f:
                recipients = json.load(f)
            logger.info(f"📋 从文件加载 {len(recipients)} 个目标")
        else:
            logger.warning("⚠️ 未找到目标文件，使用模拟数据")
            # 模拟数据（需要替换为真实的）
            for i in range(10):
                recipients.append({
                    'urn': f'urn:li:person:mock_{i}',
                    'url': f'https://www.linkedin.com/in/mock-user-{i}/',
                    'name': f'Property Agent {i+1}',
                })

        return recipients

    def run(self):
        """主执行流程"""
        logger.info("🚀 开始 LinkedIn 自动私信任务")
        logger.info(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # 初始化 API Bot
        if self.init_api_bot():
            logger.info("📡 使用 LinkedIn API 模式")
        else:
            logger.info("🌐 切换到 Selenium 模式")
            if not self.init_selenium_bot():
                logger.error("❌ 无法初始化 Selenium，退出")
                return

        # 获取目标列表
        recipients = self.get_test_recipients()
        if not recipients:
            logger.error("❌ 没有目标用户，退出")
            return

        logger.info(f"📊 目标用户数: {len(recipients)}")
        logger.info(f"🎯 最大发送数: {CONFIG['max_messages']}")

        # 遍历目标列表
        for i, recipient in enumerate(recipients):
            if self.sent_count >= CONFIG['max_messages']:
                logger.info(f"✅ 已达到最大发送数 {CONFIG['max_messages']}")
                break

            # 生成消息
            template = random.choice(CONFIG['message_templates'])
            name = recipient.get('name', 'there')
            message = template.replace("{name}", name)

            # 发送消息
            success = False
            if self.use_api:
                success = self.send_message_api(recipient['urn'], message)
            else:
                success = self.send_message_selenium(recipient['url'], message)

            # 记录结果
            result = {
                'name': name,
                'urn': recipient.get('urn', 'N/A'),
                'url': recipient.get('url', 'N/A'),
                'status': 'success' if success else 'failed',
                'timestamp': datetime.now().isoformat()
            }
            self.results.append(result)

            # 延迟，避免被检测
            delay = random.uniform(10, 20)
            logger.info(f"⏸️ 延迟 {delay:.1f} 秒...")
            time.sleep(delay)

        # 保存结果
        self.save_results()

        # 发送通知邮件
        self.send_notification()

        # 清理
        if self.selenium_bot:
            self.selenium_bot.quit()

        logger.info(f"✅ 任务完成！发送 {self.sent_count} 条，失败 {self.failed_count} 条")
        logger.info(f"⏰ 结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def save_results(self):
        """保存结果到文件"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'/root/apex-automation/logs/linkedin_results_{timestamp}.json'

        result_data = {
            'timestamp': datetime.now().isoformat(),
            'sent': self.sent_count,
            'failed': self.failed_count,
            'success_rate': (self.sent_count / (self.sent_count + self.failed_count) * 100) if (self.sent_count + self.failed_count) > 0 else 0,
            'results': self.results
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)

        logger.info(f"✅ 结果已保存到: {filename}")

    def send_notification(self):
        """发送通知邮件"""
        try:
            sender = EmailSender()
            if not sender.config.get('smtp_user'):
                logger.warning("⚠️ SMTP 未配置，跳过通知邮件")
                return

            subject = f"LinkedIn 自动私信完成 - {self.sent_count} 条发送成功"
            body = f"""LinkedIn 自动私信任务已完成

执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

统计信息:
- 发送成功: {self.sent_count} 条
- 发送失败: {self.failed_count} 条
- 成功率: {(self.sent_count / (self.sent_count + self.failed_count) * 100) if (self.sent_count + self.failed_count) > 0 else 0:.1f}%

详细结果已保存到 /root/apex-automation/logs/

Best regards,
Apex Speed Labs Automation
"""

            sender.send_email(
                to_email=sender.config['smtp_user'],
                subject=subject,
                body=body
            )
            logger.info("✅ 通知邮件已发送")

        except Exception as e:
            logger.error(f"❌ 发送通知邮件失败: {e}")

if __name__ == "__main__":
    try:
        bot = LinkedInAutoMessenger()
        bot.run()
    except KeyboardInterrupt:
        logger.info("⏹️ 用户中断执行")
    except Exception as e:
        logger.error(f"❌ 程序异常: {e}")
        import traceback
        traceback.print_exc()
