"""Cerez tabanli basit oturum yonetimi. Bellek ici tutulur (sunucu
yeniden baslatilinca herkes tekrar giris yapmali)."""
import secrets

from fastapi import HTTPException, Request

import user_store

COOKIE_NAME = "ip_session"
_sessions: dict[str, str] = {}  # token -> user_id


def create_session(user_id: str) -> str:
    token = secrets.token_hex(24)
    _sessions[token] = user_id
    return token


def destroy_session(token: str | None):
    if token:
        _sessions.pop(token, None)


def get_current_user(request: Request) -> dict:
    token = request.cookies.get(COOKIE_NAME)
    user_id = _sessions.get(token) if token else None
    if not user_id:
        raise HTTPException(401, "Giris yapmalisin")
    user = user_store.get_user(user_id)
    if not user:
        raise HTTPException(401, "Giris yapmalisin")
    return user
