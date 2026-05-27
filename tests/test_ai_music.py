import pytest
import tempfile, os
from pathlib import Path

def test_list_styles():
    from pixelle_video.services.ai_music import AIMusicService
    d = tempfile.mkdtemp()
    svc = AIMusicService(data_dir=d)
    styles = svc.list_styles()
    assert "cinematic" in styles
    assert "lofi" in styles
    assert len(styles) >= 8

def test_recommend_style():
    from pixelle_video.services.ai_music import AIMusicService
    d = tempfile.mkdtemp()
    svc = AIMusicService(data_dir=d)
    assert svc.recommend_style("科技数码产品评测") == "electronic"
    assert svc.recommend_style("咖啡店探店日记") == "jazz"
    assert svc.recommend_style("冥想放松指南") == "ambient"
    assert svc.recommend_style("random topic") == "lofi"  # default

def test_generate_creates_metadata():
    from pixelle_video.services.ai_music import AIMusicService
    import asyncio
    d = tempfile.mkdtemp()
    svc = AIMusicService(data_dir=d)
    result = asyncio.run(svc.generate(style="cinematic", duration=30, title="Test"))
    assert result["style"] == "cinematic"
    assert result["duration"] == 30
    assert result["track_id"]
    assert Path(result["output_path"].replace(".mp3", ".json")).exists()

def test_generate_unknown_style_falls_back():
    from pixelle_video.services.ai_music import AIMusicService
    import asyncio
    d = tempfile.mkdtemp()
    svc = AIMusicService(data_dir=d)
    result = asyncio.run(svc.generate(style="nonexistent"))
    assert result["style"] == "lofi"

def test_history_and_delete():
    from pixelle_video.services.ai_music import AIMusicService
    import asyncio
    d = tempfile.mkdtemp()
    svc = AIMusicService(data_dir=d)
    result = asyncio.run(svc.generate(style="jazz", duration=60))
    history = svc.get_history()
    assert len(history) >= 1
    assert svc.delete_track(result["track_id"]) is True
