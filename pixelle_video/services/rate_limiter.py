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

"""API rate limiting with token bucket algorithm"""
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class TokenBucket:
    tokens: float = 0.0
    last_refill: float = field(default_factory=time.time)


class RateLimiter:
    def __init__(self):
        self._buckets: Dict[str, TokenBucket] = defaultdict(TokenBucket)
        self._limits: Dict[str, tuple] = {}  # user_id -> (rate, burst)

    def set_limit(self, user_id: str, rate: float = 10.0, burst: int = 20):
        """Set rate limit: `rate` requests/sec, `burst` max tokens."""
        self._limits[user_id] = (rate, burst)
        # Pre-fill bucket with burst tokens so initial requests are allowed
        bucket = self._buckets[user_id]
        bucket.tokens = float(burst)
        bucket.last_refill = time.time()

    def check_limit(self, user_id: str) -> bool:
        """Check if request is allowed. Returns True if allowed."""
        rate, burst = self._limits.get(user_id, (10.0, 20))
        bucket = self._buckets[user_id]

        now = time.time()
        elapsed = now - bucket.last_refill
        bucket.tokens = min(burst, bucket.tokens + elapsed * rate)
        bucket.last_refill = now

        if bucket.tokens >= 1.0:
            bucket.tokens -= 1.0
            return True
        return False

    def get_remaining(self, user_id: str) -> int:
        rate, burst = self._limits.get(user_id, (10.0, 20))
        bucket = self._buckets[user_id]
        return int(bucket.tokens)
