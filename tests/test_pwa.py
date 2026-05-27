import pytest
import json
from pathlib import Path


def test_manifest_exists():
    p = Path("web/static/manifest.json")
    assert p.exists()
    data = json.loads(p.read_text())
    assert data["name"] == "Pixelle-Video"
    assert "icons" in data


def test_sw_exists():
    p = Path("web/static/sw.js")
    assert p.exists()
    content = p.read_text()
    assert "serviceworker" in content.lower() or "fetch" in content


def test_icons_exist():
    assert Path("web/static/icon-192.png").exists()
    assert Path("web/static/icon-512.png").exists()
