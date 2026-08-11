"""GitHub'in genel (public) REST API'sini kullanarak, OAuth/token gerektirmeden
bir kullanicinin genel profil ve repo bilgilerini ceker. Ekstra pip bagimliligi
eklememek icin sadece Python standart kutuphanesi (urllib) kullanilir."""
import json
import urllib.request
import urllib.error

_BASE = "https://api.github.com"
_HEADERS = {"Accept": "application/vnd.github+json", "User-Agent": "InterviewPilot-AI"}


def _get(path: str) -> dict | list:
    req = urllib.request.Request(f"{_BASE}{path}", headers=_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise ValueError("GitHub kullanici adi bulunamadi")
        if e.code == 403:
            raise ValueError("GitHub API istek limitine ulasildi, birkac dakika sonra tekrar dene")
        raise ValueError(f"GitHub API hatasi: {e.code}")
    except urllib.error.URLError:
        raise ValueError("GitHub'a baglanilamadi, internet baglantini kontrol et")


def fetch_profile(username: str) -> dict:
    data = _get(f"/users/{username}")
    return {
        "login": data.get("login"),
        "name": data.get("name") or data.get("login"),
        "avatar_url": data.get("avatar_url"),
        "bio": data.get("bio"),
        "public_repos": data.get("public_repos", 0),
        "followers": data.get("followers", 0),
        "html_url": data.get("html_url"),
    }


def fetch_repos(username: str, limit: int = 8) -> list[dict]:
    data = _get(f"/users/{username}/repos?sort=updated&per_page=30")
    repos = [r for r in data if not r.get("fork")]
    repos.sort(key=lambda r: r.get("updated_at") or "", reverse=True)
    return [
        {
            "name": r.get("name"),
            "description": r.get("description"),
            "language": r.get("language"),
            "stars": r.get("stargazers_count", 0),
            "html_url": r.get("html_url"),
            "updated_at": r.get("updated_at"),
        }
        for r in repos[:limit]
    ]
