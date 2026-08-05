import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from pdf_utils import extract_text_from_pdf
from session_store import store, QARecord
import gemini_client as gc
from models import (
    QuestionOut,
    AnswerIn,
    AnswerFeedbackOut,
    FinalReportOut,
    QAItem,
)

app = FastAPI(title="AI Interview Simulator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


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
def start_interview(session_id: str = Form(...)):
    session = store.get(session_id)
    if not session:
        raise HTTPException(404, "Oturum bulunamadi")
    if not session.cv_text or not session.job_text:
        raise HTTPException(400, "Once CV ve is ilani yuklenmeli")

    try:
        question = gc.generate_next_question(session.cv_text, session.job_text, session.history)
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
        eval_result = gc.evaluate_answer(current.question, payload.answer, session.job_text)
    except Exception as e:
        raise HTTPException(502, gc.friendly_error(e))
    current.score = eval_result["score"]
    current.feedback = eval_result["feedback"]
    current.missing_points = eval_result["missing_points"]

    # Onemli: session.current_index, history uzunluguna gore dinamik hesaplaniyor.
    # Asagida yeni soru history'ye eklenmeden ONCE degerini yakalamamiz lazim,
    # yoksa "cevaplanan soru numarasi" yanlislikla bir sonraki sorunun
    # numarasi olur (frontend +1 daha ekleyince soru 1'den 3'e atlar).
    answered_number = session.current_index
    finished = answered_number >= session.total_questions
    next_question = None

    if finished:
        session.finished = True
    else:
        try:
            next_question = gc.generate_next_question(session.cv_text, session.job_text, session.history)
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

    try:
        report = gc.generate_final_report(session.cv_text, session.job_text, session.history)
    except Exception as e:
        raise HTTPException(502, gc.friendly_error(e))

    history_out = [
        QAItem(question=qa.question, answer=qa.answer, score=qa.score, feedback=qa.feedback)
        for qa in session.history
    ]

    return FinalReportOut(
        overall_score=report["overall_score"],
        strengths=report["strengths"],
        weaknesses=report["weaknesses"],
        summary=report["summary"],
        history=history_out,
    )


# Frontend'i sun
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.isdir(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    @app.get("/")
    def serve_index():
        return FileResponse(os.path.join(frontend_dir, "index.html"))
