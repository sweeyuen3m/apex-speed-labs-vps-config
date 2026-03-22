#!/bin/bash
# 系统健康检查脚本
# 每日8AM自动执行

LOG_FILE="/Users/stevenwong/WorkBuddy/20260318123157/logs/health-check.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "========================================" >> "$LOG_FILE"
echo "系统健康检查 - $TIMESTAMP" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# 1. 检查Ollama服务
if pgrep -f "ollama serve" > /dev/null; then
    echo "✅ Ollama服务: 运行中" >> "$LOG_FILE"
else
    echo "❌ Ollama服务: 未运行" >> "$LOG_FILE"
fi

# 2. 检查Apex Brain
if curl -s -o /dev/null -w "%{http_code}" https://apex-brain.sweeyuen3.workers.dev | grep -q "200"; then
    echo "✅ Apex Brain: 正常 (HTTP 200)" >> "$LOG_FILE"
else
    echo "❌ Apex Brain: 异常" >> "$LOG_FILE"
fi

# 3. 检查Leads Improvement
if curl -s -o /dev/null -w "%{http_code}" https://leads-improvement.sweeyuen3.workers.dev | grep -q "200"; then
    echo "✅ Leads Improvement: 正常 (HTTP 200)" >> "$LOG_FILE"
else
    echo "❌ Leads Improvement: 异常" >> "$LOG_FILE"
fi

# 4. 检查磁盘空间
DISK_USAGE=$(df -h /System/Volumes/Data | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -lt 90 ]; then
    echo "✅ 磁盘空间: ${DISK_USAGE}% (健康)" >> "$LOG_FILE"
else
    echo "⚠️ 磁盘空间: ${DISK_USAGE}% (需关注)" >> "$LOG_FILE"
fi

# 5. 检查内存使用
MEM_FREE=$(vm_stat | grep "Pages free" | awk '{print $3}' | sed 's/\.//')
MEM_TOTAL=$(sysctl -n hw.memsize | awk '{print $1/4096}')
MEM_USAGE=$(echo "scale=1; 100 - ($MEM_FREE * 16384 / $MEM_TOTAL * 100)" | bc)
echo "📊 内存使用率: ${MEM_USAGE}%" >> "$LOG_FILE"

# 6. 检查最近自动化执行日志
echo "" >> "$LOG_FILE"
echo "=== 最近的自动化执行 ===" >> "$LOG_FILE"
echo "Upwork自动化:" >> "$LOG_FILE"
tail -3 /Users/stevenwong/WorkBuddy/20260318123157/logs/upwork-auto.log 2>/dev/null || echo "暂无日志" >> "$LOG_FILE"

echo "LinkedIn自动化:" >> "$LOG_FILE"
tail -3 /Users/stevenwong/WorkBuddy/20260318123157/logs/linkedin-auto.log 2>/dev/null || echo "暂无日志" >> "$LOG_FILE"

echo "财务监控:" >> "$LOG_FILE"
tail -3 /Users/stevenwong/WorkBuddy/20260318123157/logs/finance-monitor.log 2>/dev/null || echo "暂无日志" >> "$LOG_FILE"

echo "" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "检查完成" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
