#!/bin/bash

# ========================================
# 🚀 自动化系统 - 一键执行所有任务
# ========================================
# 功能：自动执行所有自动化任务
# ========================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

print_header() {
    echo ""
    print_message "$BLUE" "============================================================"
    print_message "$BLUE" "$1"
    print_message "$BLUE" "============================================================"
    echo ""
}

print_step() {
    print_message "$YELLOW" "📱 $1"
    echo ""
}

print_success() {
    print_message "$GREEN" "✅ $1"
}

print_warning() {
    print_message "$YELLOW" "⚠️  $1"
}

# 创建必要的目录
mkdir -p logs

print_header "🚀 自动化系统 - 一键执行所有任务"

print_message "$BLUE" "即将执行以下任务："
echo "  1. 提交 Upwork 提案（10个）⭐"
echo "  2. 发送 LinkedIn 私信（20条）"
echo "  3. 发布 Twitter 推文（3条）"
echo "  4. 配置 UptimeRobot 监控"
echo "  5. 配置邮件系统"
echo ""
print_message "$BLUE" "预计总时间：1-1.5 小时"
echo ""
print_warning "⚠️  注意："
echo "   - 确保已完成首次认证（运行 ./setup-auth.sh）"
echo "   - 检测到限制时，脚本会自动停止"
echo "   - 可以随时按 Ctrl+C 中断"
echo ""

read -p "准备好后按 Enter 开始..."

# 记录开始时间
START_TIME=$(date +%s)

# ========================================
# 任务 1: Upwork 提案
# ========================================
print_header "任务 1/5: 提交 Upwork 提案（10个）"

TASK_START_TIME=$(date +%s)
node scripts/upwork-humanized.js > logs/upwork-humanized.log 2>&1
TASK_END_TIME=$(date +%s)
TASK_DURATION=$((TASK_END_TIME - TASK_START_TIME))

print_success "Upwork 任务完成（耗时：${TASK_DURATION} 秒）"

# 等待用户确认
echo ""
read -p "Upwork 任务完成，按 Enter 继续..."

# ========================================
# 任务 2: LinkedIn 私信
# ========================================
print_header "任务 2/5: 发送 LinkedIn 私信（20条）"

TASK_START_TIME=$(date +%s)
node scripts/linkedin-humanized.js > logs/linkedin-humanized.log 2>&1
TASK_END_TIME=$(date +%s)
TASK_DURATION=$((TASK_END_TIME - TASK_START_TIME))

print_success "LinkedIn 任务完成（耗时：${TASK_DURATION} 秒）"

# 等待用户确认
echo ""
read -p "LinkedIn 任务完成，按 Enter 继续..."

# ========================================
# 任务 3: Twitter 发布
# ========================================
print_header "任务 3/5: 发布 Twitter 推文（3条）"

TASK_START_TIME=$(date +%s)
node scripts/twitter-post.js > logs/twitter-post.log 2>&1
TASK_END_TIME=$(date +%s)
TASK_DURATION=$((TASK_END_TIME - TASK_START_TIME))

print_success "Twitter 任务完成（耗时：${TASK_DURATION} 秒）"

# 等待用户确认
echo ""
read -p "Twitter 任务完成，按 Enter 继续..."

# ========================================
# 任务 4: UptimeRobot 配置
# ========================================
print_header "任务 4/5: 配置 UptimeRobot 监控"

TASK_START_TIME=$(date +%s)
node scripts/uptimerobot-setup.js > logs/uptimerobot-setup.log 2>&1
TASK_END_TIME=$(date +%s)
TASK_DURATION=$((TASK_END_TIME - TASK_START_TIME))

print_success "UptimeRobot 任务完成（耗时：${TASK_DURATION} 秒）"

# 等待用户确认
echo ""
read -p "UptimeRobot 任务完成，按 Enter 继续..."

# ========================================
# 任务 5: 邮件系统配置
# ========================================
print_header "任务 5/5: 配置邮件系统"

TASK_START_TIME=$(date +%s)
node scripts/email-setup.js > logs/email-setup.log 2>&1
TASK_END_TIME=$(date +%s)
TASK_DURATION=$((TASK_END_TIME - TASK_START_TIME))

print_success "邮件系统任务完成（耗时：${TASK_DURATION} 秒）"

# ========================================
# 执行摘要
# ========================================
END_TIME=$(date +%s)
TOTAL_DURATION=$((END_TIME - START_TIME))
TOTAL_MINUTES=$((TOTAL_DURATION / 60))

print_header "📊 执行摘要"

print_message "$BLUE" "总耗时：${TOTAL_DURATION} 秒（约 ${TOTAL_MINUTES} 分钟）"
echo ""
print_message "$BLUE" "详细日志："
echo "  - Upwork 提案: 查看 logs/upwork-humanized.log"
echo "  - LinkedIn 私信: 查看 logs/linkedin-humanized.log"
echo "  - Twitter 推文: 查看 logs/twitter-post.log"
echo "  - UptimeRobot: 查看 logs/uptimerobot-setup.log"
echo "  - 邮件系统: 查看 logs/email-setup.log"
echo ""
print_success "所有任务已完成！"

print_message "$BLUE" ""
print_message "$BLUE" "🎉 恭喜！所有自动化任务已完成！"
print_message "$BLUE" ""
print_message "$BLUE" "后续步骤："
print_message "$BLUE" "  1. 检查各平台的执行结果"
print_message "$BLUE" "  2. 监控客户响应和互动"
print_message "$BLUE$NC"
