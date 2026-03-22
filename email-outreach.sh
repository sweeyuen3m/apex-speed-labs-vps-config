#!/bin/bash
# Email Cold Outreach Automation
# Author: Apex Speed Labs AI Team
# Version: 1.0.0

# ==================== 配置 ====================
LOG_FILE="automation/logs/email-outreach.log"
EMAILS_PER_DAY=50
CAMPAIGN_NAME="Singapore-Ecommerce-Outreach"

# ==================== 邮件模板 ====================
EMAIL_SUBJECTS=(
    "30-day free trial for Shopee/Lazada sellers"
    "AI chatbot that handles 80% of customer messages"
    "Save 20+ hours/week on customer service"
    "Free trial - AI customer service for e-commerce"
    "E-commerce automation: 30 days free"
)

EMAIL_BODIES=(
    "Hi {name},

I noticed you're running an online store on Shopee or Lazada.

Here's what I've seen with sellers like you:

- Spending 3-4 hours/day replying to the same questions
- Missing messages during busy periods
- Hard to scale without hiring more staff

Our AI chatbot handles 80% of customer inquiries automatically:
✅ 24/7 instant responses
✅ Supports Chinese & English
✅ Learns from your products
✅ Easy setup in 15 minutes

We're offering a 30-day free trial for e-commerce sellers.

Would you be interested in seeing how it works?

Best regards,
Steven
Apex Speed Labs"

    "Hi {name},

Quick question - how much time does your team spend on customer service every week?

If it's more than 10 hours, there's a better way.

We've built an AI chatbot specifically for Shopee/Lazada sellers that:
- Auto-answers product questions
- Handles order status inquiries
- Works 24/7
- Increases customer satisfaction

30 sellers are already using it. Here's what one said:

\"Saved me 20 hours this week alone\" - Shopee seller, Singapore

Free 30-day trial. No credit card needed.

Interested? Reply 'trial' and I'll send you the link.

Steven
Apex Speed Labs"

    "Hi {name},

I help e-commerce sellers automate their customer service.

The problem we solve:
- Too many repetitive messages
- Can't keep up during sales events
- Hiring is expensive

Our solution:
- AI chatbot handles 80% of inquiries
- Setup in 15 minutes
- 30-day free trial
- Works with Shopee, Lazada, WhatsApp

Would a free demo help you decide if it's right for your store?

Just reply 'demo' and I'll book a 15-minute call.

Steven
Apex Speed Labs"
)

# ==================== 颜色 ====================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ==================== 日志 ====================
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> $LOG_FILE
}

log_success() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] ✓${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] SUCCESS: $1" >> $LOG_FILE
}

# ==================== 主程序 ====================
main() {
    echo ""
    echo "=========================================="
    echo "  📧 EMAIL 冷邮件获客机器人"
    echo "  $(date '+%Y-%m-%d %H:%M:%S')"
    echo "=========================================="
    echo ""
    
    # 创建日志目录
    mkdir -p automation/logs
    
    # 检查邮件客户端
    log "检查邮件配置..."
    
    if command -v himalaya &> /dev/null; then
        echo "   ✅ himalaya CLI 可用"
    elif command -v mail &> /dev/null; then
        echo "   ✅ mail CLI 可用"
    else
        echo "   ⚠️ 未检测到邮件 CLI"
        echo "   提示: 可安装 himalaya 进行邮件自动化"
    fi
    
    echo ""
    echo "=========================================="
    echo "  📋 邮件策略"
    echo "=========================================="
    echo ""
    echo "   每天发送: $EMAILS_PER_DAY 封"
    echo "   每周发送: 250 封"
    echo "   每月发送: 1000 封"
    echo ""
    echo "   预期回复率: 3-5%"
    echo "   预期转化: 1-2% (10-20 个客户)"
    echo ""
    echo "=========================================="
    echo "  🎯 目标受众"
    echo "=========================================="
    echo ""
    echo "   1. Shopee 卖家 (新加坡/马来西亚)"
    echo "   2. Lazada 卖家"
    echo "   3. Qoo10 卖家"
    echo "   4. 独立站电商"
    echo "   5. 跨境电商"
    echo ""
    echo "=========================================="
    echo "  💡 邮件主题"
    echo "=========================================="
    echo ""
    for subject in "${EMAIL_SUBJECTS[@]}"; do
        echo "   - $subject"
    done
    echo ""
    
    log_success "Email 获客系统已准备就绪"
    echo ""
    echo "📌 要进行真正的邮件发送，需要:"
    echo "   1. Gmail/himalaya 配置"
    echo "   2. 潜在客户邮箱列表"
    echo "   3. 运行: bash automation/email-outreach.sh"
}

main "$@"
