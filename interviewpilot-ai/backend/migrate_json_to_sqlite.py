"""Tek seferlik gecis scripti: eski JSON dosyalarindaki (users.json,
history.json, roadmap.json, challenges.json) verileri yeni SQLite
veritabanina (interviewpilot.db) tasir. Guvenlidir — birden fazla kez
calistirilirsa mevcut kayitlarin uzerine yazmaz, atlar.

Kullanim:
    cd backend
    python3 migrate_json_to_sqlite.py
"""
import json
import os

import db

_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def _load_json(name):
    path = os.path.join(_DATA_DIR, name)
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def migrate():
    db.init_db()

    users = _load_json("users.json") or []
    with db.get_conn() as conn:
        migrated = 0
        for u in users:
            existing = conn.execute("SELECT 1 FROM users WHERE id = ?", (u["id"],)).fetchone()
            if existing:
                continue
            conn.execute(
                "INSERT INTO users (id, email, name, target_role, github_username, password_hash, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (u["id"], u["email"], u["name"], u.get("target_role", ""),
                 u.get("github_username", ""), u["password_hash"], u["created_at"]),
            )
            migrated += 1
        print(f"users: {migrated}/{len(users)} tasindi")

    history = _load_json("history.json") or []
    with db.get_conn() as conn:
        migrated = 0
        for r in history:
            existing = conn.execute("SELECT 1 FROM history WHERE id = ?", (r["id"],)).fetchone()
            if existing:
                continue
            conn.execute(
                "INSERT INTO history (id, user_id, created_at, overall_score, sub_scores_json, "
                "strengths_json, weaknesses_json, summary, job_preview, company_id, company_name, "
                "role, interview_type, history_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    r["id"], r.get("user_id"), r.get("created_at"), r.get("overall_score"),
                    json.dumps(r.get("sub_scores") or {}, ensure_ascii=False),
                    json.dumps(r.get("strengths") or [], ensure_ascii=False),
                    json.dumps(r.get("weaknesses") or [], ensure_ascii=False),
                    r.get("summary"), r.get("job_preview"), r.get("company_id"),
                    r.get("company_name"), r.get("role"), r.get("interview_type"),
                    json.dumps(r.get("history") or [], ensure_ascii=False),
                ),
            )
            migrated += 1
        print(f"history: {migrated}/{len(history)} tasindi")

    roadmaps = _load_json("roadmap.json") or {}
    with db.get_conn() as conn:
        migrated = 0
        for user_id, rm in roadmaps.items():
            existing = conn.execute("SELECT 1 FROM roadmaps WHERE user_id = ?", (user_id,)).fetchone()
            if existing:
                continue
            conn.execute(
                "INSERT INTO roadmaps (user_id, focus_area, summary, weeks_json) VALUES (?, ?, ?, ?)",
                (user_id, rm.get("focus_area", ""), rm.get("summary", ""),
                 json.dumps(rm.get("weeks") or [], ensure_ascii=False)),
            )
            migrated += 1
        print(f"roadmaps: {migrated}/{len(roadmaps)} tasindi")

    challenges = _load_json("challenges.json") or {}
    with db.get_conn() as conn:
        migrated = 0
        total = 0
        for user_id, records in challenges.items():
            for rec in records:
                total += 1
                existing = conn.execute(
                    "SELECT 1 FROM challenges WHERE user_id = ? AND date = ?", (user_id, rec["date"])
                ).fetchone()
                if existing:
                    continue
                conn.execute(
                    "INSERT INTO challenges (user_id, date, question, answer, score, feedback, completed) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (user_id, rec["date"], rec.get("question"), rec.get("answer"),
                     rec.get("score"), rec.get("feedback"), int(bool(rec.get("completed")))),
                )
                migrated += 1
        print(f"challenges: {migrated}/{total} tasindi")

    print("Gecis tamamlandi.")


if __name__ == "__main__":
    migrate()
