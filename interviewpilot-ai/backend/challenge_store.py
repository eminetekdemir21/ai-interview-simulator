"""Gunluk Meydan Okuma (Daily Challenge) icin SQLite tabanli depo.
Her kullanicinin gunluk mini soru gecmisini (tarih, soru, cevap, puan)
saklar; gercek seri (streak) ve haftalik ilerleme buradan hesaplanir."""
from datetime import date, timedelta
from typing import Optional

import db


def _today() -> str:
    return date.today().isoformat()


def get_today(user_id: str) -> Optional[dict]:
    db.init_db()
    with db.get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM challenges WHERE user_id = ? AND date = ?", (user_id, _today())
        ).fetchone()
        return db.row_to_dict(row)


def create_today(user_id: str, question: str) -> dict:
    db.init_db()
    today = _today()
    with db.get_conn() as conn:
        existing = conn.execute(
            "SELECT * FROM challenges WHERE user_id = ? AND date = ?", (user_id, today)
        ).fetchone()
        if existing:
            return db.row_to_dict(existing)
        conn.execute(
            "INSERT INTO challenges (user_id, date, question, answer, score, feedback, completed) "
            "VALUES (?, ?, ?, NULL, NULL, NULL, 0)",
            (user_id, today, question),
        )
        return {"user_id": user_id, "date": today, "question": question, "answer": None,
                "score": None, "feedback": None, "completed": False}


def submit_answer(user_id: str, answer: str, score: int, feedback: str) -> Optional[dict]:
    db.init_db()
    today = _today()
    with db.get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM challenges WHERE user_id = ? AND date = ?", (user_id, today)
        ).fetchone()
        if not row:
            return None
        conn.execute(
            "UPDATE challenges SET answer = ?, score = ?, feedback = ?, completed = 1 "
            "WHERE user_id = ? AND date = ?",
            (answer, score, feedback, user_id, today),
        )
        updated = conn.execute(
            "SELECT * FROM challenges WHERE user_id = ? AND date = ?", (user_id, today)
        ).fetchone()
        return db.row_to_dict(updated)


def list_records(user_id: str) -> list[dict]:
    db.init_db()
    with db.get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM challenges WHERE user_id = ? ORDER BY date DESC", (user_id,)
        ).fetchall()
        return [dict(r) for r in rows]


def compute_stats(user_id: str) -> dict:
    """Gercek tamamlanmis gunlerden seri (streak) ve son 7 gunluk ilerlemeyi hesaplar."""
    db.init_db()
    with db.get_conn() as conn:
        rows = conn.execute(
            "SELECT date FROM challenges WHERE user_id = ? AND completed = 1", (user_id,)
        ).fetchall()
    completed_dates = {r["date"] for r in rows}

    today = date.today()
    streak = 0
    cursor = today
    if today.isoformat() not in completed_dates:
        cursor = today - timedelta(days=1)
    while cursor.isoformat() in completed_dates:
        streak += 1
        cursor -= timedelta(days=1)

    week_completed = sum(1 for i in range(7) if (today - timedelta(days=i)).isoformat() in completed_dates)

    badge_threshold = 30
    return {
        "streak": streak,
        "week_completed": week_completed,
        "week_total": 7,
        "badge_threshold": badge_threshold,
        "days_to_badge": max(0, badge_threshold - streak),
        "badge_earned": streak >= badge_threshold,
    }
