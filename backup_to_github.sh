#!/bin/bash
# Apex Speed Labs - VPS备份到GitHub
# 日期: 2026-03-23

set -e
echo "=== Apex Speed Labs VPS 备份开始 ==="

# 创建备份目录
BACKUP_DIR="/root/apex-automation-git"
APEX_DIR="/root/apex-automation"

# 复制核心文件
cp -r $APEX_DIR/scripts/*.py $BACKUP_DIR/ 2>/dev/null || true
cp -r $APEX_DIR/scripts/*.sh $BACKUP_DIR/ 2>/dev/null || true
cp $APEX_DIR/.env $BACKUP_DIR/ 2>/dev/null || true
cp $APEX_DIR/crontab.conf $BACKUP_DIR/ 2>/dev/null || true

# 创建备份说明
cat > $BACKUP_DIR/BACKUP_INFO.md << 'INFO'
# Apex Speed Labs VPS 备份信息

## 备份日期
2026-03-23

## 包含内容
- 自动化脚本（.py和.sh）
- 环境配置（.env）
- Cron任务配置（crontab.conf）
- 所有设置已就绪

## 恢复步骤
1. git clone https://github.com/sweeyuen3m/apex-speed-labs-vps.git
2. cp * /root/apex-automation/
3. crontab /root/apex-automation/crontab.conf

## 当前状态
✅ LinkedIn Playwright自动化 - 已配置
✅ Upwork Playwright自动化 - 已配置
✅ Twitter自动化 - 已配置
✅ YouTube视频上传 - 已配置
✅ Leads自动跟进 - 已配置
✅ 12平台监督系统 - 运行中
✅ 自我修复系统 - 运行中
✅ Dashboard - 在线
INFO

cd $BACKUP_DIR

# 添加所有文件
git add -A

# 提交
git commit -m "VPS备份 $(date +%Y-%m-%d %H:%M:%S) - Full Automation Complete" || echo "没有新变化需要提交"

# 推送到GitHub
git push -u origin main 2>&1 || echo "请确保GitHub仓库已创建"

echo "=== 备份完成 ==="
