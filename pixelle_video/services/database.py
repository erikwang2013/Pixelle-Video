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

"""SQLite database for task storage and migration from JSON"""

import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional

from loguru import logger


class DatabaseService:
    """SQLite-backed task storage with JSON migration support.

    Provides CRUD operations for video generation tasks together with
    aggregate statistics and a migration path from legacy JSON task files.
    """

    def __init__(self, db_path: str = "data/pixelle.db"):
        """Initialize database, creating the file and tables if needed.

        Args:
            db_path: Path to the SQLite database file.
        """
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._db_path = db_path
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        """Return a new connection with row_factory set to sqlite3.Row."""
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        """Create tables and indexes if they do not already exist."""
        with self._get_conn() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    title TEXT DEFAULT '',
                    status TEXT DEFAULT 'pending',
                    pipeline TEXT DEFAULT 'standard',
                    mode TEXT DEFAULT 'generate',
                    n_scenes INTEGER DEFAULT 5,
                    duration REAL DEFAULT 0,
                    file_size INTEGER DEFAULT 0,
                    video_path TEXT DEFAULT '',
                    error_message TEXT DEFAULT '',
                    created_at TEXT DEFAULT '',
                    completed_at TEXT DEFAULT '',
                    params TEXT DEFAULT '{}'
                );
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    username TEXT UNIQUE,
                    role TEXT DEFAULT 'user',
                    created_at TEXT DEFAULT ''
                );
                CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
                CREATE INDEX IF NOT EXISTS idx_tasks_created ON tasks(created_at);
                CREATE INDEX IF NOT EXISTS idx_tasks_pipeline ON tasks(pipeline);
            """
            )

    def insert_task(self, task: Dict) -> bool:
        """Insert or replace a task record.

        Args:
            task: Dictionary of task fields.

        Returns:
            True on success, False on failure.
        """
        try:
            with self._get_conn() as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO tasks
                    (task_id, title, status, pipeline, mode, n_scenes, duration,
                     file_size, video_path, created_at, completed_at, params)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        task.get("task_id", ""),
                        task.get("title", ""),
                        task.get("status", "pending"),
                        task.get("pipeline", "standard"),
                        task.get("mode", "generate"),
                        task.get("n_scenes", 5),
                        task.get("duration", 0),
                        task.get("file_size", 0),
                        task.get("video_path", ""),
                        task.get("created_at", ""),
                        task.get("completed_at", ""),
                        json.dumps(task.get("params", {})),
                    ),
                )
            return True
        except Exception as e:
            logger.error(f"DB insert error: {e}")
            return False

    def get_tasks(self, status: str = None, limit: int = 100) -> List[Dict]:
        """Retrieve tasks, optionally filtered by status.

        Args:
            status: Optional status filter (e.g., 'completed', 'failed').
            limit: Maximum number of tasks to return.

        Returns:
            List of task dictionaries ordered by created_at descending.
        """
        with self._get_conn() as conn:
            if status:
                rows = conn.execute(
                    "SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC LIMIT ?",
                    (status, limit),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM tasks ORDER BY created_at DESC LIMIT ?",
                    (limit,),
                ).fetchall()
            return [dict(r) for r in rows]

    def get_task(self, task_id: str) -> Optional[Dict]:
        """Retrieve a single task by its id.

        Args:
            task_id: The unique task identifier.

        Returns:
            Task dictionary or None if not found.
        """
        with self._get_conn() as conn:
            row = conn.execute(
                "SELECT * FROM tasks WHERE task_id = ?", (task_id,)
            ).fetchone()
            return dict(row) if row else None

    def update_task_status(self, task_id: str, status: str, **kwargs) -> None:
        """Update the status and optional extra fields of a task.

        Args:
            task_id: The task to update.
            status: New status value.
            **kwargs: Additional column=value pairs to set.
        """
        fields = ", ".join(f"{k} = ?" for k in kwargs.keys())
        values = list(kwargs.values()) + [task_id]
        with self._get_conn() as conn:
            conn.execute(
                f"UPDATE tasks SET status = ?, {fields} WHERE task_id = ?",
                [status] + values,
            )

    def delete_task(self, task_id: str) -> bool:
        """Delete a task by its id.

        Args:
            task_id: The task to delete.

        Returns:
            Always True (idempotent delete).
        """
        with self._get_conn() as conn:
            conn.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
            return True

    def get_stats(self) -> Dict:
        """Return aggregate statistics across all tasks.

        Returns:
            Dict with total_tasks, completed, failed, success_rate,
            and total_duration_seconds.
        """
        with self._get_conn() as conn:
            total = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
            completed = conn.execute(
                "SELECT COUNT(*) FROM tasks WHERE status='completed'"
            ).fetchone()[0]
            failed = conn.execute(
                "SELECT COUNT(*) FROM tasks WHERE status='failed'"
            ).fetchone()[0]
            total_dur = conn.execute(
                "SELECT COALESCE(SUM(duration), 0) FROM tasks WHERE status='completed'"
            ).fetchone()[0]
            return {
                "total_tasks": total,
                "completed": completed,
                "failed": failed,
                "success_rate": round(completed / total * 100, 1) if total else 0,
                "total_duration_seconds": total_dur,
            }

    def migrate_from_json(self, json_dir: str = "data") -> int:
        """Migrate existing JSON task files into the SQLite database.

        Reads every tasks_*.json file in *json_dir*, inserting each
        task record found.

        Args:
            json_dir: Directory containing legacy JSON task files.

        Returns:
            Number of tasks successfully migrated.
        """
        json_dir = Path(json_dir)
        migrated = 0
        for f in json_dir.glob("tasks_*.json"):
            try:
                tasks = json.loads(f.read_text())
                if isinstance(tasks, list):
                    for t in tasks:
                        if self.insert_task(t):
                            migrated += 1
                elif isinstance(tasks, dict):
                    if self.insert_task(tasks):
                        migrated += 1
            except Exception as e:
                logger.warning(f"Migration skip {f}: {e}")
        return migrated
