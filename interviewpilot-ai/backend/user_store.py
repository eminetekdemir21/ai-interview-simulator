"""Coklu kullanici deposu — SQLite tabanli. Her kullanicinin kendi
hesabiyla kayit olup giris yapmasini ve verilerinin (CV gecmisi, profil)
ayri tutulmasini saglar."""
import hashlib
import secrets
from datetime import datetime
from typing import Optional

import db


def _hash_password(password: str, salt: Optional[str] = None) -> str:
    salt = salt or secrets.token_hex(16)
    digest = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return f"{salt}${digest}"


def _verify_password(password: str, stored: str) -> bool:
    try:
        salt, _ = stored.split("$", 1)
    except ValueError:
        return False
    return secrets.compare_digest(_hash_password(password, salt), stored)


def get_user_by_email(email: str) -> Optional[dict]:
    email = email.strip().lower()
    db.init_db()
    with db.get_conn() as conn:
        row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        return db.row_to_dict(row)


def get_user(user_id: str) -> Optional[dict]:
    db.init_db()
    with db.get_conn() as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return db.row_to_dict(row)


def create_user(email: str, password: str, name: str) -> dict:
    db.init_db()
    email = email.strip().lower()
    if not email or "@" not in email:
        raise ValueError("Gecerli bir e-posta adresi gir")
    if len(password) < 6:
        raise ValueError("Sifre en az 6 karakter olmali")
    with db.get_conn() as conn:
        existing = conn.execute("SELECT 1 FROM users WHERE email = ?", (email,)).fetchone()
        if existing:
            raise ValueError("Bu e-posta ile zaten bir hesap var")
        user = {
            "id": secrets.token_hex(12),
            "email": email,
            "name": name.strip() or email.split("@")[0],
            "target_role": "",
            "github_username": "",
            "password_hash": _hash_password(password),
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
        conn.execute(
            "INSERT INTO users (id, email, name, target_role, github_username, password_hash, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user["id"], user["email"], user["name"], user["target_role"],
             user["github_username"], user["password_hash"], user["created_at"]),
        )
        return user


def verify_login(email: str, password: str) -> Optional[dict]:
    user = get_user_by_email(email)
    if not user or not _verify_password(password, user["password_hash"]):
        return None
    return user


def update_user(user_id: str, fields: dict) -> dict:
    db.init_db()
    with db.get_conn() as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if not row:
            raise ValueError("Kullanici bulunamadi")
        user = dict(row)
        for key in ("name", "target_role", "github_username"):
            if fields.get(key) is not None:
                user[key] = fields[key]
        conn.execute(
            "UPDATE users SET name = ?, target_role = ?, github_username = ? WHERE id = ?",
            (user["name"], user["target_role"], user["github_username"], user_id),
        )
        return user


def set_password(user_id: str, new_password: str):
    db.init_db()
    if len(new_password) < 6:
        raise ValueError("Sifre en az 6 karakter olmali")
    with db.get_conn() as conn:
        conn.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (_hash_password(new_password), user_id),
        )


def mark_email_verified(user_id: str):
    db.init_db()
    with db.get_conn() as conn:
        conn.execute("UPDATE users SET email_verified = 1 WHERE id = ?", (user_id,))


def public_user(user: dict) -> dict:
    user = dict(user)
    user["email_verified"] = bool(user.get("email_verified"))
    return {k: v for k, v in user.items() if k != "password_hash"}
