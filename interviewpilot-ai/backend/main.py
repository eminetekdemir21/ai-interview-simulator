import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response

from pydantic import BaseModel

from pdf_utils import extract_text_from_pdf
from session_store import store, QARecord
from companies import get_company
import gemini_client as gc
import history_store
import pdf_report
import profile_store
from models import (
    QuestionOut,
    AnswerIn,
    AnswerFeedbackOut,
    FinalReportOut,
    QAItem,
)

app = FastAPI(title="InterviewPilot AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def no_cache_middleware(request, call_next):
    """Gelistirme asamasinda tarayicinin eski HTML/JS dosyalarini
    onbellekten gostermesini engeller (stale cache sorunlarinin sebebi buydu)."""
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response


def _session_context(session) -> dict:
    """Session'daki sirket/rol/seviye secimlerini gemini_client'in
    bekledigi baglam sozlugune cevirir."""
    return {
        "company_name": session.company_name,
        "style_hint": get_company(session.company_id)["style_hint"] if session.company_id and get_company(session.company_id) else None,
        "role": session.role,
        "difficulty": session.difficulty,
        "interview_type": session.interview_type,
    }


@app.post("/api/session")
def create_session():
    session = store.create()
    return {"session_id": session.id}


@app.post("/api/upload-cv")
async def upload_cv(session_id: str = Form(...), file: UploadFile = File(...)):
    session = store.get(session_id)
    if not session:
        raise HTTPException(404, "Oturum bulunamadi")
    content = await file.read()
    if file.filename.lower().endswith(".pdf"):
        text = extract_text_from_pdf(content)
    else:
        text = content.decode("utf-8", errors="ignore")
    if not text.strip():
        raise HTTPException(400, "PDF'den metin cikarilamadi")
    session.cv_text = text
    return {"cv_preview": text[:500]}


@app.post("/api/upload-job")
async def upload_job(
    session_id: str = Form(...),
    file: UploadFile | None = File(None),
    job_text: str | None = Form(None),
):
    session = store.get(session_id)
    if not session:
        raise HTTPException(404, "Oturum bulunamadi")
    if file is not None:
        content = await file.read()
        if file.filename.lower().endswith(".pdf"):
            text = extract_text_from_pdf(content)
        else:
            text = content.decode("utf-8", errors="ignore")
    elif job_text:
        text = job_text
    else:
        raise HTTPException(400, "Dosya ya da metin gerekli")
    if not text.strip():
        raise HTTPException(400, "Is ilani metni bos")
    session.job_text = text
    return {"job_preview": text[:500]}


@app.post("/api/start", response_model=QuestionOut)
def start_interview(
    session_id: str = Form(...),
    company_id: str | None = Form(None),
    role: str | None = Form(None),
    difficulty: str | None = Form(None),
    interview_type: str | None = Form(None),
    total_questions: int | None = Form(None),
):
    session = store.get(session_id)
    if not session:
        raise HTTPException(404, "Oturum bulunamadi")
    if not session.cv_text or not session.job_text:
        raise HTTPException(400, "Once CV ve is ilani yuklenmeli")

    # Sirket Bazli Mulakat Modu secimleri (hepsi opsiyonel; secilmezse
    # genel/CV+is ilani tabanli mod calisir).
    if company_id:
        company = get_company(company_id)
        if not company:
            raise HTTPException(400, "Gecersiz sirket secimi")
        session.company_id = company_id
        session.company_name = company["name"]
    session.role = role
    session.difficulty = difficulty
    session.interview_type = interview_type
    if total_questions:
        session.total_questions = max(1, min(total_questions, 8))

    try:
        question = gc.generate_next_question(
            session.cv_text, session.job_text, session.history, _session_context(session)
        )
    except Exception as e:
        raise HTTPException(502, gc.friendly_error(e))
    session.history.append(QARecord(question))

    return QuestionOut(
        question=question,
        question_number=session.current_index,
        total_questions=session.total_questions,
        finished=False,
    )


@app.post("/api/answer", response_model=AnswerFeedbackOut)
def submit_answer(payload: AnswerIn):
    session = store.get(payload.session_id)
    if not session:
        raise HTTPException(404, "Oturum bulunamadi")
    if not session.history:
        raise HTTPException(400, "Mulakat henuz baslamadi")

    current = session.history[-1]
    current.answer = payload.answer

    try:
        eval_result = gc.evaluate_answer(current.question, payload.answer, session.job_text, _session_context(session))
    except Exception as e:
        raise HTTPException(502, gc.friendly_error(e))
    current.score = eval_result["score"]
    current.feedback = eval_result["feedback"]
    current.missing_points = eval_result["missing_points"]

    # Onemli: session.current_index history uzunluguna gore dinamik
    # hesaplaniyor; yeni soru eklenmeden ONCE degerini yakalamamiz lazim.
    answered_number = session.current_index
    finished = answered_number >= session.total_questions
    next_question = None

    if finished:
        session.finished = True
    else:
        try:
            next_question = gc.generate_next_question(
                session.cv_text, session.job_text, session.history, _session_context(session)
            )
        except Exception as e:
            raise HTTPException(502, gc.friendly_error(e))
        session.history.append(QARecord(next_question))

    return AnswerFeedbackOut(
        score=current.score,
        feedback=current.feedback,
        missing_points=current.missing_points,
        next_question=next_question,
        question_number=answered_number,
        total_questions=session.total_questions,
        finished=finished,
    )


@app.get("/api/result/{session_id}", response_model=FinalReportOut)
def get_result(session_id: str):
    session = store.get(session_id)
    if not session:
        raise HTTPException(404, "Oturum bulunamadi")
    if not session.finished:
        raise HTTPException(400, "Mulakat henuz tamamlanmadi")

    cached = history_store.get_record(session_id)
    if cached:
        return FinalReportOut(
            overall_score=cached["overall_score"],
            sub_scores=cached.get("sub_scores") or {},
            strengths=cached["strengths"],
            weaknesses=cached["weaknesses"],
            summary=cached["summary"],
            history=[QAItem(**qa) for qa in cached["history"]],
            company_id=cached.get("company_id"),
            company_name=cached.get("company_name"),
            role=cached.get("role"),
            difficulty=cached.get("difficulty"),
            interview_type=cached.get("interview_type"),
        )

    try:
        report = gc.generate_final_report(session.cv_text, session.job_text, session.history, _session_context(session))
    except Exception as e:
        raise HTTPException(502, gc.friendly_error(e))

    history_out = [
        QAItem(question=qa.question, answer=qa.answer, score=qa.score, feedback=qa.feedback)
        for qa in session.history
    ]
    sub_scores = report.get("sub_scores") or {}

    history_store.add_record({
        "id": session_id,
        "overall_score": report["overall_score"],
        "sub_scores": sub_scores,
        "strengths": report["strengths"],
        "weaknesses": report["weaknesses"],
        "summary": report["summary"],
        "history": [qa.model_dump() for qa in history_out],
        "job_preview": session.job_text[:300],
        "company_id": session.company_id,
        "company_name": session.company_name,
        "role": session.role,
        "difficulty": session.difficulty,
        "interview_type": session.interview_type,
    })

    return FinalReportOut(
        overall_score=report["overall_score"],
        sub_scores=sub_scores,
        strengths=report["strengths"],
        weaknesses=report["weaknesses"],
        summary=report["summary"],
        history=history_out,
        company_id=session.company_id,
        company_name=session.company_name,
        role=session.role,
        difficulty=session.difficulty,
        interview_type=session.interview_type,
    )


@app.get("/api/history")
def list_history():
    return history_store.list_records()


@app.get("/api/history/stats")
def get_history_stats():
    """Dashboard KPI'lari icin gercek verilerden hesaplanan ozet."""
    return history_store.stats()


@app.get("/api/history/{item_id}")
def get_history_item(item_id: str):
    record = history_store.get_record(item_id)
    if not record:
        raise HTTPException(404, "Kayit bulunamadi")
    return record


@app.get("/api/history/{item_id}/pdf")
def get_history_pdf(item_id: str):
    record = history_store.get_record(item_id)
    if not record:
        raise HTTPException(404, "Kayit bulunamadi")
    pdf_bytes = pdf_report.build_pdf_bytes(record)
    filename = f"mulakat_raporu_{item_id[:8]}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.get("/api/companies")
def list_companies():
    from companies import COMPANIES
    return [{"id": cid, **data} for cid, data in COMPANIES.items()]


class LoginIn(BaseModel):
    password: str


@app.post("/api/login")
def login(payload: LoginIn):
    expected = os.getenv("AUTH_PASSWORD", "")
    if not expected:
        raise HTTPException(500, ".env dosyasinda AUTH_PASSWORD tanimli degil")
    if payload.password != expected:
        raise HTTPException(401, "Sifre hatali")
    return {"ok": True}


@app.get("/api/profile")
def get_profile():
    return profile_store.get_profile()


class ProfileIn(BaseModel):
    name: str | None = None
    email: str | None = None
    target_role: str | None = None


@app.post("/api/profile")
def update_profile(payload: ProfileIn):
    return profile_store.save_profile(payload.model_dump(exclude_none=True))


# Frontend'i (interviewpilot-ai/ altindaki tum statik sayfalar) sun
frontend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.isdir(frontend_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dir, "assets")), name="assets")

    @app.get("/")
    def serve_index():
        return FileResponse(os.path.join(frontend_dir, "index.html"))

    @app.get("/{page_name}.html")
    def serve_page(page_name: str):
        path = os.path.join(frontend_dir, f"{page_name}.html")
        if os.path.isfile(path):
            return FileResponse(path)
        raise HTTPException(404, "Sayfa bulunamadi")
