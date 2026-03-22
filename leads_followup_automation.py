#!/usr/bin/env python3
"""
Leads 自动跟进系统
自动跟进潜在客户，发送邮件和 LinkedIn 消息
"""
import os
import sys
import time
import random
import logging
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 添加 modules 路径
sys.path.insert(0, '/root/apex-automation/modules')

from email_sender import EmailSender

# 加载 .env 文件
load_dotenv('/root/apex-automation/.env')

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/root/apex-automation/logs/leads_followup.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 配置参数
CONFIG = {
    'leads_file': '/root/apex-automation/data/leads_database.json',
    'followup_interval_days': 3,  # 每 3 天跟进一次
    'max_followups_per_run': 20,
    'followup_templates': [
        {
            'day_offset': 3,
            'subject': 'Quick check-in - {{name}}',
            'message': """Hi {{name}},

I wanted to quickly follow up and see if you had any questions about our AI-powered lead generation service.

Quick reminder of what we offer:
- Generate 300% more qualified leads
- Save 20+ hours per week on manual outreach
- Close deals 50% faster

Would you be open to a quick 15-minute call to learn more?

Best regards,
Steven Wong
CEO, Apex Speed Labs
+65 9298 4102
https://leads-improvement.sweeyuen3.workers.dev"""
        },
        {
            'day_offset': 7,
            'subject': 'Limited time offer - 70% OFF for {{name}}!',
            'message': """Hi {{name}},

We have a special offer just for you!

Limited Time Offer:
✅ 70% OFF your first month
✅ Promo Code: WELCOME70
✅ Valid until: 2026-04-30

What You Get:
- AI-powered lead generation
- 300% more qualified leads
- Save 20+ hours per week
- Close deals 50% faster

Don't miss out! Use your promo code now.

Claim Your Offer: https://leads-improvement.sweeyuen3.workers.dev

Best regards,
Steven Wong
CEO, Apex Speed Labs
+65 9298 4102"""
        },
        {
            'day_offset': 14,
            'subject': 'Last chance - Exclusive offer for {{name}}',
            'message': """Hi {{name}},

This is your last chance to take advantage of our special offer!

Final Offer:
✅ 70% OFF your first month
✅ 5 Free Property Leads
✅ Promo Code: WELCOME70
✅ Expires: 2026-03-31

Don't miss out on this opportunity to transform your lead generation!

Act Now: https://leads-improvement.sweeyuen3.workers.dev

Best regards,
Steven Wong
CEO, Apex Speed Labs
+65 9298 4102"""
        }
    ]
}

