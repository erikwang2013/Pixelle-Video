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

"""Tests for the A/B testing service."""

import os
import tempfile
from pathlib import Path

import pytest


def test_list_dimensions():
    from pixelle_video.services.ab_testing import ABTestingService
    d = tempfile.mkdtemp()
    svc = ABTestingService(data_dir=d)
    dims = svc.list_dimensions()
    assert "style" in dims
    assert "voice" in dims
    assert "transition" in dims


def test_get_variants():
    from pixelle_video.services.ab_testing import ABTestingService
    d = tempfile.mkdtemp()
    svc = ABTestingService(data_dir=d)
    variants = svc.get_variants("style")
    assert len(variants) == 4
    assert variants[0]["name_zh"] == "现代简约"


def test_create_test():
    from pixelle_video.services.ab_testing import ABTestingService
    d = tempfile.mkdtemp()
    svc = ABTestingService(data_dir=d)
    test = svc.create_test("如何提高工作效率", ["style", "subtitles"])
    assert test["topic"] == "如何提高工作效率"
    # 4 styles + 2 subtitle variants = 6 total
    assert len(test["variants"]) == 6  # 4 style + 2 subtitle


def test_update_and_report():
    from pixelle_video.services.ab_testing import ABTestingService
    d = tempfile.mkdtemp()
    svc = ABTestingService(data_dir=d)
    test = svc.create_test("Test Topic", ["voice"])
    vid = test["variants"][0]["variant_id"]
    svc.update_variant_status(test["test_id"], vid, "completed", "task_001", {"duration": 45.5})
    report = svc.get_comparison_report(test["test_id"])
    assert report["completed"] == 1


def test_list_tests():
    from pixelle_video.services.ab_testing import ABTestingService
    d = tempfile.mkdtemp()
    svc = ABTestingService(data_dir=d)
    svc.create_test("Topic A", ["style"])
    svc.create_test("Topic B", ["voice"])
    tests = svc.list_tests()
    assert len(tests) == 2
