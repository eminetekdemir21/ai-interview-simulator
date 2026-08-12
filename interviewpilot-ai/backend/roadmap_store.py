"""Kullanicilarin kisisellestirilmis ogrenme yol haritalarini (Gemini
tarafindan uretilen) ve gorev tamamlama durumlarini SQLite'ta saklar."""
from typing import Optional

import db


def get_roadmap(user_id: str) -> Optional[dict]:
    db.init_db()
    with db.get_conn() as conn:
        row = conn.execute("SELECT * FROM roadmaps WHERE user_id = ?", (user_id,)).fetchone()
        if not row:
            return None
        return {
            "focus_area": row["focus_area"],
            "summary": row["summary"],
            "weeks": db.loads(row["weeks_json"], []),
        }


def save_roadmap(user_id: str, generated: dict) -> dict:
    """Gemini'den gelen ham veriyi (tasks: [str,...]) checklist formatina
    (tasks: [{text, done}, ...]) cevirip kaydeder."""
    db.init_db()
    weeks = []
    for w in generated.get("weeks", []):
        tasks = [{"text": t, "done": False} for t in w.get("tasks", [])]
        weeks.append({"title": w.get("title", ""), "tasks": tasks})
    roadmap = {
        "focus_area": generated.get("focus_area", ""),
        "summary": generated.get("summary", ""),
        "weeks": weeks,
    }
    with db.get_conn() as conn:
        conn.execute(
            "INSERT INTO roadmaps (user_id, focus_area, summary, weeks_json) VALUES (?, ?, ?, ?) "
            "ON CONFLICT(user_id) DO UPDATE SET focus_area=excluded.focus_area, "
            "summary=excluded.summary, weeks_json=excluded.weeks_json",
            (user_id, roadmap["focus_area"], roadmap["summary"], db.dumps(weeks)),
        )
    return roadmap


def toggle_task(user_id: str, week_index: int, task_index: int) -> Optional[dict]:
    db.init_db()
    with db.get_conn() as conn:
        row = conn.execute("SELECT * FROM roadmaps WHERE user_id = ?", (user_id,)).fetchone()
        if not row:
            return None
        weeks = db.loads(row["weeks_json"], [])
        try:
            task = weeks[week_index]["tasks"][task_index]
            task["done"] = not task["done"]
        except (IndexError, KeyError, TypeError):
            return None
        conn.execute("UPDATE roadmaps SET weeks_json = ? WHERE user_id = ?", (db.dumps(weeks), user_id))
        return {"focus_area": row["focus_area"], "summary": row["summary"], "weeks": weeks}
