#!/usr/bin/env python3
"""
客户跟进自动化系统
自动追踪客户状态，发送个性化跟进消息
"""

import json
import os
from datetime import datetime, timedelta

# 跟进策略模板
FOLLOWUP_TEMPLATES = {
    'new_lead': {
        'day_1': 'Thanks for your interest! Here is more info about our AI lead generation system...',
        'day_3': 'Quick follow-up - any questions?',
        'day_7': 'Thought you might like to see a demo...',
        'day_14': 'Still interested in saving 10+ hours/week?',
    },
    'contacted': {
        'day_2': 'Thanks for connecting! Here is what I promised...',
        'day_5': 'Any thoughts on the proposal?',
        'day_10': 'Ready to move forward?',
    },
    'demo_scheduled': {
        'day_0': 'Demo confirmed for {datetime}. See you then!',
        'day_1': 'Thanks for attending the demo! Here is the recording...',
    },
    'proposal_sent': {
        'day_1': 'Did you get a chance to review the proposal?',
        'day_3': 'Any questions about pricing?',
        'day_7': 'Limited time offer - 20% off if you sign this week',
    }
}

class CustomerFollowupSystem:
    def __init__(self, data_file='data/customers.json'):
        self.data_file = data_file
        self.customers = {}
        self.load_data()
    
    def load_data(self):
        """加载客户数据"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.customers = json.load(f)
        else:
            os.makedirs(os.path.dirname(self.data_file) or '.', exist_ok=True)
    
    def save_data(self):
        """保存客户数据"""
        with open(self.data_file, 'w') as f:
            json.dump(self.customers, f, indent=2)
    
    def add_customer(self, email, name, company):
        """添加新客户"""
        self.customers[email] = {
            'email': email,
            'name': name,
            'company': company,
            'created_at': datetime.now().isoformat(),
            'status': 'new_lead',
            'last_followup_day': 0,
            'followup_count': 0
        }
        self.save_data()
    
    def update_status(self, email, status):
        """更新客户状态"""
        if email in self.customers:
            self.customers[email]['status'] = status
            self.save_data()
    
    def get_pending_followups(self):
        """获取需要跟进的客户"""
        pending = []
        now = datetime.now()
        
        for email, customer in self.customers.items():
            status = customer.get('status', 'new_lead')
            if status not in FOLLOWUP_TEMPLATES:
                continue
            
            created_at = datetime.fromisoformat(customer['created_at'])
            days_since_creation = (now - created_at).days
            
            templates = FOLLOWUP_TEMPLATES[status]
            for day_offset_str, message in templates.items():
                day_num = int(day_offset_str.split('_')[1])
                
                if days_since_creation >= day_num and customer['last_followup_day'] < day_num:
                    pending.append({
                        'email': email,
                        'customer': customer,
                        'message': message,
                        'status': status,
                        'followup_day': day_num
                    })
        
        return pending
    
    def mark_followup_sent(self, email, day_num):
        """标记跟进已发送"""
        if email in self.customers:
            self.customers[email]['last_followup_day'] = day_num
            self.customers[email]['followup_count'] += 1
            self.save_data()
    
    def get_summary(self):
        """获取摘要信息"""
        return {
            'total_customers': len(self.customers),
            'by_status': {
                'new_lead': len([c for c in self.customers.values() if c['status'] == 'new_lead']),
                'contacted': len([c for c in self.customers.values() if c['status'] == 'contacted']),
                'demo_scheduled': len([c for c in self.customers.values() if c['status'] == 'demo_scheduled']),
                'proposal_sent': len([c for c in self.customers.values() if c['status'] == 'proposal_sent']),
            }
        }

if __name__ == '__main__':
    system = CustomerFollowupSystem()
    
    print('=== 客户跟进自动化系统 ===')
    summary = system.get_summary()
    print(f'总客户数: {summary["total_customers"]}')
    print(f'按状态: {summary["by_status"]}')
    
    pending = system.get_pending_followups()
    print(f'\n需要跟进的客户: {len(pending)}')
    for item in pending[:5]:
        print(f'  - {item["customer"]["name"]} ({item["status"]}, Day {item["followup_day"]})')
