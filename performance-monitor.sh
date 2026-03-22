#!/bin/bash
# ═════════════════════════════════════════════════════════
#   Apex Speed Labs - VPS 性能监控脚本 (Linux)
#   频率: 每 5 分钟
# ═════════════════════════════════════════════════════════

LOG_FILE="/root/apex-automation/logs/performance.log"
mkdir -p "$(dirname "$LOG_FILE")"

# 获取当前时间
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
echo "[$TIMESTAMP] 性能监控开始..." >> "$LOG_FILE"

# 1. CPU 使用率
echo "--- CPU 使用率 ---" >> "$LOG_FILE"
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
echo "CPU 使用率: ${CPU_USAGE}%" >> "$LOG_FILE"

# 2. 内存使用率
echo "--- 内存使用率 ---" >> "$LOG_FILE"
MEM_INFO=$(free -m | grep "Mem:")
MEM_TOTAL=$(echo "$MEM_INFO" | awk '{print $2}')
MEM_USED=$(echo "$MEM_INFO" | awk '{print $3}')
MEM_PERCENT=$((MEM_USED * 100 / MEM_TOTAL))
echo "内存使用: ${MEM_USED}MB / ${MEM_TOTAL}MB (${MEM_PERCENT}%)" >> "$LOG_FILE"

# 3. 磁盘使用率
echo "--- 磁盘使用率 ---" >> "$LOG_FILE"
DISK_USAGE=$(df -h / | tail -1 | awk '{print $5}' | cut -d'%' -f1)
echo "磁盘使用率: ${DISK_USAGE}%" >> "$LOG_FILE"

# 4. 系统负载
echo "--- 系统负载 ---" >> "$LOG_FILE"
LOAD_AVG=$(uptime | awk -F'load average:' '{print $2}')
echo "系统负载: ${LOAD_AVG}" >> "$LOG_FILE"

# 5. Docker 容器状态
echo "--- Docker 容器 ---" >> "$LOG_FILE"
CONTAINER_COUNT=$(docker ps --format "{{.Names}}" | wc -l)
echo "运行中的容器: ${CONTAINER_COUNT}" >> "$LOG_FILE"

# 6. Ollama 服务状态
echo "--- Ollama 服务 ---" >> "$LOG_FILE"
if pgrep -f "ollama serve" > /dev/null; then
    echo "Ollama 服务: ✅ 运行中" >> "$LOG_FILE"
else
    echo "Ollama 服务: ❌ 未运行" >> "$LOG_FILE"
fi

# 7. 检查异常情况
echo "--- 健康检查 ---" >> "$LOG_FILE"

# CPU 使用率 > 80%
if (( $(echo "$CPU_USAGE > 80" | bc -l) )); then
    echo "⚠️ 警告: CPU 使用率过高 (${CPU_USAGE}%)" >> "$LOG_FILE"
fi

# 内存使用率 > 80%
if [ "$MEM_PERCENT" -gt 80 ]; then
    echo "⚠️ 警告: 内存使用率过高 (${MEM_PERCENT}%)" >> "$LOG_FILE"
fi

# 磁盘使用率 > 80%
if [ "$DISK_USAGE" -gt 80 ]; then
    echo "⚠️ 警告: 磁盘使用率过高 (${DISK_USAGE}%)" >> "$LOG_FILE"
fi

echo "[$TIMESTAMP] 性能监控完成" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
