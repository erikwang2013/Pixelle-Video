import pytest

def test_list_platforms():
    from pixelle_video.services.social_publisher import SocialPublisher
    svc = SocialPublisher(data_dir="/tmp/pixelle_test_social")
    platforms = svc.list_platforms()
    assert "youtube" in platforms
    assert "bilibili" in platforms

def test_unsupported_platform():
    from pixelle_video.services.social_publisher import SocialPublisher
    import pytest, asyncio
    svc = SocialPublisher(data_dir="/tmp/pixelle_test_social2")
    with pytest.raises(ValueError):
        asyncio.run(svc.publish("unsupported", "/tmp/v.mp4", "Test"))
