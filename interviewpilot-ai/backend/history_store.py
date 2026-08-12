"""Tamamlanan mulakatlarin sonuc raporlarini SQLite'ta saklayan depo.
Eskiden tek bir JSON dosyasi kullaniliyordu; simdi gercek bir veritabani
uzerinden, kullaniciya gore izole edilmis sekilde saklanir."""
from datetime import datetime
from typing import List, Optional

import db


def add_record(record: dict) -> dict:
    """Yeni bir rapor kaydi ekler. Ayni id zaten varsa (orn. kullanici
    sonuc sayfasini yeniden yukledi) tekrar eklemez, mevcut kaydi dondurur."""
    db.init_db()
    with db.get_conn() as conn:
        existing = conn.execute("SELECT * FROM history WHERE id = ?", (record["id"],)).fetchone()
        if existing:
            row = dict(existing)
            row["sub_scores"] = db.loads(row.pop("sub_scores_json", None), {})
            row["strengths"] = db.loads(row.pop("strengths_json", None), [])
            row["weaknesses"] = db.loads(row.pop("weaknesses_json", None), [])
            row["history"] = db.loads(row.pop("history_json", None), [])
            return row

        record = dict(record)
        record["created_at"] = datetime.now().isoformat(timespec="seconds")
        conn.execute(
            "INSERT INTO history (id, user_id, created_at, overall_score, sub_scores_json, "
            "strengths_json, weaknesses_json, summary, job_preview, company_id, company_name, "
            "role, interview_type, history_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                record["id"], record.get("user_id"), record["created_at"], record.get("overall_score"),
                db.dumps(record.get("sub_scores") or {}), db.dumps(record.get("strengths") or []),
                db.dumps(record.get("weaknesses") or []), record.get("summary"), record.get("job_preview"),
                record.get("company_id"), record.get("company_name"), record.get("role"),
                record.get("interview_type"), db.dumps(record.get("history") or []),
            ),
        )
        return record


def _full_records(user_id: Optional[str] = None) -> List[dict]:
    db.init_db()
    with db.get_conn() as conn:
        if user_id is not None:
            rows = conn.execute(
                "SELECT * FROM history WHERE user_id = ? ORDER BY created_at DESC", (user_id,)
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM history ORDER BY created_at DESC").fetchall()
        records = []
        for row in rows:
            r = dict(row)
            r["sub_scores"] = db.loads(r.pop("sub_scores_json", None), {})
            r["strengths"] = db.loads(r.pop("strengths_json", None), [])
            r["weaknesses"] = db.loads(r.pop("weaknesses_json", None), [])
            r["history"] = db.loads(r.pop("history_json", None), [])
            records.append(r)
        return records


def list_records(user_id: Optional[str] = None) -> List[dict]:
    """Ozet liste: PDF/tam gecmis olmadan, listeleme ekrani icin."""
    records = _full_records(user_id)
    return [{
        "id": r["id"],
        "created_at": r.get("created_at"),
        "overall_score": r.get("overall_score"),
        "job_preview": r.get("job_preview", ""),
        "question_count": len(r.get("history", [])),
        "company_id": r.get("company_id"),
        "company_name": r.get("company_name"),
        "role": r.get("role"),
        "interview_type": r.get("interview_type"),
    } for r in records]


def stats(user_id: Optional[str] = None) -> dict:
    """Dashboard KPI'lari icin gercek verilerden hesaplanan ozet istatistik."""
    records = _full_records(user_id)
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

    dates = sorted({r.get("created_at", "")[:10] for r in records if r.get("created_at")}, reverse=True)
    streak = 0
    if dates:
        from datetime import timedelta
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


def get_record(item_id: str, user_id: Optional[str] = None) -> Optional[dict]:
    """user_id verilirse, kayit baska bir kullaniciya aitse None doner."""
    db.init_db()
    with db.get_conn() as conn:
        row = conn.execute("SELECT * FROM history WHERE id = ?", (item_id,)).fetchone()
        if not row:
            return None
        record = dict(row)
        if user_id is not None and record.get("user_id") != user_id:
            return None
        record["sub_scores"] = db.loads(record.pop("sub_scores_json", None), {})
        record["strengths"] = db.loads(record.pop("strengths_json", None), [])
        record["weaknesses"] = db.loads(record.pop("weaknesses_json", None), [])
        record["history"] = db.loads(record.pop("history_json", None), [])
        return record
