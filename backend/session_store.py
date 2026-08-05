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
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.cv_text: str = ""
        self.job_text: str = ""
        self.history: List[QARecord] = []
        # Test asamasinda ucretsiz Gemini kotasini az tuketmek icin 4'e
        # dusuruldu; istersen bu sayiyi tekrar artirabilirsin.
        self.total_questions: int = 4
        self.finished: bool = False

    @property
    def current_index(self) -> int:
        return len(self.history)


class SessionStore:
    """Basit bellek ici oturum deposu. Gercek bir veritabani degildir,
    sunucu yeniden baslatilinca oturumlar silinir."""

    def __init__(self):
        self._sessions: Dict[str, Session] = {}

    def create(self) -> Session:
        session = Session()
        self._sessions[session.id] = session
        return session

    def get(self, session_id: str) -> Optional[Session]:
        return self._sessions.get(session_id)


store = SessionStore()
