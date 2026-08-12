"""SQLite veritabani baglantisi ve semasi. Basit dosya tabanli JSON depolarin
yerini alir; ekstra bir pip bagimliligi gerektirmez (Python'un yerlesik
sqlite3 modulunu kullanir). Her fonksiyon kendi kisa omurlu baglantisini
acip isini bitirince kapatir (dosya tabanli eski deponun ayni deseni) —
boylece coklu istek/thread arasinda basit ve guvenli kalir.
"""
import json
import os
import sqlite3
import threading
from contextlib import contextmanager

_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DB_PATH = os.path.join(_DATA_DIR, "interviewpilot.db")
_lock = threading.Lock()
_initialized = False


@contextmanager
def get_conn():
    os.makedirs(_DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    global _initialized
    if _initialized:
        return
    with _lock:
        if _initialized:
            return
        with get_conn() as conn:
            conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                target_role TEXT DEFAULT '',
                github_username TEXT DEFAULT '',
                password_hash TEXT NOT NULL,
                email_verified INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS password_resets (
                token TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                used INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS email_verifications (
                user_id TEXT PRIMARY KEY,
                code TEXT NOT NULL,
                expires_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS auth_sessions (
                token TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS interview_sessions (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                cv_text TEXT DEFAULT '',
                job_text TEXT DEFAULT '',
                history_json TEXT DEFAULT '[]',
                total_questions INTEGER DEFAULT 4,
                finished INTEGER DEFAULT 0,
                company_id TEXT,
                company_name TEXT,
                role TEXT,
                difficulty TEXT,
                interview_type TEXT,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS history (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                created_at TEXT NOT NULL,
                overall_score INTEGER,
                sub_scores_json TEXT,
                strengths_json TEXT,
                weaknesses_json TEXT,
                summary TEXT,
                job_preview TEXT,
                company_id TEXT,
                company_name TEXT,
                role TEXT,
                interview_type TEXT,
                history_json TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_history_user ON history(user_id);

            CREATE TABLE IF NOT EXISTS roadmaps (
                user_id TEXT PRIMARY KEY,
                focus_area TEXT,
                summary TEXT,
                weeks_json TEXT
            );

            CREATE TABLE IF NOT EXISTS challenges (
                user_id TEXT NOT NULL,
                date TEXT NOT NULL,
                question TEXT,
                answer TEXT,
                score INTEGER,
                feedback TEXT,
                completed INTEGER DEFAULT 0,
                PRIMARY KEY (user_id, date)
            );
            """)
            # Eski veritabanlarinda (bu sutun eklenmeden once olusturulmus)
            # users tablosuna email_verified sutununu sonradan ekle.
            existing_cols = {row["name"] for row in conn.execute("PRAGMA table_info(users)").fetchall()}
            if "email_verified" not in existing_cols:
                conn.execute("ALTER TABLE users ADD COLUMN email_verified INTEGER DEFAULT 0")
        _initialized = True


def row_to_dict(row: sqlite3.Row | None) -> dict | None:
    return dict(row) if row is not None else None


def loads(text: str | None, default):
    if not text:
        return default
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return default


def dumps(value) -> str:
    return json.dumps(value, ensure_ascii=False)
