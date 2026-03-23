#!/usr/bin/env python3
"""
Telegram 健康检查脚本
每5分钟检查一次，失败自动告警
"""
import os
import requests
from datetime import datetime

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8768921354:AAEvCrvyou9ypeGR9mvfwhnvvF7Erox05pA")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "8125001108")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def check_bot():
    try:
        resp = requests.get(f"{API_URL}/getMe", timeout=5)
        return resp.json().get("ok", False)
    except:
        return False

def send_message(text):
    try:
        resp = requests.post(f"{API_URL}/sendMessage",
            data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=10)
        return resp.json().get("ok", False)
    except:
        return False

if __name__ == "__main__":
    if check_bot():
        msg = f"✅ TG健康检查 {datetime.now().strftime('%H:%M:%S')} - FULL AUTO ACTIVE"
        send_message(msg)
        print(f"[OK] {msg}")
    else:
        print("[FAIL] Telegram Bot不可用")
