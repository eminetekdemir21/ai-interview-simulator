import uuid
from typing import Dict, List, Optional


class QARecord:
    def __init__(self, question: str):
        self.question = question
        self.answer: Optional[str] = None
        self.score: Optional[int] = None
        self.feedback: Optional[str] = None
        self.missing_points: Optional[str] = None


class Session:
    def __init__(self, user_id: Optional[str] = None):
        self.id = str(uuid.uuid4())
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
    """Basit bellek ici oturum deposu. Gercek bir veritabani degildir,
    sunucu yeniden baslatilinca aktif oturumlar silinir (tamamlanmis
    mulakatlar history_store.py araciligiyla diskte kalir)."""

    def __init__(self):
        self._sessions: Dict[str, Session] = {}

    def create(self, user_id: Optional[str] = None) -> Session:
        session = Session(user_id=user_id)
        self._sessions[session.id] = session
        return session

    def get(self, session_id: str) -> Optional[Session]:
        return self._sessions.get(session_id)


store = SessionStore()