class LeadsFollowupAutomation:
    def __init__(self):
        self.email_sender = EmailSender()
        self.followup_count = 0
        self.failed_count = 0
        self.results = []
    
    def load_leads(self):
        """加载 leads 数据库"""
        if not os.path.exists(CONFIG['leads_file']):
            logger.warning(f"⚠️ Leads 文件不存在: {CONFIG['leads_file']}")
            return []
        
        with open(CONFIG['leads_file'], 'r', encoding='utf-8') as f:
            leads = json.load(f)
        
        logger.info(f"📋 加载了 {len(leads)} 个 leads")
        return leads
    
    def save_leads(self, leads):
        """保存 leads 数据库"""
        with open(CONFIG['leads_file'], 'w', encoding='utf-8') as f:
            json.dump(leads, f, ensure_ascii=False, indent=2)
        logger.info("✅ Leads 数据库已保存")
    
    def get_leads_needing_followup(self, leads):
        """获取需要跟进的 leads"""
        today = datetime.now()
        leads_needing_followup = []
        
        for lead in leads:
            # 跳过已转化的 leads
            if lead.get('status') == 'converted':
                continue
            
            # 跳过已取消的 leads
            if lead.get('status') == 'cancelled':
                continue
            
            # 检查最后跟进时间
            last_contact = lead.get('last_contact_date')
            if not last_contact:
                # 如果从未联系过，需要首次联系
                leads_needing_followup.append({
                    'lead': lead,
                    'followup_type': 'first_contact'
                })
                continue
            
            # 计算距离上次联系的天数
            last_contact_date = datetime.fromisoformat(last_contact)
            days_since_contact = (today - last_contact_date).days
            
            # 检查是否需要跟进
            if days_since_contact >= CONFIG['followup_interval_days']:
                leads_needing_followup.append({
                    'lead': lead,
                    'followup_type': 'followup',
                    'days_since_contact': days_since_contact
                })
        
        logger.info(f"📊 找到 {len(leads_needing_followup)} 个需要跟进的 leads")
        return leads_needing_followup
    
    def get_followup_template(self, days_since_contact):
        """根据天数获取跟进模板"""
        for template in CONFIG['followup_templates']:
            if days_since_contact <= template['day_offset']:
                return template
        
        # 如果超过所有模板，使用最后一个
        return CONFIG['followup_templates'][-1]
    
    def send_email_followup(self, lead, followup_template):
        """发送邮件跟进"""
        try:
            # 替换模板变量
            subject = followup_template['subject'].replace('{{name}}', lead['name'])
            message = followup_template['message'].replace('{{name}}', lead['name'])
            
            # 发送邮件
            success = self.email_sender.send_email(
                to_email=lead['email'],
                subject=subject,
                body=message
            )
            
            if success:
                logger.info(f"✅ 邮件跟进发送成功: {lead['email']}")
                return True
            else:
                logger.error(f"❌ 邮件跟进发送失败: {lead['email']}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 邮件跟进异常: {e}")
            return False
    
    def send_linkedin_followup(self, lead, followup_template):
        """发送 LinkedIn 跟进（预留功能）"""
        # 这里可以集成 LinkedIn API 或 Selenium
        # 暂时跳过
        return True
    
    def update_lead_status(self, lead, followup_result):
        """更新 lead 状态"""
        lead['last_contact_date'] = datetime.now().isoformat()
        lead['followup_count'] = lead.get('followup_count', 0) + 1
        
        if followup_result['success']:
            lead['status'] = 'contacted'
        else:
            lead['status'] = 'failed'
        
        return lead
    
    def run(self):
        """主执行流程"""
        logger.info("🚀 开始 Leads 自动跟进任务")
        logger.info(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 加载 leads
        leads = self.load_leads()
        
        if not leads:
            logger.warning("⚠️ 没有 leads 数据，跳过")
            return
        
        # 获取需要跟进的 leads
        leads_needing_followup = self.get_leads_needing_followup(leads)
        
        if not leads_needing_followup:
            logger.info("✅ 没有 leads 需要跟进")
            return
        
        # 限制跟进数量
        leads_to_followup = leads_needing_followup[:CONFIG['max_followups_per_run']]
        logger.info(f"🎯 将跟进 {len(leads_to_followup)} 个 leads")
        
        # 跟进每个 lead
        for i, item in enumerate(leads_to_followup):
            lead = item['lead']
            followup_type = item.get('followup_type', 'followup')
            
            logger.info(f"\n{'='*50}")
            logger.info(f"处理 Lead {i+1}/{len(leads_to_followup)}: {lead['name']}")
            logger.info(f"跟进类型: {followup_type}")
            
            # 获取跟进模板
            if followup_type == 'first_contact':
                followup_template = CONFIG['followup_templates'][0]
            else:
                days_since_contact = item.get('days_since_contact', 0)
                followup_template = self.get_followup_template(days_since_contact)
            
            logger.info(f"使用模板: Day {followup_template['day_offset']}")
            
            # 发送跟进
            success = False
            
            # 邮件跟进
            if lead.get('email'):
                success = self.send_email_followup(lead, followup_template)
            
            # LinkedIn 跟进（如果有 LinkedIn URL）
            if lead.get('linkedin_url'):
                linkedin_success = self.send_linkedin_followup(lead, followup_template)
                if not success:
                    success = linkedin_success
            
            # 更新 lead 状态
            followup_result = {
                'success': success,
                'type': followup_type,
                'template_day': followup_template['day_offset'],
                'timestamp': datetime.now().isoformat()
            }
            
            lead = self.update_lead_status(lead, followup_result)
            
            # 记录结果
            result = {
                'lead_id': lead.get('id'),
                'name': lead['name'],
                'email': lead.get('email'),
                'followup_type': followup_type,
                'success': success,
                'timestamp': datetime.now().isoformat()
            }
            self.results.append(result)
            
            # 更新计数
            if success:
                self.followup_count += 1
            else:
                self.failed_count += 1
            
            # 延迟，避免被限流
            delay = random.uniform(30, 60)
            logger.info(f"⏸️ 延迟 {delay:.1f} 秒...")
            time.sleep(delay)
        
        # 保存 leads 数据库
        self.save_leads(leads)
        
        # 保存结果
        self.save_results()
        
        logger.info(f"\n✅ 任务完成！跟进 {self.followup_count} 个，失败 {self.failed_count} 个")
        logger.info(f"⏰ 结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def save_results(self):
        """保存结果到文件"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'/root/apex-automation/logs/leads_followup_results_{timestamp}.json'
        
        result_data = {
            'timestamp': datetime.now().isoformat(),
            'followup': self.followup_count,
            'failed': self.failed_count,
            'success_rate': (self.followup_count / (self.followup_count + self.failed_count) * 100) if (self.followup_count + self.failed_count) > 0 else 0,
            'results': self.results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✅ 结果已保存到: {filename}")

if __name__ == "__main__":
    try:
        automation = LeadsFollowupAutomation()
        automation.run()
    except KeyboardInterrupt:
        logger.info("⏹️ 用户中断执行")
    except Exception as e:
        logger.error(f"❌ 程序异常: {e}")
        import traceback
        traceback.print_exc()
