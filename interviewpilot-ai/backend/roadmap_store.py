"""Kullanicilarin kisisellestirilmis ogrenme yol haritalarini (Gemini
tarafindan uretilen) ve gorev tamamlama durumlarini saklayan basit,
dosya tabanli depo."""
import json
import os
import threading
from typing import Optional

_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
_PATH = os.path.join(_DATA_DIR, "roadmap.json")
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


def get_roadmap(user_id: str) -> Optional[dict]:
    return _load().get(user_id)


def save_roadmap(user_id: str, generated: dict) -> dict:
    """Gemini'den gelen ham veriyi (tasks: [str,...]) checklist formatina
    (tasks: [{text, done}, ...]) cevirip kaydeder."""
    with _lock:
        data = _load()
        weeks = []
        for w in generated.get("weeks", []):
            tasks = [{"text": t, "done": False} for t in w.get("tasks", [])]
            weeks.append({"title": w.get("title", ""), "tasks": tasks})
        roadmap = {
            "focus_area": generated.get("focus_area", ""),
            "summary": generated.get("summary", ""),
            "weeks": weeks,
        }
        data[user_id] = roadmap
        _save(data)
        return roadmap


def toggle_task(user_id: str, week_index: int, task_index: int) -> Optional[dict]:
    with _lock:
        data = _load()
        roadmap = data.get(user_id)
        if not roadmap:
            return None
        try:
            task = roadmap["weeks"][week_index]["tasks"][task_index]
            task["done"] = not task["done"]
        except (IndexError, KeyError, TypeError):
            return None
        data[user_id] = roadmap
        _save(data)
        return roadmap
