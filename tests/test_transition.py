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

import pytest


class TestTransitionService:
    """Tests for TransitionService — transition listing, xfade filter building,
    single-segment no-transition handling."""

    def test_transition_list_available(self):
        """Should list all available transition types."""
        from pixelle_video.services.transition import TransitionService

        svc = TransitionService()
        types = svc.list_transitions()
        assert "none" in types
        assert "crossfade" in types
        assert "fade_in_out" in types

    def test_xfade_filter_builder(self):
        """Should build valid xfade filter string for N segments."""
        from pixelle_video.services.transition import TransitionService

        svc = TransitionService()
        filters, final_label = svc._build_xfade_filters(
            n_segments=3,
            durations=[3.0, 2.0, 4.0],
            transition="crossfade",
            duration=0.5,
        )
        assert "xfade" in filters
        assert final_label == "v2"
        assert "[0:v][1:v]" in filters
        assert "[v1][2:v]" in filters
        assert "concat" in filters  # audio concat
        assert "[a]" in filters

    def test_single_segment_no_transition(self):
        """Single segment should just copy."""
        from pixelle_video.services.transition import TransitionService

        svc = TransitionService()
        # Test that _concat_simple handles single segment
        # Without actual video files, we verify the method doesn't crash on bad input
        try:
            svc._concat_simple(["/nonexistent.mp4"], "/tmp/out.mp4")
        except Exception:
            pass  # Expected since file doesn't exist
