#!/bin/bash
# 🚀 Apex Speed Labs - 销售冲刺自动化
# 一次性执行所有销售渠道

echo "============================================"
echo "🚀 APEX SPEED LABS - 销售冲刺自动化"
echo "============================================"
echo ""

# 配置
LINKEDIN_COUNT=${1:-10}
UPWORK_COUNT=${2:-5}

# 1. LinkedIn 自动化
echo "📱 STEP 1: LinkedIn 自动化"
echo "-----------------------------------"
./automation/linkedin-batch.sh
echo ""

# 2. Upwork 自动化
echo "💼 STEP 2: Upwork 自动化"
echo "-----------------------------------"
./automation/upwork-batch.sh
echo ""

# 3. 发送 Stripe 支付链接提醒
echo "💰 STEP 3: 支付链接"
echo "-----------------------------------"
echo "支付链接已准备就绪："
echo "   试用套餐: https://buy.stripe.com/9B628k311fg7gWPcRO8k806"
echo "   Basic: https://buy.stripe.com/28EfZafNN0ld9uncRO8k807"
echo "   Professional: https://buy.stripe.com/00w7sE311aZR5e75pm8k808"
echo ""

echo "============================================"
echo "🎉 销售冲刺完成！"
echo "============================================"
echo ""
echo "📊 查看结果："
echo "   LinkedIn: https://www.linkedin.com/messaging"
echo "   Upwork: https://www.upwork.com/ab/find-work/"
echo "   Fiverr: https://www.fiverr.com/users/apexspeedlabs_sg/gigs"
echo "   Stripe: https://dashboard.stripe.com"
