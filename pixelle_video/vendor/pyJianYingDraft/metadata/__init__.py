"""记录各种特效/音效/滤镜等的元数据

音频相关元数据更新时间：2024
其余元数据更新时间：2025-08
"""

# 音频特效
from .audio_scene_effect import AudioSceneEffectType
from .effect_meta import AnimationMeta, EffectMeta, EffectParamInstance
from .filter_meta import FilterType

# 其它
from .font_meta import FontType
from .mask_meta import MaskMeta, MaskType
from .speech_to_song import SpeechToSongType

# 文本动画
from .text_intro import TextIntro
from .text_loop import TextLoopAnim
from .text_outro import TextOutro
from .tone_effect import ToneEffectType
from .transition_meta import TransitionType
from .video_character_effect import VideoCharacterEffectType
from .video_group_animation import GroupAnimationType

# 视频动画
from .video_intro import IntroType
from .video_outro import OutroType

# 视频特效
from .video_scene_effect import VideoSceneEffectType

__all__ = [
    "AnimationMeta",
    "EffectMeta",
    "EffectParamInstance",
    "MaskType",
    "MaskMeta",
    "FilterType",
    "FontType",
    "TransitionType",
    "IntroType",
    "OutroType",
    "GroupAnimationType",
    "TextIntro",
    "TextOutro",
    "TextLoopAnim",
    "AudioSceneEffectType",
    "ToneEffectType",
    "SpeechToSongType",
    "VideoSceneEffectType",
    "VideoCharacterEffectType"
]
