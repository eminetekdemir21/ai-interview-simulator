"""Sifre sifirlama token'lari ve e-posta dogrulama kodlari icin SQLite
tabanli depo."""
import secrets
from datetime import datetime, timedelta
from typing import Optional

import db

RESET_TOKEN_TTL_MINUTES = 30
VERIFY_CODE_TTL_MINUTES = 15


def create_reset_token(user_id: str) -> str:
    db.init_db()
    token = secrets.token_urlsafe(32)
    expires_at = (datetime.now() + timedelta(minutes=RESET_TOKEN_TTL_MINUTES)).isoformat(timespec="seconds")
    with db.get_conn() as conn:
        # Ayni kullanicinin eski, kullanilmamis token'larini gecersiz kil
        conn.execute("DELETE FROM password_resets WHERE user_id = ? AND used = 0", (user_id,))
        conn.execute(
            "INSERT INTO password_resets (token, user_id, expires_at, used) VALUES (?, ?, ?, 0)",
            (token, user_id, expires_at),
        )
    return token


def verify_reset_token(token: str) -> Optional[str]:
    """Gecerliyse user_id doner, degilse (bulunamadi/suresi gecmis/kullanilmis) None."""
    db.init_db()
    with db.get_conn() as conn:
        row = conn.execute("SELECT * FROM password_resets WHERE token = ?", (token,)).fetchone()
        if not row or row["used"]:
            return None
        if datetime.fromisoformat(row["expires_at"]) < datetime.now():
            return None
        return row["user_id"]


def consume_reset_token(token: str):
    db.init_db()
    with db.get_conn() as conn:
        conn.execute("UPDATE password_resets SET used = 1 WHERE token = ?", (token,))


def create_verification_code(user_id: str) -> str:
    db.init_db()
    code = f"{secrets.randbelow(1000000):06d}"
    expires_at = (datetime.now() + timedelta(minutes=VERIFY_CODE_TTL_MINUTES)).isoformat(timespec="seconds")
    with db.get_conn() as conn:
        conn.execute(
            "INSERT INTO email_verifications (user_id, code, expires_at) VALUES (?, ?, ?) "
            "ON CONFLICT(user_id) DO UPDATE SET code=excluded.code, expires_at=excluded.expires_at",
            (user_id, code, expires_at),
        )
    return code


def verify_code(user_id: str, code: str) -> bool:
    db.init_db()
    with db.get_conn() as conn:
        row = conn.execute("SELECT * FROM email_verifications WHERE user_id = ?", (user_id,)).fetchone()
        if not row or row["code"] != code.strip():
            return False
        if datetime.fromisoformat(row["expires_at"]) < datetime.now():
            return False
        conn.execute("DELETE FROM email_verifications WHERE user_id = ?", (user_id,))
        return True
