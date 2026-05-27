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
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo   Pixelle-Video - Windows Launcher
echo ========================================
echo.

:: Set environment variables
set "PYTHON_HOME=%~dp0python\python311"
set "PATH=%PYTHON_HOME%;%PYTHON_HOME%\Scripts;%~dp0tools\ffmpeg\bin;%PATH%"
set "PROJECT_ROOT=%~dp0Pixelle-Video"

:: Change to project directory
cd /d "%PROJECT_ROOT%"

:: Set PYTHONPATH to project root for module imports
set "PYTHONPATH=%PROJECT_ROOT%"

:: Set PIXELLE_VIDEO_ROOT environment variable for reliable path resolution
set "PIXELLE_VIDEO_ROOT=%PROJECT_ROOT%"

:: Start Web UI
echo [Starting] Launching Pixelle-Video Web UI...
echo Browser will open automatically.
echo.
echo Note: Configure API keys and settings in the Web UI.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

"%PYTHON_HOME%\python.exe" -m streamlit run web\app.py

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start. Please check:
    echo   1. Python is properly installed
    echo   2. Dependencies are installed
    echo.
    pause
)

