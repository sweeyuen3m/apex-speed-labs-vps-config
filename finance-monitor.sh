#!/bin/bash
# =====================================================
# APEX SPEED LABS - 财务自动监控系统
# Financial Auto-Monitoring System
# =====================================================

STRIPE_KEY="sk_live_XXXXX"
LOG_FILE="/Users/stevenwong/WorkBuddy/20260318123157/automation/logs/finance-monitor.log"
REPORT_FILE="/Users/stevenwong/WorkBuddy/20260318123157/FINANCIAL-DIRECTOR-REPORT.md"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

# 创建日志目录
mkdir -p "$(dirname $LOG_FILE)"

echo "========================================" >> $LOG_FILE
echo "财务监控 - $TIMESTAMP" >> $LOG_FILE
echo "========================================" >> $LOG_FILE

# 1. 检查 Stripe 余额
BALANCE=$(curl -s -X GET "https://api.stripe.com/v1/balance" \
  -u "$STRIPE_KEY:" \
  -H "Stripe-Version: 2023-10-16")

AVAILABLE=$(echo $BALANCE | python3 -c "
import sys, json
d = json.load(sys.stdin)
avail = d.get('available', [])
print(sum(c['amount'] for c in avail)/100)
")

PENDING=$(echo $BALANCE | python3 -c "
import sys, json
d = json.load(sys.stdin)
pend = d.get('pending', [])
print(sum(c['amount'] for c in pend)/100)
")

echo "可用余额: $AVAILABLE SGD" >> $LOG_FILE
echo "待处理: $PENDING SGD" >> $LOG_FILE

# 2. 检查支付数
PAYMENTS=$(curl -s -X GET "https://api.stripe.com/v1/payments?limit=10" \
  -u "$STRIPE_KEY:" \
  -H "Stripe-Version: 2023-10-16")

PAYMENT_COUNT=$(echo $PAYMENTS | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(len(d.get('data', [])))
")

echo "支付数: $PAYMENT_COUNT" >> $LOG_FILE

# 3. 检查客户数
CUSTOMERS=$(curl -s -X GET "https://api.stripe.com/v1/customers?limit=10" \
  -u "$STRIPE_KEY:" \
  -H "Stripe-Version: 2023-10-16")

CUSTOMER_COUNT=$(echo $CUSTOMERS | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(len(d.get('data', [])))
")

echo "客户数: $CUSTOMER_COUNT" >> $LOG_FILE

# 4. 检查订阅
SUBS=$(curl -s -X GET "https://api.stripe.com/v1/subscriptions?limit=10" \
  -u "$STRIPE_KEY:" \
  -H "Stripe-Version: 2023-10-16")

SUB_COUNT=$(echo $SUBS | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(len(d.get('data', [])))
")

echo "订阅数: $SUB_COUNT" >> $LOG_FILE

# 5. 发送通知如果有新收入
if (( $(echo "$AVAILABLE > 0" | bc -l) )); then
    echo "🎉 新收入检测到！$AVAILABLE SGD" >> $LOG_FILE
    # 可以添加通知逻辑 (Telegram/Email)
fi

echo "" >> $LOG_FILE

# 输出最新状态
echo "=== 财务状态 ($TIMESTAMP) ==="
echo "可用余额: $AVAILABLE SGD"
echo "待处理: $PENDING SGD"
echo "支付数: $PAYMENT_COUNT"
echo "客户数: $CUSTOMER_COUNT"
echo "订阅数: $SUB_COUNT"

# 如果有收入，触发通知
if (( $(echo "$AVAILABLE > 0" | bc -l) )); then
    echo ""
    echo "🎉🎉🎉 第一笔收入！！！ 🎉🎉🎉"
fi
