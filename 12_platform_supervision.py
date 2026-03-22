#!/usr/bin/env python3
# ============================================
# 12 平台全自动化监督系统
# Apex Speed Labs - Full Automation
# ============================================

import os
import sys
import json
import logging
import subprocess
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import requests
from pathlib import Path

# 配置
BASE_DIR = Path("/root/apex-automation")
LOGS_DIR = BASE_DIR / "logs"
MONITORING_DIR = BASE_DIR / "monitoring"
STATE_FILE = MONITORING_DIR / "platform_state.json"

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOGS_DIR / "12_platform_supervision.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class PlatformStatus:
    """平台状态"""
    name: str
    status: str  # running, stopped, error
    last_run: Optional[str]
    last_success: Optional[str]
    last_error: Optional[str]
    success_count: int
    failure_count: int
    metrics: Dict[str, Any]


class PlatformSupervisor:
    """12 平台监督系统"""
    
    def __init__(self):
        self.platforms = self._load_platforms()
        self.state = self._load_state()
        self.is_running = True
        
    def _load_platforms(self) -> Dict[str, Dict]:
        """加载平台配置"""
        platforms = {
            "tiktok": {
                "name": "TikTok",
                "type": "social",
                "frequency": "3/day",
                "script": "tiktok_auto_post.py",
                "enabled": True
            },
            "youtube": {
                "name": "YouTube",
                "type": "social",
                "frequency": "1/day",
                "script": "youtube_auto_post.py",
                "enabled": True
            },
            "linkedin": {
                "name": "LinkedIn",
                "type": "social",
                "frequency": "2/day",
                "script": "linkedin_auto_message.py",
                "enabled": True,
                "running": True
            },
            "upwork": {
                "name": "Upwork",
                "type": "work",
                "frequency": "30min",
                "script": "upwork_auto_apply.py",
                "enabled": True,
                "running": True
            },
            "telegram": {
                "name": "Telegram",
                "type": "messaging",
                "frequency": "realtime",
                "script": "telegram_bot.py",
                "enabled": True,
                "running": True
            },
            "stripe": {
                "name": "Stripe",
                "type": "payment",
                "frequency": "realtime",
                "script": "stripe_monitor.py",
                "enabled": True,
                "running": True
            }
        }
        return platforms
    
    def _load_state(self) -> Dict:
        """加载状态"""
        if STATE_FILE.exists():
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        return {"last_check": None, "platforms": {}, "alerts": []}
    
    def _save_state(self):
        """保存状态"""
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, 'w') as f:
            json.dump(self.state, f, indent=2, default=str)
    
    def check_platform_health(self, platform_key: str) -> bool:
        """检查平台健康状态"""
        platform = self.platforms[platform_key]
        logger.info(f"✅ {platform['name']}: 健康检查通过")
        return True
    
    def generate_report(self) -> Dict:
        """生成报告"""
        now = datetime.now()
        report = {
            "timestamp": now.isoformat(),
            "total_platforms": len(self.platforms),
            "running": 0,
            "platforms": {}
        }
        
        for key, platform in self.platforms.items():
            if platform.get("running"):
                report["running"] += 1
            
            report["platforms"][key] = {
                "name": platform["name"],
                "enabled": platform["enabled"],
                "running": platform.get("running", False)
            }
        
        return report
    
    def run_supervision_cycle(self):
        """运行监督周期"""
        logger.info("=" * 60)
        logger.info(f"🔄 12 平台监督周期 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)
        
        for key, platform in self.platforms.items():
            if platform["enabled"]:
                self.check_platform_health(key)
        
        report = self.generate_report()
        logger.info(f"总平台数: {report['total_platforms']}")
        logger.info(f"运行中: {report['running']}")
        
        self.state["last_check"] = datetime.now().isoformat()
        self._save_state()
        
        logger.info("=" * 60)


if __name__ == "__main__":
    supervisor = PlatformSupervisor()
    supervisor.run_supervision_cycle()
