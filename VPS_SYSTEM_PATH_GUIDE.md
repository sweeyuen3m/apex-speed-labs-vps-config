# Apex Speed Labs - VPS 系统路径指南

## 更新时间
2026-03-23

---

## 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    MacBook (本地)                        │
│  ~/WorkBuddy/20260322214926/                           │
│  ~/Library/Application Support/WorkBuddy/               │
└─────────────────────────────────────────────────────────┘
                            │
                            │ 同步
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    VPS (云端)                           │
│  167.71.120.132                                        │
└─────────────────────────────────────────────────────────┘
```

---

## VPS 路径 (统一命名)

| 类型 | 路径 | 说明 |
|------|------|------|
| **主目录** | `/root/apex-automation/` | 所有自动化脚本 |
| **GitHub备份** | `/root/apex-automation-git/` | 推送到GitHub的备份 |
| **日志** | `/root/apex-automation/logs/` | 系统运行日志 |
| **外接硬盘** | `/Volumes/Steven/VPS-Backups/apex-speed-labs-vps-config/` | 本地备份 |

---

## GitHub 仓库

**URL**: https://github.com/sweeyuen3m/apex-speed-labs-vps-config

**仓库名**: `apex-speed-labs-vps-config`

**说明**: Apex Speed Labs VPS Full Automation Configuration - 14 Platform Auto System

---

## 备份策略 (安全版)

### ✅ GitHub 备份 (无敏感数据)
- 自动化脚本 (.py)
- Shell脚本 (.sh)
- HTML页面 (.html)
- 配置文件 (.gitignore)
- README文档

### ❌ 永远不备份到 GitHub
- `.env` 文件 (API密钥、密码等)
- 日志文件
- 缓存文件

### ✅ 外接硬盘 备份 (完整数据)
- `.env` 文件
- 所有自动化脚本
- 日志文件
- 系统配置

---

## 关键脚本

| 脚本 | 位置 | 功能 |
|------|------|------|
| `backup_to_github.sh` | /root/apex-automation/ | 备份到GitHub (无.env) |
| `backup_env_to_disk.sh` | /root/apex-automation/ | 备份.env到外接硬盘 |
| `auto-backup.sh` | /root/apex-automation/ | 完整自动备份 |
| `health_check.sh` | /root/apex-automation/ | 系统健康检查 |
| `daily_report_v2.py` | /root/apex-automation/ | 每日汇报 |

---

## Cron 任务配置

### 自动备份 (每日 23:59)
```bash
59 23 * * * /root/apex-automation/auto-backup.sh >> /root/apex-automation/logs/backup.log 2>&1
```

### .env 备份 (每周日 00:00)
```bash
0 0 * * 0 /root/apex-automation/backup_env_to_disk.sh >> /root/apex-automation/logs/env_backup.log 2>&1
```

---

## 恢复流程

### 1. 从 GitHub 恢复 (无.env)
```bash
# 克隆仓库
git clone https://github.com/sweeyuen3m/apex-speed-labs-vps-config.git /root/apex-automation

# 重新配置 .env
# 从外接硬盘复制
cp /Volumes/Steven/VPS-Backups/apex-speed-labs-vps-config/.env /root/apex-automation/

# 重新配置 Cron
crontab /root/apex-automation/crontab.conf
```

### 2. 从外接硬盘恢复 (完整)
```bash
# 恢复所有文件
cp -r /Volumes/Steven/VPS-Backups/apex-speed-labs-vps-config/* /root/apex-automation/

# 重启服务
systemctl restart apex-automation
```

---

## 路径验证命令

```bash
# 检查主目录
ls /root/apex-automation/*.py | wc -l

# 检查GitHub备份
ls /root/apex-automation-git/

# 检查外接硬盘
ls /Volumes/Steven/VPS-Backups/

# 检查日志
tail -20 /root/apex-automation/logs/*.log

# 检查GitHub仓库
cd /root/apex-automation && git remote -v
```

---

## 团队职责

### Elon (技术)
- 维护 VPS 系统
- 确保备份正常运行
- 监控 GitHub 同步

### Steven (CEO)
- 定期检查备份状态
- 从外接硬盘恢复 .env (如需要)
- 批准重大变更

---

## 紧急联系

- **VPS IP**: 167.71.120.132
- **GitHub**: https://github.com/sweeyuen3m/apex-speed-labs-vps-config
- **外接硬盘**: /Volumes/Steven/VPS-Backups/
