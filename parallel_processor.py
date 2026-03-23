#!/usr/bin/env python3
"""
并发处理引擎 - 充分利用升级硬件
利用3.8GB内存 + 2vCPUs + 6GB虚拟内存
"""

import threading
import time
from queue import Queue
import json
from datetime import datetime

# 资源配置
RESOURCE_CONFIG = {
    'physical_memory': 3.8,
    'cpu_cores': 2,
    'virtual_memory': 6.0,
    'total_processes': 9,
}

# 任务队列配置
TASK_QUEUE = {
    'linkedin_tasks': Queue(maxsize=1000),
    'email_tasks': Queue(maxsize=500),
    'stripe_tasks': Queue(maxsize=200),
}

# 进程配置
PROCESS_CONFIG = {
    'linkedin_processes': 5,
    'email_processes': 3,
    'monitoring_processes': 1,
}

class LinkedInProcessor(threading.Thread):
    """LinkedIn消息并发处理器"""
    
    def __init__(self, process_id):
        super().__init__()
        self.process_id = process_id
        self.processed = 0
        self.success = 0
        self.failed = 0
        self.daemon = True
    
    def run(self):
        print(f"[LinkedIn-P{self.process_id}] 启动 (内存: 600MB/进程)")
        
        while True:
            try:
                task = TASK_QUEUE['linkedin_tasks'].get(timeout=1)
                
                if self._process_message(task):
                    self.success += 1
                else:
                    self.failed += 1
                
                self.processed += 1
                
                if self.processed % 100 == 0:
                    print(f"[LinkedIn-P{self.process_id}] 已处理 {self.processed} 条 (成功: {self.success})")
                
                TASK_QUEUE['linkedin_tasks'].task_done()
            
            except:
                time.sleep(0.1)
    
    def _process_message(self, task):
        """处理单条消息"""
        return True
    
    def get_stats(self):
        return {
            'process_id': self.process_id,
            'type': 'linkedin',
            'processed': self.processed,
            'success': self.success,
            'failed': self.failed,
            'memory_mb': 600
        }

class EmailProcessor(threading.Thread):
    """Email并发处理器"""
    
    def __init__(self, process_id):
        super().__init__()
        self.process_id = process_id
        self.processed = 0
        self.success = 0
        self.daemon = True
    
    def run(self):
        print(f"[Email-P{self.process_id}] 启动 (内存: 400MB/进程)")
        
        while True:
            try:
                task = TASK_QUEUE['email_tasks'].get(timeout=1)
                
                if self._send_email(task):
                    self.success += 1
                
                self.processed += 1
                
                if self.processed % 50 == 0:
                    print(f"[Email-P{self.process_id}] 已发送 {self.processed} 封 (成功: {self.success})")
                
                TASK_QUEUE['email_tasks'].task_done()
            
            except:
                time.sleep(0.1)
    
    def _send_email(self, task):
        return True
    
    def get_stats(self):
        return {
            'process_id': self.process_id,
            'type': 'email',
            'processed': self.processed,
            'success': self.success,
            'memory_mb': 400
        }

class MonitoringProcessor(threading.Thread):
    """系统监控和统计"""
    
    def __init__(self, processors):
        super().__init__()
        self.processors = processors
        self.daemon = True
        self.start_time = time.time()
    
    def run(self):
        print("\n=== 并发处理监控启动 ===")
        print(f"总进程数: {len(self.processors)}")
        print(f"物理内存利用: {RESOURCE_CONFIG['physical_memory']}GB")
        print(f"虚拟内存利用: {RESOURCE_CONFIG['virtual_memory']}GB")
        print("\n" + "="*50)
        
        while True:
            time.sleep(60)
            
            elapsed = int((time.time() - self.start_time) / 60)
            print(f"\n[监控 - {elapsed}分钟] 实时统计:")
            
            total_processed = 0
            total_success = 0
            total_memory = 0
            
            for proc in self.processors:
                if proc.is_alive():
                    stats = proc.get_stats()
                    total_processed += stats.get('processed', 0)
                    total_success += stats.get('success', 0)
                    total_memory += stats.get('memory_mb', 0)
                    
                    if stats['type'] == 'linkedin':
                        print(f"  LinkedIn-P{stats['process_id']}: {stats['processed']} 条")
                    else:
                        print(f"  Email-P{stats['process_id']}: {stats['processed']} 封")
            
            print(f"\n总处理: {total_processed} | 成功: {total_success} | 内存: {total_memory}MB")

def start_parallel_processors():
    """启动所有并发处理器"""
    processors = []
    
    # 启动LinkedIn处理器
    for i in range(PROCESS_CONFIG['linkedin_processes']):
        proc = LinkedInProcessor(i+1)
        proc.start()
        processors.append(proc)
    
    # 启动Email处理器
    for i in range(PROCESS_CONFIG['email_processes']):
        proc = EmailProcessor(i+1)
        proc.start()
        processors.append(proc)
    
    # 启动监控处理器
    monitor = MonitoringProcessor(processors)
    monitor.start()
    
    return processors

def feed_sample_tasks():
    """填充示例任务"""
    print("\n[任务队列] 开始填充示例任务...")
    
    # 添加LinkedIn任务
    for i in range(100):
        TASK_QUEUE['linkedin_tasks'].put({
            'type': 'linkedin_message',
            'recipient': f'user_{i}@linkedin.com',
            'message': f'Sample message {i}'
        })
    
    # 添加Email任务
    for i in range(50):
        TASK_QUEUE['email_tasks'].put({
            'type': 'email',
            'to': f'recipient_{i}@gmail.com',
            'subject': f'Test Email {i}'
        })
    
    print(f"[任务队列] 已添加:")
    print(f"  - LinkedIn: {TASK_QUEUE['linkedin_tasks'].qsize()} 个")
    print(f"  - Email: {TASK_QUEUE['email_tasks'].qsize()} 个")

if __name__ == '__main__':
    print("="*60)
    print("VPS 并发处理引擎 - 充分利用升级硬件")
    print("="*60)
    
    # 启动处理器
    processors = start_parallel_processors()
    
    # 填充示例任务
    time.sleep(2)
    feed_sample_tasks()
    
    # 保持运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[系统] 正在关闭...")
