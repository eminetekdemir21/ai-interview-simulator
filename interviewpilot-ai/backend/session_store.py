import uuid
from datetime import datetime
from typing import Dict, List, Optional

import db


class QARecord:
    def __init__(self, question: str):
        self.question = question
        self.answer: Optional[str] = None
        self.score: Optional[int] = None
        self.feedback: Optional[str] = None
        self.missing_points: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "question": self.question, "answer": self.answer, "score": self.score,
            "feedback": self.feedback, "missing_points": self.missing_points,
        }

    @staticmethod
    def from_dict(d: dict) -> "QARecord":
        qa = QARecord(d.get("question", ""))
        qa.answer = d.get("answer")
        qa.score = d.get("score")
        qa.feedback = d.get("feedback")
        qa.missing_points = d.get("missing_points")
        return qa


class Session:
    def __init__(self, user_id: Optional[str] = None, session_id: Optional[str] = None):
        self.id = session_id or str(uuid.uuid4())
        self.user_id = user_id
        self.cv_text: str = ""
        self.job_text: str = ""
        self.history: List[QARecord] = []
        self.total_questions: int = 4
        self.finished: bool = False

        # Sirket Bazli Mulakat Modu icin secimler (Gun 2'de /api/start
        # uzerinden doldurulur; bos birakilirsa genel mod calisir).
        self.company_id: Optional[str] = None
        self.company_name: Optional[str] = None
        self.role: Optional[str] = None
        self.difficulty: Optional[str] = None
        self.interview_type: Optional[str] = None

    @property
    def current_index(self) -> int:
        return len(self.history)


class SessionStore:
    """Aktif (henuz tamamlanmamis) mulakat oturumlarini tutar. Hizli erisim
    icin bellek ici bir onbellek kullanir, ama her mutasyondan sonra
    save() cagrilarak SQLite'a da yazilir — boylece sunucu yeniden baslasa
    bile devam eden bir mulakat kaybolmaz (get() DB'den geri yukler)."""

    def __init__(self):
        self._cache: Dict[str, Session] = {}

    def create(self, user_id: Optional[str] = None) -> Session:
        session = Session(user_id=user_id)
        self._cache[session.id] = session
        self._insert(session)
        return session

    def _insert(self, session: Session):
        db.init_db()
        with db.get_conn() as conn:
            conn.execute(
                "INSERT INTO interview_sessions (id, user_id, cv_text, job_text, history_json, "
                "total_questions, finished, company_id, company_name, role, difficulty, "
                "interview_type, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (session.id, session.user_id, session.cv_text, session.job_text,
                 db.dumps([qa.to_dict() for qa in session.history]), session.total_questions,
                 int(session.finished), session.company_id, session.company_name, session.role,
                 session.difficulty, session.interview_type, datetime.now().isoformat(timespec="seconds")),
            )

    def save(self, session: Session):
        """Bir oturumdaki degisiklikleri SQLite'a yazar. Session'i mutate
        eden her endpoint, degisikligi kalici hale getirmek icin bunu
        cagirmali."""
        db.init_db()
        with db.get_conn() as conn:
            conn.execute(
                "UPDATE interview_sessions SET cv_text=?, job_text=?, history_json=?, "
                "total_questions=?, finished=?, company_id=?, company_name=?, role=?, "
                "difficulty=?, interview_type=? WHERE id=?",
                (session.cv_text, session.job_text, db.dumps([qa.to_dict() for qa in session.history]),
                 session.total_questions, int(session.finished), session.company_id,
                 session.company_name, session.role, session.difficulty, session.interview_type,
                 session.id),
            )

    def get(self, session_id: str) -> Optional[Session]:
        cached = self._cache.get(session_id)
        if cached:
            return cached
        # Bellek onbelleginde yok (orn. sunucu yeniden baslamis olabilir) —
        # SQLite'tan geri yukle.
        db.init_db()
        with db.get_conn() as conn:
            row = conn.execute("SELECT * FROM interview_sessions WHERE id = ?", (session_id,)).fetchone()
        if not row:
            return None
        session = Session(user_id=row["user_id"], session_id=row["id"])
        session.cv_text = row["cv_text"] or ""
        session.job_text = row["job_text"] or ""
        session.history = [QARecord.from_dict(d) for d in db.loads(row["history_json"], [])]
        session.total_questions = row["total_questions"]
        session.finished = bool(row["finished"])
        session.company_id = row["company_id"]
        session.company_name = row["company_name"]
        session.role = row["role"]
        session.difficulty = row["difficulty"]
        session.interview_type = row["interview_type"]
        self._cache[session_id] = session
        return session


store = SessionStore()
