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
