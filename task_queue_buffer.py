#!/usr/bin/env python3
"""
任务队列缓冲系统 - 利用6GB虚拟内存
支持2500个任务队列深度，实现24/7自动化发送
"""

import json
import os
from collections import deque
import time
from datetime import datetime

class TaskQueueBuffer:
    """
    分层任务缓冲系统
    - 内存层: 500个任务 (实时处理)
    - 虚拟内存层: 2000个任务 (缓冲层)
    - 总容量: 2500个任务
    """
    
    def __init__(self, base_dir='data/task_buffers'):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)
        
        # 内存队列（实时处理）
        self.memory_queue = {
            'linkedin': deque(maxlen=500),
            'email': deque(maxlen=500),
            'stripe': deque(maxlen=100),
        }
        
        # 虚拟内存队列（磁盘缓冲）
        self.buffer_stats = {
            'linkedin': {'memory': 0, 'disk': 0, 'processed': 0},
            'email': {'memory': 0, 'disk': 0, 'processed': 0},
            'stripe': {'memory': 0, 'disk': 0, 'processed': 0},
        }
        
        self.start_time = time.time()
    
    def enqueue_linkedin(self, message_data):
        """添加LinkedIn任务到内存队列"""
        if len(self.memory_queue['linkedin']) < 500:
            self.memory_queue['linkedin'].append(message_data)
            self.buffer_stats['linkedin']['memory'] += 1
            return 'memory', len(self.memory_queue['linkedin'])
        else:
            # 溢出到虚拟内存/磁盘
            self._save_to_disk('linkedin', message_data)
            self.buffer_stats['linkedin']['disk'] += 1
            return 'disk', self.buffer_stats['linkedin']['disk']
    
    def enqueue_email(self, email_data):
        """添加Email任务到内存队列"""
        if len(self.memory_queue['email']) < 500:
            self.memory_queue['email'].append(email_data)
            self.buffer_stats['email']['memory'] += 1
            return 'memory', len(self.memory_queue['email'])
        else:
            self._save_to_disk('email', email_data)
            self.buffer_stats['email']['disk'] += 1
            return 'disk', self.buffer_stats['email']['disk']
    
    def dequeue_linkedin(self, count=10):
        """从LinkedIn队列获取任务"""
        tasks = []
        for _ in range(min(count, len(self.memory_queue['linkedin']))):
            tasks.append(self.memory_queue['linkedin'].popleft())
        
        # 从磁盘补充
        if len(self.memory_queue['linkedin']) < 100:
            disk_tasks = self._load_from_disk('linkedin', max(100, count))
            tasks.extend(disk_tasks)
            self.buffer_stats['linkedin']['disk'] -= len(disk_tasks)
        
        self.buffer_stats['linkedin']['processed'] += len(tasks)
        return tasks
    
    def dequeue_email(self, count=5):
        """从Email队列获取任务"""
        tasks = []
        for _ in range(min(count, len(self.memory_queue['email']))):
            tasks.append(self.memory_queue['email'].popleft())
        
        # 从磁盘补充
        if len(self.memory_queue['email']) < 50:
            disk_tasks = self._load_from_disk('email', max(50, count))
            tasks.extend(disk_tasks)
            self.buffer_stats['email']['disk'] -= len(disk_tasks)
        
        self.buffer_stats['email']['processed'] += len(tasks)
        return tasks
    
    def _save_to_disk(self, queue_type, data):
        """保存任务到磁盘（虚拟内存）"""
        file_path = os.path.join(self.base_dir, f'{queue_type}_buffer.jsonl')
        with open(file_path, 'a') as f:
            f.write(json.dumps(data) + '\n')
    
    def _load_from_disk(self, queue_type, count):
        """从磁盘加载任务"""
        file_path = os.path.join(self.base_dir, f'{queue_type}_buffer.jsonl')
        if not os.path.exists(file_path):
            return []
        
        tasks = []
        with open(file_path, 'r') as f:
            for line in f:
                if tasks.__len__() >= count:
                    break
                tasks.append(json.loads(line))
        
        # 清理已读的任务
        if tasks:
            with open(file_path, 'w') as f:
                for line in open(file_path):
                    task = json.loads(line)
                    if task not in tasks:
                        f.write(json.dumps(task) + '\n')
        
        return tasks
    
    def get_stats(self):
        """获取队列统计信息"""
        elapsed = int((time.time() - self.start_time) / 60)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'elapsed_minutes': elapsed,
            'linkedin': {
                'memory_queue': len(self.memory_queue['linkedin']),
                'disk_buffer': self.buffer_stats['linkedin']['disk'],
                'total_buffered': len(self.memory_queue['linkedin']) + self.buffer_stats['linkedin']['disk'],
                'processed': self.buffer_stats['linkedin']['processed'],
                'throughput_per_min': self.buffer_stats['linkedin']['processed'] / max(1, elapsed) if elapsed > 0 else 0,
            },
            'email': {
                'memory_queue': len(self.memory_queue['email']),
                'disk_buffer': self.buffer_stats['email']['disk'],
                'total_buffered': len(self.memory_queue['email']) + self.buffer_stats['email']['disk'],
                'processed': self.buffer_stats['email']['processed'],
                'throughput_per_min': self.buffer_stats['email']['processed'] / max(1, elapsed) if elapsed > 0 else 0,
            },
            'capacity_used': {
                'linkedin': (len(self.memory_queue['linkedin']) + self.buffer_stats['linkedin']['disk']) / 2500 * 100,
                'email': (len(self.memory_queue['email']) + self.buffer_stats['email']['disk']) / 1500 * 100,
            }
        }
    
    def print_status(self):
        """打印队列状态"""
        stats = self.get_stats()
        print("\n" + "="*60)
        print("📊 任务队列缓冲系统 - 实时状态")
        print("="*60)
        
        print(f"\n运行时间: {stats['elapsed_minutes']} 分钟")
        
        print(f"\n📧 LinkedIn 队列:")
        print(f"  内存队列: {stats['linkedin']['memory_queue']}/500")
        print(f"  磁盘缓冲: {stats['linkedin']['disk_buffer']}")
        print(f"  总容量使用: {stats['linkedin']['total_buffered']}/2500 ({stats['capacity_used']['linkedin']:.1f}%)")
        print(f"  已处理: {stats['linkedin']['processed']} 条")
        print(f"  吞吐: {stats['linkedin']['throughput_per_min']:.1f} 条/分钟")
        
        print(f"\n✉️  Email 队列:")
        print(f"  内存队列: {stats['email']['memory_queue']}/500")
        print(f"  磁盘缓冲: {stats['email']['disk_buffer']}")
        print(f"  总容量使用: {stats['email']['total_buffered']}/1500 ({stats['capacity_used']['email']:.1f}%)")
        print(f"  已处理: {stats['email']['processed']} 封")
        print(f"  吞吐: {stats['email']['throughput_per_min']:.1f} 封/分钟")
        
        print("\n" + "="*60)

# 示例使用
if __name__ == '__main__':
    print("✅ 任务队列缓冲系统初始化完成")
    print("\n使用示例:")
    print("  queue = TaskQueueBuffer()")
    print("  queue.enqueue_linkedin({'recipient': 'user@linkedin.com', 'message': '...'})")
    print("  queue.enqueue_email({'to': 'user@gmail.com', 'subject': '...'})")
    print("  tasks = queue.dequeue_linkedin(count=10)")
    print("  queue.print_status()")
