#!/usr/bin/env python3
"""
LinkedIn Messages - 10个话术版本 (A/B测试优化)
"""

LINKEDIN_MESSAGES = {
    # 直接推销型 (5个版本)
    'v1_direct_benefit': 'Hi {name},\n\nI noticed you\'re a top performer at {company}. I help real estate agents save 10+ hours per week with automated lead generation.\n\nWant to see how?',
    
    'v2_direct_stats': 'Hi {name},\n\nTop agents like you are closing 3x more deals with our AI-powered lead system.\n\nWant to see the numbers?',
    
    'v3_direct_time': 'Hi {name},\n\nWhat would you do with 10 extra hours every week?\n\nMy system generates qualified leads automatically. Interested in learning more?',
    
    'v4_direct_result': 'Hi {name},\n\nI help agents like you at {company} increase their commission by 30% through better leads.\n\nWant to see how it works?',
    
    'v5_direct_growth': 'Hi {name},\n\nLooking to scale your real estate business this quarter?\n\nI\'ve helped 50+ agents grow their pipeline with AI-powered leads. Let\'s connect.',
    
    # 价值主张型 (3个版本)
    'v6_value_problem': 'Hi {name},\n\nThe biggest challenge I hear from agents is finding time to prospect while serving clients.\n\nI\'ve built a system that solves this - it generates qualified leads while you sleep.\n\nCurious how it works?',
    
    'v7_value_competitive': 'Hi {name},\n\nIn today\'s market, agents with better leads win.\n\nMy system gives you a competitive advantage with AI-powered prospecting.\n\nWant to learn more?',
    
    'v8_value_system': 'Hi {name},\n\nImagine having a 24/7 lead generation machine that never takes a break.\n\nThat\'s what I\'ve built for successful agents. Interested in a demo?',
    
    # 关系建立型 (2个版本)
    'v9_relationship_curiosity': 'Hi {name},\n\nI\'ve been following {company}\'s growth in the Singapore market - impressive!\n\nQuick question: How are you currently finding new leads? I\'m curious about your process.',
    
    'v10_relationship_peer': 'Hi {name},\n\nFellow real estate professional here.\n\nI\'m testing a new AI lead generation system and looking for feedback from top performers like yourself.\n\nOpen to a quick chat?'
}

def get_message(variant, name='', company=''):
    """获取消息并填充变量"""
    if variant not in LINKEDIN_MESSAGES:
        return None
    message = LINKEDIN_MESSAGES[variant]
    return message.format(name=name, company=company)

def get_all_variants():
    """获取所有话术变体"""
    return list(LINKEDIN_MESSAGES.keys())

if __name__ == '__main__':
    print('LinkedIn Messages v2.0 - 10个话术版本')
    print('=' * 50)
    for variant in get_all_variants():
        print(f'\n{variant}:')
        print(get_message(variant, 'John', 'ERA Singapore'))
        print('-' * 50)
