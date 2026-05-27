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
