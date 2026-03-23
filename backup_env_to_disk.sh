#!/bin/bash
# 只备份 .env 到外接硬盘
# 永远不会上传到GitHub

set -e
echo '=== .env 备份到外接硬盘 ==='

# 外接硬盘路径
DISK_PATH='/Volumes/Steven/VPS-Backups/apex-speed-labs-vps-config'
mkdir -p $DISK_PATH

# 备份.env
cp /root/apex-automation/.env $DISK_PATH/.env.backup
tar -czf $DISK_PATH/env_backup_$(date +%Y%m%d_%H%M).tar.gz -C /root/apex-automation .env

echo '✅ .env 已备份到外接硬盘'
ls -la $DISK_PATH
