"""Cerez tabanli oturum yonetimi. Oturum token'lari SQLite'ta saklanir,
boylece sunucu yeniden baslasa bile kullanicilar tekrar giris yapmak
zorunda kalmaz (eskiden bellek ici tutuluyordu)."""
import secrets
from datetime import datetime

from fastapi import HTTPException, Request

import db
import user_store

COOKIE_NAME = "ip_session"


def create_session(user_id: str) -> str:
    db.init_db()
    token = secrets.token_hex(24)
    with db.get_conn() as conn:
        conn.execute(
            "INSERT INTO auth_sessions (token, user_id, created_at) VALUES (?, ?, ?)",
            (token, user_id, datetime.now().isoformat(timespec="seconds")),
        )
    return token


def destroy_session(token: str | None):
    if not token:
        return
    db.init_db()
    with db.get_conn() as conn:
        conn.execute("DELETE FROM auth_sessions WHERE token = ?", (token,))


def get_current_user(request: Request) -> dict:
    token = request.cookies.get(COOKIE_NAME)
    db.init_db()
    user_id = None
    if token:
        with db.get_conn() as conn:
            row = conn.execute("SELECT user_id FROM auth_sessions WHERE token = ?", (token,)).fetchone()
            user_id = row["user_id"] if row else None
    if not user_id:
        raise HTTPException(401, "Giris yapmalisin")
    user = user_store.get_user(user_id)
    if not user:
        raise HTTPException(401, "Giris yapmalisin")
    return user
