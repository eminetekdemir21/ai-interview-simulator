"""Tamamlanan mulakatlarin sonuc raporlarini basit bir JSON dosyasinda
saklayan kucuk bir depo. Gercek bir veritabani degildir ama sunucu
yeniden baslatilsa bile gecmisin kaybolmamasini saglar.
"""
import json
import os
import threading
from datetime import datetime
from typing import List, Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")

_lock = threading.Lock()


def _ensure_file():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


def _load() -> List[dict]:
    _ensure_file()
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def _save(records: List[dict]):
    _ensure_file()
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def add_record(record: dict) -> dict:
    """Yeni bir rapor kaydi ekler. Ayni id zaten varsa (orn. kullanici
    sonuc sayfasini yeniden yukledi) tekrar eklemez, mevcut kaydi dondurur."""
    with _lock:
        records = _load()
        existing = next((r for r in records if r["id"] == record["id"]), None)
        if existing:
            return existing
        record["created_at"] = datetime.now().isoformat(timespec="seconds")
        records.insert(0, record)  # en yeni basta
        _save(records)
        return record


def list_records() -> List[dict]:
    """Ozet liste: PDF/tam gecmis olmadan, listeleme ekrani icin."""
    records = _load()
    summaries = []
    for r in records:
        summaries.append({
            "id": r["id"],
            "created_at": r.get("created_at"),
            "overall_score": r.get("overall_score"),
            "job_preview": r.get("job_preview", ""),
            "question_count": len(r.get("history", [])),
            "company_id": r.get("company_id"),
            "company_name": r.get("company_name"),
            "role": r.get("role"),
            "interview_type": r.get("interview_type"),
        })
    return summaries


def stats() -> dict:
    """Dashboard KPI'lari icin gercek verilerden hesaplanan ozet istatistik."""
    records = _load()
    if not records:
        return {
            "total_interviews": 0,
            "avg_score": 0,
            "best_score": 0,
            "streak_days": 0,
            "weakest_topic": None,
            "strongest_topic": None,
            "recent": [],
            "weekly": [],
            "avg_sub_scores": {"technical": 0, "communication": 0, "confidence": 0, "system_design": 0},
        }

    scores = [r.get("overall_score", 0) for r in records]
    avg_score = round(sum(scores) / len(scores))
    best_score = max(scores)

    # Gunluk seri: kayitlarin created_at tarihlerine gore ardisik gun sayisi
    dates = sorted({r.get("created_at", "")[:10] for r in records if r.get("created_at")}, reverse=True)
    streak = 0
    if dates:
        from datetime import datetime, timedelta
        cursor = datetime.fromisoformat(dates[0]).date()
        today = datetime.now().date()
        if (today - cursor).days <= 1:
            streak = 1
            for d in dates[1:]:
                d_date = datetime.fromisoformat(d).date()
                if (cursor - d_date).days == 1:
                    streak += 1
                    cursor = d_date
                else:
                    break

    # Konu bazli zayif/guclu: weaknesses/strengths listelerinden en sik geceni bul
    from collections import Counter
    weak_counter = Counter()
    strong_counter = Counter()
    for r in records:
        for w in r.get("weaknesses", []) or []:
            weak_counter[w] += 1
        for s in r.get("strengths", []) or []:
            strong_counter[s] += 1
    weakest = weak_counter.most_common(1)[0][0] if weak_counter else None
    strongest = strong_counter.most_common(1)[0][0] if strong_counter else None

    recent = [{
        "id": r["id"],
        "created_at": r.get("created_at"),
        "overall_score": r.get("overall_score"),
        "company_name": r.get("company_name"),
        "role": r.get("role"),
        "interview_type": r.get("interview_type"),
    } for r in records[:8]]

    weekly = [{"date": r.get("created_at", "")[:10], "score": r.get("overall_score", 0)} for r in reversed(records[:7])]

    # Sub-score'lari olan kayitlardan ortalama beceri profili (radar grafik icin)
    sub_keys = ["technical", "communication", "confidence", "system_design"]
    sub_totals = {k: 0 for k in sub_keys}
    sub_count = 0
    for r in records:
        sub = r.get("sub_scores")
        if sub:
            sub_count += 1
            for k in sub_keys:
                sub_totals[k] += sub.get(k, 0)
    avg_sub_scores = {k: round(sub_totals[k] / sub_count) for k in sub_keys} if sub_count else {k: 0 for k in sub_keys}

    return {
        "total_interviews": len(records),
        "avg_score": avg_score,
        "best_score": best_score,
        "streak_days": streak,
        "weakest_topic": weakest,
        "strongest_topic": strongest,
        "recent": recent,
        "weekly": weekly,
        "avg_sub_scores": avg_sub_scores,
    }


def get_record(item_id: str) -> Optional[dict]:
    records = _load()
    return next((r for r in records if r["id"] == item_id), None)
