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

"""
Health check and system info endpoints
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = "healthy"
    version: str = "0.1.0"
    service: str = "Pixelle-Video API"


class CapabilitiesResponse(BaseModel):
    """Capabilities response"""
    success: bool = True
    capabilities: dict


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    
    Returns service status and version information.
    """
    return HealthResponse()


@router.get("/ready")
async def readiness_check():
    """
    Kubernetes readiness probe — checks all dependencies.

    Verifies that ffmpeg is available and the database is reachable.
    """
    import shutil

    checks: dict = {"ffmpeg": False, "db": False}

    checks["ffmpeg"] = shutil.which("ffmpeg") is not None

    try:
        from pixelle_video.services.database import DatabaseService

        DatabaseService().get_stats()
        checks["db"] = True
    except Exception:
        pass

    all_ok = all(checks.values())
    return {"status": "ready" if all_ok else "not_ready", "checks": checks}


@router.get("/live")
async def liveness_check():
    """
    Kubernetes liveness probe — basic alive check.

    Returns a simple alive status without checking dependencies.
    """
    return {"status": "alive"}


@router.get("/version", response_model=HealthResponse)
async def get_version():
    """
    Get API version

    Returns version information.
    """
    return HealthResponse()

