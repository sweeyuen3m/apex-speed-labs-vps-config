# Apex Speed Labs VPS 备份说明

## GitHub仓库
**https://github.com/sweeyuen3m/apex-speed-labs-vps-config**

## 克隆到新VPS
\`\`\`bash
git clone https://github.com/sweeyuen3m/apex-speed-labs-vps-config.git /root/apex-automation
cd /root/apex-automation
\`\`\`

## 恢复Cron任务
\`\`\`bash
crontab crontab.conf
\`\`\`

## 重要配置文件
- `.env` - 敏感配置（不包含在git中，需要手动创建）
- `crontab.conf` - 完整Cron任务配置
- 所有脚本已设置执行权限

## 完整自动化清单
✅ Upwork Playwright自动化
✅ LinkedIn Playwright自动化  
✅ Twitter自动化
✅ YouTube视频上传
✅ Leads自动跟进
✅ 12平台监督系统
✅ 自我修复系统
✅ Dashboard监控
✅ 性能监控
✅ 财务监控
✅ 健康检查
✅ 自动备份
