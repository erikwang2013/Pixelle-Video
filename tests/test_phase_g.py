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

"""Tests for Phase G: SEO, Database, and Health Check features."""


# ---------------------------------------------------------------------------
# G3: SEO Metadata Generator
# ---------------------------------------------------------------------------

def test_seo_metadata():
    from pixelle_video.services.seo import SEOService

    svc = SEOService()
    meta = svc.generate_metadata("如何使用Python自动化视频制作", "本教程将介绍Python自动化...")
    assert meta["title"] == "如何使用Python自动化视频制作"
    assert "教程" in meta["tags"]


def test_seo_social_post():
    from pixelle_video.services.seo import SEOService

    svc = SEOService()
    post = svc.generate_social_post("AI视频制作", platform="weibo")
    assert "AI视频制作" in post


def test_seo_long_title_truncation():
    from pixelle_video.services.seo import SEOService

    svc = SEOService()
    long_topic = "这是一个非常非常长的标题" * 5
    meta = svc.generate_metadata(long_topic)
    assert len(meta["title"]) <= svc.MAX_TITLE_LENGTH


def test_seo_default_description():
    from pixelle_video.services.seo import SEOService

    svc = SEOService()
    meta = svc.generate_metadata("Test Topic")
    assert "AI-generated video about Test Topic" in meta["description"]


def test_seo_max_tags():
    from pixelle_video.services.seo import SEOService

    svc = SEOService()
    meta = svc.generate_metadata("tutorial how to guide review news recipe travel fitness finance ai")
    assert len(meta["tags"]) <= svc.MAX_TAGS


# ---------------------------------------------------------------------------
# G4: Database Migration (JSON to SQLite)
# ---------------------------------------------------------------------------

def test_database_init():
    import tempfile
    from pixelle_video.services.database import DatabaseService

    d = tempfile.mkdtemp()
    db = DatabaseService(db_path=f"{d}/test.db")
    assert db.get_stats()["total_tasks"] == 0


def test_database_insert_and_query():
    import tempfile
    from pixelle_video.services.database import DatabaseService

    d = tempfile.mkdtemp()
    db = DatabaseService(db_path=f"{d}/test.db")
    db.insert_task({
        "task_id": "t1",
        "title": "Test",
        "status": "completed",
        "duration": 120,
    })
    task = db.get_task("t1")
    assert task["title"] == "Test"
    assert db.get_stats()["completed"] == 1


def test_database_migration():
    import json
    import tempfile
    from pathlib import Path
    from pixelle_video.services.database import DatabaseService

    d = tempfile.mkdtemp()
    tasks = [{"task_id": "old1", "title": "Old Task", "status": "completed"}]
    Path(f"{d}/tasks_old.json").write_text(json.dumps(tasks))
    db = DatabaseService(db_path=f"{d}/test.db")
    count = db.migrate_from_json(d)
    assert count == 1


def test_database_update_status():
    import tempfile
    from pixelle_video.services.database import DatabaseService

    d = tempfile.mkdtemp()
    db = DatabaseService(db_path=f"{d}/test.db")
    db.insert_task({"task_id": "t2", "title": "Update Me", "status": "pending"})
    db.update_task_status("t2", "completed", duration=300, completed_at="2025-01-01T00:00:00")
    task = db.get_task("t2")
    assert task["status"] == "completed"
    assert task["duration"] == 300


def test_database_delete_task():
    import tempfile
    from pixelle_video.services.database import DatabaseService

    d = tempfile.mkdtemp()
    db = DatabaseService(db_path=f"{d}/test.db")
    db.insert_task({"task_id": "t3", "title": "Delete Me"})
    assert db.get_task("t3") is not None
    db.delete_task("t3")
    assert db.get_task("t3") is None


def test_database_get_tasks_filtered():
    import tempfile
    from pixelle_video.services.database import DatabaseService

    d = tempfile.mkdtemp()
    db = DatabaseService(db_path=f"{d}/test.db")
    db.insert_task({"task_id": "a", "status": "completed"})
    db.insert_task({"task_id": "b", "status": "pending"})
    db.insert_task({"task_id": "c", "status": "completed"})
    completed = db.get_tasks(status="completed")
    assert len(completed) == 2
