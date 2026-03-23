#!/usr/bin/env python3
"""
Email Templates - 10个主题和内容版本 (A/B测试优化)
"""

EMAIL_SUBJECTS = {
    's1_benefit': 'Save 10+ hours/week with AI lead generation',
    's2_stats': 'How top agents close 3x more deals',
    's3_time': 'What would you do with 10 extra hours?',
    's4_result': 'Increase your commission by 30%',
    's5_growth': 'Scale your real estate business this quarter',
    's6_problem': 'Stop struggling with prospecting',
    's7_competitive': 'Your competitive advantage in today\'s market',
    's8_system': '24/7 lead generation system for top agents',
    's9_curiosity': 'Quick question about your lead process',
    's10_peer': 'Feedback requested: New AI lead system'
}

EMAIL_BODIES = {
    'body_standard': '''Hi {name},

I help real estate professionals like you generate qualified leads on autopilot.

My AI-powered system:
- Identifies high-intent prospects
- Delivers qualified leads daily
- Saves 10+ hours per week

Best of all? It works while you sleep.

Ready to see it in action?

Just reply "DEMO" and I'll show you how.

Best regards,
Steven Wong
Apex Speed Labs
+65 9298 4102
https://apex-speed-labs.com''',
    
    'body_short': '''Hi {name},

AI-powered lead generation that saves 10+ hours/week.

Want a demo?

Reply "DEMO" or book a call here: https://apex-speed-labs.com/demo

Steven
Apex Speed Labs''',
    
    'body_story': '''Hi {name},

Last week, I helped a real estate agent in Singapore close 3 more deals - all from leads our AI system generated.

She was spending 20+ hours/week prospecting. Now? She focuses on closing.

Her secret? Our AI-powered lead generation system.

Want the same results?

Reply "DEMO" and I'll show you how it works.

Best,
Steven Wong
Apex Speed Labs'''
}

def get_email(subject_variant, body_variant='body_standard', name=''):
    """获取完整邮件"""
    if subject_variant not in EMAIL_SUBJECTS or body_variant not in EMAIL_BODIES:
        return None, None
    
    subject = EMAIL_SUBJECTS[subject_variant]
    body = EMAIL_BODIES[body_variant].format(name=name)
    return subject, body

def get_all_subject_variants():
    """获取所有主题变体"""
    return list(EMAIL_SUBJECTS.keys())

def get_all_body_variants():
    """获取所有内容变体"""
    return list(EMAIL_BODIES.keys())

if __name__ == '__main__':
    print('Email Templates v2.0 - 10个主题版本')
    print('=' * 60)
    for subject_var in get_all_subject_variants():
        subject, body = get_email(subject_var, 'body_standard', 'John')
        print(f'\n{subject_var}: {subject}')
    print('\n' + '=' * 60)
