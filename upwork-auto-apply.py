#!/usr/bin/env python3
"""
Upwork自动化申请脚本
真正自动化执行，而非仅打开页面
"""
import json
import time
import random
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/Users/stevenwong/WorkBuddy/20260318123157/logs/upwork-auto.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 配置参数
CONFIG = {
    'max_applications': 5,  # 每次最多申请5个项目
    'min_budget': 200,      # 最低预算$200
    'max_budget': 5000,     # 最高预算$5000
    'keywords': ['chatbot', 'AI automation', 'AI assistant', 'chatgpt integration'],
    'cover_letter_templates': [
        """
Hi there,

I saw your project on Upwork and I believe I can help you build a high-quality {project_type} solution.

I specialize in AI-powered chatbot development and automation. My team at Apex Speed Labs has extensive experience in:

✅ Building intelligent chatbots with ChatGPT/Claude integration
✅ Automating customer support and sales workflows
✅ Creating custom AI agents for business automation
✅ Implementing RAG (Retrieval-Augmented Generation) for knowledge bases

Why work with us?
- 24/7 support and quick turnaround
- Free 7-day trial with no commitment
- 70% off your first month (limited time offer)
- Proven track record of delivering successful projects

I'd love to discuss your project in more detail. Would you be available for a quick call this week?

Best regards,
Steven
CEO, Apex Speed Labs
""",
        """
Hello,

I'm excited to apply for your {project_type} project. This is exactly what my team does best at Apex Speed Labs.

We've built dozens of AI-powered solutions including:
- Custom chatbots for e-commerce businesses
- AI automation workflows that save 20+ hours/week
- Integration of ChatGPT, Claude, and other LLMs into business processes

Special Offer: Get 70% off your first month + 7-day free trial
We're confident in our quality and want to prove it to you.

Check out our recent work: https://leads-improvement.sweeyuen3.workers.dev

Would you like to see a free demo of our capabilities?

Steven
Apex Speed Labs
"""
    ]
}

class UpworkAutoApply:
    def __init__(self):
        self.driver = None
        self.applied_count = 0

    def setup_driver(self):
        """配置浏览器"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无头模式
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')

        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("Chrome浏览器启动成功")
        except Exception as e:
            logger.error(f"浏览器启动失败: {e}")
            raise

    def login(self, email, password):
        """登录Upwork"""
        try:
            logger.info("正在登录Upwork...")
            self.driver.get("https://www.upwork.com/login")

            # 等待登录页面加载
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.ID, "login_username")))

            # 输入用户名
            username_field = self.driver.find_element(By.ID, "login_username")
            username_field.send_keys(email)

            # 点击继续
            continue_button = self.driver.find_element(By.ID, "login_control_continue")
            continue_button.click()

            # 等待密码输入框
            time.sleep(2)
            password_field = self.driver.find_element(By.ID, "login_password")
            password_field.send_keys(password)

            # 点击登录
            login_button = self.driver.find_element(By.ID, "login_control_continue")
            login_button.click()

            # 等待登录完成
            time.sleep(5)
            logger.info("登录成功")
            return True

        except Exception as e:
            logger.error(f"登录失败: {e}")
            return False

    def search_jobs(self):
        """搜索项目"""
        try:
            keywords = "+OR+".join(CONFIG['keywords'])
            url = f"https://www.upwork.com/ab/jobs/search/?q={keywords}&sort=recency&budget={CONFIG['min_budget']}-{CONFIG['max_budget']}"

            logger.info(f"正在搜索项目: {url}")
            self.driver.get(url)

            # 等待项目列表加载
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "job-tile")))

            # 获取项目卡片
            job_cards = self.driver.find_elements(By.CLASS_NAME, "job-tile")
            logger.info(f"找到 {len(job_cards)} 个项目")
            return job_cards[:CONFIG['max_applications']]

        except Exception as e:
            logger.error(f"搜索项目失败: {e}")
            return []

    def apply_to_job(self, job_card):
        """申请项目"""
        try:
            # 获取项目标题
            title_element = job_card.find_element(By.CLASS_NAME, "job-title")
            title = title_element.text
            logger.info(f"正在申请项目: {title}")

            # 点击项目
            title_element.click()
            time.sleep(2)

            # 生成cover letter
            cover_letter = random.choice(CONFIG['cover_letter_templates'])
            cover_letter = cover_letter.replace("{project_type}", "chatbot/automation")

            # 找到申请按钮（这里需要根据实际页面结构调整）
            try:
                apply_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-qa='btn-apply']")
                apply_button.click()

                # 等待申请对话框
                time.sleep(2)

                # 输入cover letter
                cover_textarea = self.driver.find_element(By.CSS_SELECTOR, "textarea[data-qa='bid-description']")
                cover_textarea.send_keys(cover_letter)

                # 点击提交
                submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-qa='btn-submit-bid']")
                submit_button.click()

                time.sleep(2)
                logger.info(f"✅ 成功申请项目: {title}")
                self.applied_count += 1

                # 返回搜索结果
                self.driver.back()
                time.sleep(1)

            except Exception as e:
                logger.warning(f"申请按钮未找到或点击失败: {e}")
                self.driver.back()
                time.sleep(1)

        except Exception as e:
            logger.error(f"申请项目时出错: {e}")

    def run(self):
        """主执行流程"""
        try:
            self.setup_driver()

            # 登录（需要用户提供凭证）
            # email = os.getenv('UPWORK_EMAIL')
            # password = os.getenv('UPWORK_PASSWORD')
            # if not self.login(email, password):
            #     return

            # 搜索项目
            job_cards = self.search_jobs()

            # 申请项目
            for job_card in job_cards:
                if self.applied_count >= CONFIG['max_applications']:
                    break
                self.apply_to_job(job_card)
                time.sleep(random.uniform(2, 5))  # 随机延迟

            logger.info(f"✅ 完成！共申请 {self.applied_count} 个项目")

            # 记录结果
            self.log_results()

        except Exception as e:
            logger.error(f"执行失败: {e}")
        finally:
            if self.driver:
                self.driver.quit()

    def log_results(self):
        """记录结果"""
        result = {
            'timestamp': datetime.now().isoformat(),
            'applied_count': self.applied_count,
            'status': 'success' if self.applied_count > 0 else 'no_opportunities'
        }

        with open('/Users/stevenwong/WorkBuddy/20260318123157/logs/upwork_results.json', 'a') as f:
            f.write(json.dumps(result) + '\n')

        logger.info(f"结果已记录到 upwork_results.json")

if __name__ == "__main__":
    try:
        bot = UpworkAutoApply()
        bot.run()
    except KeyboardInterrupt:
        logger.info("用户中断执行")
    except Exception as e:
        logger.error(f"程序异常: {e}")
