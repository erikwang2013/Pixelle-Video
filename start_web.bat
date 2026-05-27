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

@echo off
chcp 65001 >nul 2>&1

echo 🚀 Starting Pixelle-Video Web UI...
echo.

uv run streamlit run web/app.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo   [ERROR] Failed to Start
    echo ========================================
    echo.
    echo It appears you downloaded the SOURCE CODE directly.
    echo.
    echo ========================================
    echo   For Regular Users:
    echo ========================================
    echo Please download the ONE-CLICK PACKAGE from:
    echo https://github.com/AIDC-AI/Pixelle-Video/releases
    echo.
    echo The one-click package includes:
    echo   ✓ Pre-configured Python environment
    echo   ✓ All required dependencies
    echo   ✓ FFmpeg tools
    echo   ✓ Ready to use, no setup needed
    echo.
    echo ========================================
    echo   For Developers:
    echo ========================================
    echo If you intend to develop or modify the code:
    echo   1. Install uv: https://docs.astral.sh/uv/
    echo   2. Run: uv sync
    echo   3. Then run this script again
    echo.
    echo ========================================
    echo.
    pause
)


