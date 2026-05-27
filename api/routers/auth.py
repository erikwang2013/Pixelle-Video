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

"""Auth API endpoints"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from pixelle_video.services.auth import UserManager

router = APIRouter(prefix="/auth", tags=["Auth"])
user_manager = UserManager()


class LoginRequest(BaseModel):
    username: str
    password: str


class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: str = "user"


class APIKeyResponse(BaseModel):
    key_id: str
    key_prefix: str
    created_at: str


@router.post("/login")
async def login(req: LoginRequest):
    user = user_manager.authenticate(req.username, req.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"status": "ok", "user": user}


@router.post("/api-keys")
async def create_api_key(req: LoginRequest):
    user = user_manager.authenticate(req.username, req.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    key = user_manager.create_api_key(req.username)
    return {"api_key": key, "message": "Store this key safely. It will not be shown again."}


@router.get("/api-keys")
async def list_api_keys(username: str, password: str):
    user = user_manager.authenticate(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user_manager.list_api_keys(username)


@router.delete("/api-keys/{key_id}")
async def revoke_api_key(key_id: str, username: str, password: str):
    user = user_manager.authenticate(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if user_manager.revoke_api_key(username, key_id):
        return {"status": "ok"}
    raise HTTPException(status_code=404, detail="Key not found")
