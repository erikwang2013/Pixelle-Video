# Copyright (C) 2025 AIDC-AI
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
]

