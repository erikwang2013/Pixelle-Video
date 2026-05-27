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

"""Cloud storage integration (S3, OSS, COS)"""
import os
from pathlib import Path
from typing import Optional, Dict
import hashlib
import mimetypes
from loguru import logger


class CloudStorageService:
    PROVIDERS = ["s3", "oss", "cos", "local"]

    def list_providers(self):
        return self.PROVIDERS

    async def upload(self, file_path: str, provider: str = "local",
                     credentials: Dict = None) -> Dict:
        """Upload file to cloud storage. Returns {"url": str, "provider": str}."""
        credentials = credentials or {}

        if provider == "local":
            return self._upload_local(file_path, credentials)
        elif provider == "s3":
            return await self._upload_s3(file_path, credentials)
        elif provider == "oss":
            return await self._upload_oss(file_path, credentials)
        else:
            return {"url": "", "error": f"Provider {provider} not supported or missing credentials", "provider": provider}

    def _upload_local(self, file_path: str, credentials: Dict) -> Dict:
        """Copy to local public directory."""
        public_dir = Path(credentials.get("public_dir", "data/public"))
        public_dir.mkdir(parents=True, exist_ok=True)
        dest = public_dir / Path(file_path).name
        import shutil
        shutil.copy(file_path, dest)
        base_url = credentials.get("base_url", "http://localhost:8000")
        return {"url": f"{base_url}/files/public/{dest.name}", "provider": "local"}

    async def _upload_s3(self, file_path: str, credentials: Dict) -> Dict:
        """Upload to S3-compatible storage using httpx."""
        try:
            import httpx
            bucket = credentials.get("bucket", "")
            endpoint = credentials.get("endpoint", "")
            region = credentials.get("region", "us-east-1")
            access_key = credentials.get("access_key", "")
            secret_key = credentials.get("secret_key", "")

            if not all([bucket, endpoint, access_key, secret_key]):
                return {"url": "", "error": "Missing S3 credentials", "provider": "s3"}

            obj_key = f"pixelle-video/{Path(file_path).name}"
            content_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"

            with open(file_path, "rb") as f:
                data = f.read()

            url = f"{endpoint}/{bucket}/{obj_key}"
            async with httpx.AsyncClient(timeout=60) as client:
                resp = await client.put(url, content=data, headers={
                    "Content-Type": content_type,
                    "x-amz-acl": "public-read",
                })
                if resp.status_code < 300:
                    return {"url": url, "provider": "s3"}
                return {"url": "", "error": f"S3 upload failed: {resp.status_code}", "provider": "s3"}
        except Exception as e:
            logger.error(f"S3 upload error: {e}")
            return {"url": "", "error": str(e), "provider": "s3"}

    async def _upload_oss(self, file_path: str, credentials: Dict) -> Dict:
        """Upload to Aliyun OSS — placeholder."""
        return {"url": "", "error": "OSS provider requires aliyun-oss SDK. Install: pip install oss2", "provider": "oss"}
