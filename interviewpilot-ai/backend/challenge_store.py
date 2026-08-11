"""Gunluk Meydan Okuma (Daily Challenge) icin dosya tabanli depo.
Her kullanicinin gunluk mini soru gecmisini (tarih, soru, cevap, puan)
saklar; gercek seri (streak) ve haftalik ilerleme buradan hesaplanir."""
import json
import os
import threading
from datetime import date, timedelta
from typing import Optional

_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
_PATH = os.path.join(_DATA_DIR, "challenges.json")
_lock = threading.Lock()


def _load() -> dict:
    if not os.path.isfile(_PATH):
        return {}
    try:
        with open(_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _save(data: dict):
    os.makedirs(_DATA_DIR, exist_ok=True)
    with open(_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _today() -> str:
    return date.today().isoformat()


def get_today(user_id: str) -> Optional[dict]:
    records = _load().get(user_id, [])
    today = _today()
    return next((r for r in records if r["date"] == today), None)


def create_today(user_id: str, question: str) -> dict:
    with _lock:
        data = _load()
        records = data.setdefault(user_id, [])
        today = _today()
        existing = next((r for r in records if r["date"] == today), None)
        if existing:
            return existing
        record = {"date": today, "question": question, "answer": None, "score": None, "feedback": None, "completed": False}
        records.append(record)
        _save(data)
        return record


def submit_answer(user_id: str, answer: str, score: int, feedback: str) -> Optional[dict]:
    with _lock:
        data = _load()
        records = data.get(user_id, [])
        today = _today()
        record = next((r for r in records if r["date"] == today), None)
        if not record:
            return None
        record["answer"] = answer
        record["score"] = score
        record["feedback"] = feedback
        record["completed"] = True
        _save(data)
        return record


def list_records(user_id: str) -> list[dict]:
    return sorted(_load().get(user_id, []), key=lambda r: r["date"], reverse=True)


def compute_stats(user_id: str) -> dict:
    """Gercek tamamlanmis gunlerden seri (streak) ve son 7 gunluk ilerlemeyi hesaplar."""
    records = [r for r in _load().get(user_id, []) if r.get("completed")]
    completed_dates = {r["date"] for r in records}

    today = date.today()
    # Seri: bugunden (ya da dunden, bugun henuz yapilmadiysa) geriye dogru ardisik tamamlanmis gunler
    streak = 0
    cursor = today
    if today.isoformat() not in completed_dates:
        cursor = today - timedelta(days=1)
    while cursor.isoformat() in completed_dates:
        streak += 1
        cursor -= timedelta(days=1)

    # Son 7 takvim gunu (bugun dahil) icinde kac gun tamamlanmis
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
