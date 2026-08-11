"""Basit, dosya tabanli coklu kullanici deposu. Gercek bir veritabani
degildir ama her kullanicinin kendi hesabiyla kayit olup giris yapmasini
ve verilerinin (CV gecmisi, profil) ayri tutulmasini saglar."""
import hashlib
import json
import os
import secrets
import threading
from datetime import datetime
from typing import Optional

_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
_USERS_PATH = os.path.join(_DATA_DIR, "users.json")
_lock = threading.Lock()


def _load() -> list[dict]:
    if not os.path.isfile(_USERS_PATH):
        return []
    try:
        with open(_USERS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def _save(users: list[dict]):
    os.makedirs(_DATA_DIR, exist_ok=True)
    with open(_USERS_PATH, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


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
    return next((u for u in _load() if u["email"] == email), None)


def get_user(user_id: str) -> Optional[dict]:
    return next((u for u in _load() if u["id"] == user_id), None)


def create_user(email: str, password: str, name: str) -> dict:
    with _lock:
        users = _load()
        email = email.strip().lower()
        if not email or "@" not in email:
            raise ValueError("Gecerli bir e-posta adresi gir")
        if len(password) < 6:
            raise ValueError("Sifre en az 6 karakter olmali")
        if any(u["email"] == email for u in users):
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
        users.append(user)
        _save(users)
        return user


def verify_login(email: str, password: str) -> Optional[dict]:
    user = get_user_by_email(email)
    if not user or not _verify_password(password, user["password_hash"]):
        return None
    return user


def update_user(user_id: str, fields: dict) -> dict:
    with _lock:
        users = _load()
        user = next((u for u in users if u["id"] == user_id), None)
        if not user:
            raise ValueError("Kullanici bulunamadi")
        for key in ("name", "target_role", "github_username"):
            if fields.get(key) is not None:
                user[key] = fields[key]
        _save(users)
        return user


def public_user(user: dict) -> dict:
    return {k: v for k, v in user.items() if k != "password_hash"}
