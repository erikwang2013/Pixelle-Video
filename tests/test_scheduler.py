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

import pytest

def test_add_schedule():
    from pixelle_video.services.scheduler import TaskScheduler
    svc = TaskScheduler(data_dir="/tmp/pixelle_test_sched")
    s = svc.add_schedule("Test", "0 9 * * *", pipeline="standard")
    assert s["name"] == "Test"
    assert s["cron_expression"] == "0 9 * * *"

def test_invalid_cron_raises():
    from pixelle_video.services.scheduler import TaskScheduler
    svc = TaskScheduler(data_dir="/tmp/pixelle_test_sched2")
    with pytest.raises(ValueError):
        svc.add_schedule("Bad", "invalid")

def test_list_and_remove():
    from pixelle_video.services.scheduler import TaskScheduler
    svc = TaskScheduler(data_dir="/tmp/pixelle_test_sched3")
    s = svc.add_schedule("X", "* * * * *")
    assert len(svc.list_schedules()) == 1
    assert svc.remove_schedule(s["schedule_id"]) is True
    assert len(svc.list_schedules()) == 0
