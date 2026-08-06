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
        })
    return summaries


def get_record(item_id: str) -> Optional[dict]:
    records = _load()
    return next((r for r in records if r["id"] == item_id), None)
