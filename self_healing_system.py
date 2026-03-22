#!/usr/bin/env python3
# ============================================
# 云端自我修复系统
# Apex Speed Labs - Full Automation
# ============================================

import os
import json
import logging
import subprocess
import time
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

# 配置
BASE_DIR = Path("/root/apex-automation")
LOGS_DIR = BASE_DIR / "logs"
MONITORING_DIR = BASE_DIR / "monitoring"
BACKUP_DIR = BASE_DIR / "backups"

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOGS_DIR / "self_healing.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SelfHealingSystem:
    """自我修复系统"""
    
    def __init__(self):
        self.issues = []
        self.fixed_issues = []
        
    def check_disk_space(self) -> Tuple[bool, Dict]:
        """检查磁盘空间"""
        result = subprocess.run(
            ["df", "-h", "/"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            if len(lines) > 1:
                parts = lines[1].split()
                usage_percent = parts[4].rstrip('%')
                usage = int(usage_percent)
                
                return (
                    usage < 80,
                    {
                        "usage_percent": usage,
                        "total": parts[1],
                        "used": parts[2],
                        "available": parts[3]
                    }
                )
        
        return False, {}
    
    def heal_disk_space(self) -> bool:
        """修复磁盘空间"""
        logger.info("🔧 尝试修复磁盘空间...")
        
        try:
            # 清理日志文件（保留最近7天）
            logger.info("🗑️ 清理旧日志...")
            for log_file in LOGS_DIR.glob("*.log"):
                if log_file.stat().st_mtime < time.time() - 7 * 86400:
                    log_file.unlink()
                    logger.info(f"✅ 已删除: {log_file.name}")
            
            # 清理临时文件
            logger.info("🗑️ 清理临时文件...")
            subprocess.run(["apt-get", "clean"], capture_output=True)
            subprocess.run(["apt-get", "autoremove", "-y"], capture_output=True)
            
            return True
        except Exception as e:
            logger.error(f"❌ 修复失败: {e}")
            return False
    
    def check_memory(self) -> Tuple[bool, Dict]:
        """检查内存使用"""
        result = subprocess.run(
            ["free", "-m"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            if len(lines) > 1:
                parts = lines[1].split()
                total = int(parts[1])
                used = int(parts[2])
                usage_percent = (used / total) * 100
                
                return (
                    usage_percent < 90,
                    {
                        "total_mb": total,
                        "used_mb": used,
                        "usage_percent": usage_percent
                    }
                )
        
        return False, {}
    
    def heal_memory(self) -> bool:
        """修复内存问题"""
        logger.info("🔧 尝试修复内存问题...")
        
        try:
            # 查找占用内存最多的进程
            result = subprocess.run(
                ["ps", "aux", "--sort=-%mem", "|", "head", "-10"],
                shell=True,
                capture_output=True,
                text=True
            )
            
            logger.info("📊 占用内存最多的进程:")
            logger.info(result.stdout)
            
            # 释放缓存
            subprocess.run(["sync"], capture_output=True)
            subprocess.run(
                ["sh", "-c", "echo 3 > /proc/sys/vm/drop_caches"],
                capture_output=True
            )
            
            logger.info("✅ 缓存已释放")
            return True
        except Exception as e:
            logger.error(f"❌ 修复失败: {e}")
            return False
    
    def check_network(self) -> Tuple[bool, Dict]:
        """检查网络连接"""
        try:
            # 测试外网连接
            response = requests.get("https://www.google.com", timeout=10)
            return response.status_code == 200, {"status": "ok"}
        except Exception as e:
            return False, {"error": str(e)}
    
    def check_processes(self) -> Tuple[bool, Dict]:
        """检查关键进程"""
        critical_processes = ["python3", "cron", "nginx"]
        running_processes = {}
        
        for proc in critical_processes:
            result = subprocess.run(
                ["pgrep", "-x", proc],
                capture_output=True
            )
            running_processes[proc] = result.returncode == 0
        
        all_running = all(running_processes.values())
        return all_running, running_processes
    
    def heal_processes(self) -> bool:
        """修复进程问题"""
        logger.info("🔧 尝试修复进程...")
        
        try:
            # 确保 cron 在运行
            subprocess.run(["service", "cron", "start"], capture_output=True)
            
            logger.info("✅ 进程已修复")
            return True
        except Exception as e:
            logger.error(f"❌ 修复失败: {e}")
            return False
    
    def check_database(self) -> Tuple[bool, Dict]:
        """检查数据库连接"""
        # TODO: 实现数据库检查
        return True, {"status": "not_configured"}
    
    def backup_system(self) -> bool:
        """备份系统"""
        logger.info("💾 开始系统备份...")
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = BACKUP_DIR / f"backup_{timestamp}"
            backup_path.mkdir(parents=True, exist_ok=True)
            
            # 备份配置文件
            subprocess.run(
                f"cp -r {BASE_DIR}/.env {backup_path}/",
                shell=True,
                capture_output=True
            )
            
            # 备份监控数据
            subprocess.run(
                f"cp -r {MONITORING_DIR}/* {backup_path}/monitoring/",
                shell=True,
                capture_output=True
            )
            
            logger.info(f"✅ 备份完成: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"❌ 备份失败: {e}")
            return False
    
    def run_health_check(self) -> Dict:
        """运行健康检查"""
        logger.info("=" * 60)
        logger.info(f"🏥 系统健康检查 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)
        
        issues = []
        
        # 检查磁盘空间
        disk_ok, disk_info = self.check_disk_space()
        if not disk_ok:
            issues.append({
                "type": "disk_space",
                "severity": "high",
                "message": f"磁盘使用率过高: {disk_info['usage_percent']}%",
                "info": disk_info
            })
            logger.warning(f"⚠️ 磁盘空间不足: {disk_info['usage_percent']}%")
        else:
            logger.info(f"✅ 磁盘空间正常: {disk_info['usage_percent']}%")
        
        # 检查内存
        memory_ok, memory_info = self.check_memory()
        if not memory_ok:
            issues.append({
                "type": "memory",
                "severity": "medium",
                "message": f"内存使用率过高: {memory_info['usage_percent']:.1f}%",
                "info": memory_info
            })
            logger.warning(f"⚠️ 内存使用率高: {memory_info['usage_percent']:.1f}%")
        else:
            logger.info(f"✅ 内存正常: {memory_info['usage_percent']:.1f}%")
        
        # 检查网络
        network_ok, network_info = self.check_network()
        if not network_ok:
            issues.append({
                "type": "network",
                "severity": "high",
                "message": "网络连接失败",
                "info": network_info
            })
            logger.error("❌ 网络连接失败")
        else:
            logger.info("✅ 网络连接正常")
        
        # 检查进程
        processes_ok, processes_info = self.check_processes()
        if not processes_ok:
            issues.append({
                "type": "processes",
                "severity": "high",
                "message": "关键进程未运行",
                "info": processes_info
            })
            logger.error(f"❌ 进程状态异常: {processes_info}")
        else:
            logger.info("✅ 所有关键进程运行正常")
        
        # 保存检查结果
        check_result = {
            "timestamp": datetime.now().isoformat(),
            "disk": disk_info,
            "memory": memory_info,
            "network": network_info,
            "processes": processes_info,
            "issues": issues,
            "overall_status": "healthy" if not issues else "unhealthy"
        }
        
        self.issues = issues
        
        logger.info("=" * 60)
        return check_result
    
    def auto_heal(self) -> List[Dict]:
        """自动修复问题"""
        logger.info("=" * 60)
        logger.info("🔧 开始自动修复...")
        logger.info("=" * 60)
        
        fixed = []
        
        for issue in self.issues:
            issue_type = issue["type"]
            severity = issue["severity"]
            
            logger.info(f"修复中: {issue['message']}")
            
            if issue_type == "disk_space":
                success = self.heal_disk_space()
            elif issue_type == "memory":
                success = self.heal_memory()
            elif issue_type == "processes":
                success = self.heal_processes()
            else:
                logger.info(f"⏭️ 跳过: {issue_type} (无自动修复方案)")
                continue
            
            if success:
                fixed.append(issue)
                logger.info(f"✅ 修复成功: {issue['message']}")
            else:
                logger.error(f"❌ 修复失败: {issue['message']}")
        
        self.fixed_issues = fixed
        logger.info("=" * 60)
        
        return fixed
    
    def run_healing_cycle(self):
        """运行修复周期"""
        # 健康检查
        health_result = self.run_health_check()
        
        # 保存结果
        report_file = MONITORING_DIR / f"health_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        with open(report_file, 'w') as f:
            json.dump(health_result, f, indent=2, default=str)
        
        # 如果有问题，自动修复
        if self.issues:
            logger.info(f"发现 {len(self.issues)} 个问题，开始自动修复...")
            fixed = self.auto_heal()
            
            # 记录修复结果
            if fixed:
                logger.info(f"✅ 已修复 {len(fixed)} 个问题")
        
        # 备份系统（每天一次）
        if datetime.now().hour == 8:
            self.backup_system()


if __name__ == "__main__":
    healer = SelfHealingSystem()
    healer.run_healing_cycle()
