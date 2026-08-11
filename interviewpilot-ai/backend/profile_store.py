import json
import os

_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
_PROFILE_PATH = os.path.join(_DATA_DIR, "profile.json")

_DEFAULT_PROFILE = {
    "name": "",
    "email": "",
    "target_role": "",
}


def get_profile() -> dict:
    if not os.path.isfile(_PROFILE_PATH):
        return dict(_DEFAULT_PROFILE)
    try:
        with open(_PROFILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        merged = dict(_DEFAULT_PROFILE)
        merged.update(data or {})
        return merged
    except (json.JSONDecodeError, OSError):
        return dict(_DEFAULT_PROFILE)


def save_profile(data: dict) -> dict:
    os.makedirs(_DATA_DIR, exist_ok=True)
    profile = get_profile()
    profile.update({k: v for k, v in data.items() if k in _DEFAULT_PROFILE})
    with open(_PROFILE_PATH, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)
    return profile
