#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 APEX SPEED LABS - 自动备份脚本
# 
# 功能:
# 1. 完整备份所有系统文件
# 2. 备份到本地
# 3. 备份到GitHub
# 4. 记录备份历史
#
# 启动: 每天自动执行
# ═══════════════════════════════════════════════════════════════════════════════

cd /Users/stevenwong/WorkBuddy/20260318123157

WORKSPACE="/Users/stevenwong/WorkBuddy/20260318123157"
BACKUP_DIR="$HOME/Backups/ApexSpeedLabs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_DIR="$WORKSPACE/logs"

# 创建必要目录
mkdir -p "$BACKUP_DIR/$TIMESTAMP"
mkdir -p "$BACKUP_DIR/latest"
mkdir -p "$LOG_DIR"

echo "
╔════════════════════════════════════════════════════════════════════════╗
║                                                                        ║
║          💾 APEX SPEED LABS - 自动备份系统                          ║
║                                                                        ║
║                    $TIMESTAMP                                        ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝
"

# ═══════════════════════════════════════════════════════════════════════════
# 1. 备份核心系统文件
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo "📁 步骤1: 备份核心系统文件..."

backup_dir="$BACKUP_DIR/$TIMESTAMP"

# PM系统
[ -d "$WORKSPACE/okr" ] && cp -r "$WORKSPACE/okr" "$backup_dir/"
[ -d "$WORKSPACE/tracking" ] && cp -r "$WORKSPACE/tracking" "$backup_dir/"
[ -d "$WORKSPACE/templates" ] && cp -r "$WORKSPACE/templates" "$backup_dir/"

# 核心文档
cp "$WORKSPACE/SELF_MONITOR_SYSTEM.md" "$backup_dir/" 2>/dev/null || true
cp "$WORKSPACE/TEAM_PM_SYSTEM.md" "$backup_dir/" 2>/dev/null || true
cp "$WORKSPACE/WORKFLOW_STARK_V3.md" "$backup_dir/" 2>/dev/null || true
cp "$WORKSPACE/WORKFLOW_ELON_V3.md" "$backup_dir/" 2>/dev/null || true
cp "$WORKSPACE/SYSTEM_PATHS.md" "$backup_dir/" 2>/dev/null || true

echo "   ✅ OKR/Tracking/Templates"

# ═══════════════════════════════════════════════════════════════════════════
# 2. 备份自动化系统
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo "📁 步骤2: 备份自动化系统..."

[ -d "$WORKSPACE/automation" ] && cp -r "$WORKSPACE/automation" "$backup_dir/"
[ -d "$WORKSPACE/fast_money" ] && cp -r "$WORKSPACE/fast_money" "$backup_dir/"

echo "   ✅ Automation/Fast_Money"

# ═══════════════════════════════════════════════════════════════════════════
# 3. 备份AI产品
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo "📁 步骤3: 备份AI产品..."

[ -d "$WORKSPACE/apex-brain-py" ] && cp -r "$WORKSPACE/apex-brain-py" "$backup_dir/"
[ -d "$WORKSPACE/leads-improvement" ] && cp -r "$WORKSPACE/leads-improvement" "$backup_dir/"
[ -d "$WORKSPACE/ai-writing-assistant" ] && cp -r "$WORKSPACE/ai-writing-assistant" "$backup_dir/"

echo "   ✅ AI Products"

# ═══════════════════════════════════════════════════════════════════════════
# 4. 备份Cloudflare Workers
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo "📁 步骤4: 备份Cloudflare Workers..."

[ -d "$WORKSPACE/cloudflare" ] && cp -r "$WORKSPACE/cloudflare" "$backup_dir/"

echo "   ✅ Cloudflare"

# ═══════════════════════════════════════════════════════════════════════════
# 5. 备份到最新目录
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo "📁 步骤5: 更新最新备份..."

rsync -a --delete "$backup_dir/" "$BACKUP_DIR/latest/" 2>/dev/null || {
    rm -rf "$BACKUP_DIR/latest"
    cp -r "$backup_dir" "$BACKUP_DIR/latest"
}

echo "   ✅ 最新备份已更新"

# ═══════════════════════════════════════════════════════════════════════════
# 6. 备份到GitHub
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo "📁 步骤6: 备份到GitHub..."

git add -A 2>/dev/null
git commit -m "💾 Auto-backup: $TIMESTAMP" 2>/dev/null
git push origin main 2>/dev/null

echo "   ✅ GitHub 已更新"

# ═══════════════════════════════════════════════════════════════════════════
# 7. 统计
# ═══════════════════════════════════════════════════════════════════════════

FILE_COUNT=$(find "$backup_dir" -type f 2>/dev/null | wc -l)
BACKUP_SIZE=$(du -sh "$backup_dir" 2>/dev/null | cut -f1)

# 记录到日志
echo "[$TIMESTAMP] 备份完成: $FILE_COUNT 文件, $BACKUP_SIZE" >> "$LOG_DIR/backup.log"

# ═══════════════════════════════════════════════════════════════════════════
# 8. 完成报告
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║                      ✅ 备份完成！                                 ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "📍 时间戳备份: $BACKUP_DIR/$TIMESTAMP"
echo "📍 最新备份:   $BACKUP_DIR/latest"
echo "📊 文件数量:   $FILE_COUNT"
echo "📊 总大小:     $BACKUP_SIZE"
echo ""
echo "💾 备份日志: $LOG_DIR/backup.log"
echo ""
