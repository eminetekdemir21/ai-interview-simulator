from pydantic import BaseModel
from typing import List, Optional


class JobDescriptionIn(BaseModel):
    session_id: str
    job_text: str


class StartInterviewIn(BaseModel):
    session_id: str


class AnswerIn(BaseModel):
    session_id: str
    answer: str


class QAItem(BaseModel):
    question: str
    answer: Optional[str] = None
    score: Optional[int] = None
    feedback: Optional[str] = None


class QuestionOut(BaseModel):
    question: str
    question_number: int
    total_questions: int
    finished: bool = False


class AnswerFeedbackOut(BaseModel):
    score: int
    feedback: str
    missing_points: str
    next_question: Optional[str] = None
    question_number: int
    total_questions: int
    finished: bool


class FinalReportOut(BaseModel):
    overall_score: int
    strengths: List[str]
    weaknesses: List[str]
    summary: str
    history: List[QAItem]
