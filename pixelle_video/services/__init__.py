# Copyright (c) 2026 erik <erik@erik.xyz> — https://erik.xyz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Pixelle-Video Services

Core services providing atomic capabilities.

Services:
- LLMService: LLM text generation
- TTSService: Text-to-speech
- MediaService: Media generation (image & video)
- VideoService: Video processing
- FrameProcessor: Frame processing orchestrator
- SubtitleService: SRT subtitle generation and timing
- TransitionService: Video transition effects between concatenated segments
- PersistenceService: Task metadata and storyboard persistence
- HistoryManager: History management business logic
- ComfyBaseService: Base class for ComfyUI-based services
- AnalyticsService: Usage analytics and summary statistics
- URLFetcher: URL content extraction and summarization
- VideoEditorService: trim, reorder, and replace frame operations
- TaskScheduler: Cron-based task scheduling for automated video generation
- SocialPublisher: Social media video publishing (YouTube, Bilibili, TikTok)
- UserManager: User authentication and API key management
- WebhookService: Webhook registration and dispatch service
- WorkspaceService: Team workspaces with shared resources and invite codes
- PaymentService: Stripe payment integration with plan management
- EmbedService: Video embed code and share link generation
- CloudStorageService: Cloud storage integration (S3, OSS, COS, local)
- RateLimiter: API rate limiting with token bucket algorithm
- AnalyticsExportService: Export analytics data as CSV or HTML report
- QualityPresetService: Video quality presets for different output needs
- ThumbnailService: AI thumbnail generation with frame extraction and text overlay
- WatermarkService: Text and image watermark overlay on videos
- ScriptTemplateService: Script template library for different video genres
- TTSEmotionService: TTS emotion profiles for voice styling
- BatchCSVService: Batch CSV import for video generation
- EmailNotifyService: Email notification service with SMTP and enable/disable toggle
- SEOService: AI-powered SEO metadata generation for videos
- EmbedService: Video embed code and share link generation
- CloudStorageService: Cloud storage integration (S3, OSS, COS, local)
- RateLimiter: API rate limiting with token bucket algorithm
- AnalyticsExportService: Export analytics data as CSV or HTML report
- QualityPresetService: Video quality presets for different output needs
- ThumbnailService: AI thumbnail generation with frame extraction and text overlay
- WatermarkService: Text and image watermark overlay on videos
- ScriptTemplateService: Script template library for different video genres
- TTSEmotionService: TTS emotion profiles for voice styling
- BatchCSVService: Batch CSV import for video generation
- EmailNotifyService: Email notification service with SMTP and enable/disable toggle
- SEOService: AI-powered SEO metadata generation for videos
- DatabaseService: SQLite database for task storage and migration from JSON
- JianYingExportService: Export storyboard to JianYing (剪映) draft format
- ABTestingService: A/B testing — generate multiple video versions for comparison
"""

from pixelle_video.services.comfy_base_service import ComfyBaseService
from pixelle_video.services.llm_service import LLMService
from pixelle_video.services.tts_service import TTSService
from pixelle_video.services.media import MediaService
from pixelle_video.services.video import VideoService
from pixelle_video.services.frame_processor import FrameProcessor
from pixelle_video.services.persistence import PersistenceService
from pixelle_video.services.history_manager import HistoryManager
from pixelle_video.services.subtitle import SubtitleService
from pixelle_video.services.transition import TransitionService
from pixelle_video.services.analytics import AnalyticsService
from pixelle_video.services.url_fetcher import URLFetcher
from pixelle_video.services.video_editor import VideoEditorService
from pixelle_video.services.scheduler import TaskScheduler
from pixelle_video.services.social_publisher import SocialPublisher
from pixelle_video.services.auth import UserManager
from pixelle_video.services.webhook import WebhookService
from pixelle_video.services.workspace import WorkspaceService
from pixelle_video.services.payment import PaymentService
from pixelle_video.services.embed import EmbedService
from pixelle_video.services.cloud_storage import CloudStorageService
from pixelle_video.services.rate_limiter import RateLimiter
from pixelle_video.services.analytics_export import AnalyticsExportService
from pixelle_video.services.quality_presets import QualityPresetService
from pixelle_video.services.thumbnail import ThumbnailService
from pixelle_video.services.watermark import WatermarkService
from pixelle_video.services.script_templates import ScriptTemplateService
from pixelle_video.services.tts_emotion import TTSEmotionService
from pixelle_video.services.batch_csv import BatchCSVService
from pixelle_video.services.email_notify import EmailNotifyService
from pixelle_video.services.seo import SEOService
from pixelle_video.services.database import DatabaseService
from pixelle_video.services.jianying_export import JianYingExportService
from pixelle_video.services.ab_testing import ABTestingService
from pixelle_video.services.ai_music import AIMusicService

# Backward compatibility alias
ImageService = MediaService

__all__ = [
    "ComfyBaseService",
    "LLMService",
    "TTSService",
    "MediaService",
    "ImageService",  # Backward compatibility
    "VideoService",
    "FrameProcessor",
    "PersistenceService",
    "HistoryManager",
    "SubtitleService",
    "TransitionService",
    "AnalyticsService",
    "URLFetcher",
    "VideoEditorService",
    "TaskScheduler",
    "SocialPublisher",
    "UserManager",
    "WebhookService",
    "WorkspaceService",
    "PaymentService",
    "EmbedService",
    "CloudStorageService",
    "RateLimiter",
    "AnalyticsExportService",
    "QualityPresetService",
    "ThumbnailService",
    "WatermarkService",
    "ScriptTemplateService",
    "TTSEmotionService",
    "BatchCSVService",
    "EmailNotifyService",
    "SEOService",
    "DatabaseService",
    "JianYingExportService",
    "ABTestingService",
    "AIMusicService",
]
