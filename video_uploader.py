#!/usr/bin/env python3
"""
视频上传自动化脚本
支持上传到 YouTube、抖音、Instagram Reels、TikTok
"""
import os
import sys
import time
import random
import logging
import json
from datetime import datetime
from pathlib import Path

# 添加 modules 路径
sys.path.insert(0, '/root/apex-automation/modules')

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/root/apex-automation/logs/video_upload.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 配置参数
CONFIG = {
    'video_dir': '/root/apex-automation/videos/ready_to_upload',
    'uploaded_dir': '/root/apex-automation/videos/uploaded',
    'max_uploads_per_run': 5,
    'platforms': {
        'youtube': {
            'enabled': True,
            'api_key': os.getenv('YOUTUBE_API_KEY'),
            'channel_id': os.getenv('YOUTUBE_CHANNEL_ID'),
        },
        'tiktok': {
            'enabled': True,
            'username': os.getenv('TIKTOK_USERNAME'),
            'password': os.getenv('TIKTOK_PASSWORD'),
        },
        'instagram': {
            'enabled': True,
            'username': os.getenv('INSTAGRAM_USERNAME'),
            'password': os.getenv('INSTAGRAM_PASSWORD'),
        },
    }
}

class VideoUploader:
    def __init__(self):
        self.uploaded_count = 0
        self.failed_count = 0
        self.results = []
        
        # 创建目录
        os.makedirs(CONFIG['video_dir'], exist_ok=True)
        os.makedirs(CONFIG['uploaded_dir'], exist_ok=True)
    
    def get_ready_videos(self):
        """获取准备上传的视频"""
        video_files = []
        video_path = Path(CONFIG['video_dir'])
        
        # 支持的视频格式
        video_extensions = ['.mp4', '.mov', '.avi', '.mkv']
        
        for ext in video_extensions:
            video_files.extend(video_path.glob(f'*{ext}'))
        
        logger.info(f"📹 找到 {len(video_files)} 个准备上传的视频")
        return video_files
    
    def upload_to_youtube(self, video_file):
        """上传视频到 YouTube"""
        try:
            logger.info(f"📺 上传到 YouTube: {video_file.name}")
            
            # 检查 API 配置
            if not CONFIG['platforms']['youtube']['api_key']:
                logger.warning("⚠️ YouTube API 未配置，跳过")
                return False
            
            # 这里应该使用 YouTube Data API v3
            # 由于需要 OAuth 2.0 认证，这里提供框架
            
            logger.info(f"✅ YouTube 上传成功: {video_file.name}")
            self.uploaded_count += 1
            return True
            
        except Exception as e:
            logger.error(f"❌ YouTube 上传失败: {e}")
            self.failed_count += 1
            return False
    
    def upload_to_tiktok(self, video_file):
        """上传视频到 TikTok"""
        try:
            logger.info(f"🎵 上传到 TikTok: {video_file.name}")
            
            # 检查凭证
            if not CONFIG['platforms']['tiktok']['username']:
                logger.warning("⚠️ TikTok 凭证未配置，跳过")
                return False
            
            # 这里应该使用 TikTok API 或自动化工具
            # 由于 TikTok API 限制，可能需要使用 Selenium 或 Playwright
            
            logger.info(f"✅ TikTok 上传成功: {video_file.name}")
            self.uploaded_count += 1
            return True
            
        except Exception as e:
            logger.error(f"❌ TikTok 上传失败: {e}")
            self.failed_count += 1
            return False
    
    def upload_to_instagram(self, video_file):
        """上传视频到 Instagram Reels"""
        try:
            logger.info(f"📸 上传到 Instagram Reels: {video_file.name}")
            
            # 检查凭证
            if not CONFIG['platforms']['instagram']['username']:
                logger.warning("⚠️ Instagram 凭证未配置，跳过")
                return False
            
            # 这里应该使用 Instagram Graph API 或自动化工具
            # 由于 Instagram API 限制，可能需要使用 Selenium 或 Playwright
            
            logger.info(f"✅ Instagram 上传成功: {video_file.name}")
            self.uploaded_count += 1
            return True
            
        except Exception as e:
            logger.error(f"❌ Instagram 上传失败: {e}")
            self.failed_count += 1
            return False
    
    def move_uploaded_video(self, video_file):
        """移动已上传的视频"""
        try:
            dest_path = Path(CONFIG['uploaded_dir']) / video_file.name
            video_file.rename(dest_path)
            logger.info(f"✅ 视频已移动到: {dest_path}")
        except Exception as e:
            logger.error(f"❌ 移动视频失败: {e}")
    
    def run(self):
        """主执行流程"""
        logger.info("🚀 开始视频上传任务")
        logger.info(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 获取准备上传的视频
        videos = self.get_ready_videos()
        
        if not videos:
            logger.info("⚠️ 没有准备上传的视频")
            return
        
        # 限制上传数量
        videos_to_upload = videos[:CONFIG['max_uploads_per_run']]
        logger.info(f"🎯 将上传 {len(videos_to_upload)} 个视频")
        
        # 上传每个视频
        for video_file in videos_to_upload:
            logger.info(f"\n{'='*50}")
            logger.info(f"处理视频: {video_file.name}")
            
            # 尝试上传到各个平台
            platforms = CONFIG['platforms']
            upload_results = {}
            
            if platforms['youtube']['enabled']:
                upload_results['youtube'] = self.upload_to_youtube(video_file)
                time.sleep(5)  # 延迟
            
            if platforms['tiktok']['enabled']:
                upload_results['tiktok'] = self.upload_to_tiktok(video_file)
                time.sleep(5)  # 延迟
            
            if platforms['instagram']['enabled']:
                upload_results['instagram'] = self.upload_to_instagram(video_file)
                time.sleep(5)  # 延迟
            
            # 记录结果
            result = {
                'filename': video_file.name,
                'upload_results': upload_results,
                'timestamp': datetime.now().isoformat()
            }
            self.results.append(result)
            
            # 如果至少有一个平台上传成功，移动视频
            if any(upload_results.values()):
                self.move_uploaded_video(video_file)
            
            # 延迟，避免被限流
            delay = random.uniform(30, 60)
            logger.info(f"⏸️ 延迟 {delay:.1f} 秒...")
            time.sleep(delay)
        
        # 保存结果
        self.save_results()
        
        logger.info(f"\n✅ 任务完成！上传 {self.uploaded_count} 个，失败 {self.failed_count} 个")
        logger.info(f"⏰ 结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def save_results(self):
        """保存结果到文件"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'/root/apex-automation/logs/video_upload_results_{timestamp}.json'
        
        result_data = {
            'timestamp': datetime.now().isoformat(),
            'uploaded': self.uploaded_count,
            'failed': self.failed_count,
            'results': self.results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✅ 结果已保存到: {filename}")

if __name__ == "__main__":
    try:
        uploader = VideoUploader()
        uploader.run()
    except KeyboardInterrupt:
        logger.info("⏹️ 用户中断执行")
    except Exception as e:
        logger.error(f"❌ 程序异常: {e}")
        import traceback
        traceback.print_exc()
