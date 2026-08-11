import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import Depends, FastAPI, UploadFile, File, Form, HTTPException, Request, Response as FastAPIResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response

from pydantic import BaseModel

from pdf_utils import extract_text_from_pdf
from session_store import store, QARecord
from companies import get_company
import auth
import gemini_client as gc
import history_store
import pdf_report
import roadmap_store
import challenge_store
import github_client
import user_store
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
def create_session(user: dict = Depends(auth.get_current_user)):
    session = store.create(user_id=user["id"])
    return {"session_id": session.id}


@app.post("/api/upload-cv")
async def upload_cv(session_id: str = Form(...), file: UploadFile = File(...), user: dict = Depends(auth.get_current_user)):
    session = store.get(session_id)
    if not session or session.user_id != user["id"]:
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
    user: dict = Depends(auth.get_current_user),
):
    session = store.get(session_id)
    if not session or session.user_id != user["id"]:
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
    user: dict = Depends(auth.get_current_user),
):
    session = store.get(session_id)
    if not session or session.user_id != user["id"]:
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
def submit_answer(payload: AnswerIn, user: dict = Depends(auth.get_current_user)):
    session = store.get(payload.session_id)
    if not session or session.user_id != user["id"]:
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
def get_result(session_id: str, user: dict = Depends(auth.get_current_user)):
    session = store.get(session_id)
    if not session or session.user_id != user["id"]:
        raise HTTPException(404, "Oturum bulunamadi")
    if not session.finished:
        raise HTTPException(400, "Mulakat henuz tamamlanmadi")

    cached = history_store.get_record(session_id, user_id=user["id"])
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
        "user_id": user["id"],
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
def list_history(user: dict = Depends(auth.get_current_user)):
    return history_store.list_records(user_id=user["id"])


@app.get("/api/history/stats")
def get_history_stats(user: dict = Depends(auth.get_current_user)):
    """Dashboard KPI'lari icin gercek verilerden hesaplanan ozet."""
    return history_store.stats(user_id=user["id"])


@app.get("/api/history/{item_id}")
def get_history_item(item_id: str, user: dict = Depends(auth.get_current_user)):
    record = history_store.get_record(item_id, user_id=user["id"])
    if not record:
        raise HTTPException(404, "Kayit bulunamadi")
    return record


@app.get("/api/history/{item_id}/pdf")
def get_history_pdf(item_id: str, user: dict = Depends(auth.get_current_user)):
    record = history_store.get_record(item_id, user_id=user["id"])
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


COOKIE_MAX_AGE = 60 * 60 * 24 * 30  # 30 gun


def _set_session_cookie(response: FastAPIResponse, user_id: str):
    token = auth.create_session(user_id)
    response.set_cookie(
        auth.COOKIE_NAME, token,
        httponly=True, samesite="lax", max_age=COOKIE_MAX_AGE,
    )


class RegisterIn(BaseModel):
    name: str
    email: str
    password: str


@app.post("/api/register")
def register(payload: RegisterIn, response: FastAPIResponse):
    try:
        user = user_store.create_user(payload.email, payload.password, payload.name)
    except ValueError as e:
        raise HTTPException(400, str(e))
    _set_session_cookie(response, user["id"])
    return user_store.public_user(user)


class LoginIn(BaseModel):
    email: str
    password: str


@app.post("/api/login")
def login(payload: LoginIn, response: FastAPIResponse):
    user = user_store.verify_login(payload.email, payload.password)
    if not user:
        raise HTTPException(401, "E-posta veya sifre hatali")
    _set_session_cookie(response, user["id"])
    return user_store.public_user(user)


@app.post("/api/logout")
def logout(request: Request, response: FastAPIResponse):
    auth.destroy_session(request.cookies.get(auth.COOKIE_NAME))
    response.delete_cookie(auth.COOKIE_NAME)
    return {"ok": True}


@app.get("/api/me")
def me(user: dict = Depends(auth.get_current_user)):
    return user_store.public_user(user)


@app.get("/api/profile")
def get_profile(user: dict = Depends(auth.get_current_user)):
    return user_store.public_user(user)


class ProfileIn(BaseModel):
    name: str | None = None
    target_role: str | None = None


@app.post("/api/profile")
def update_profile(payload: ProfileIn, user: dict = Depends(auth.get_current_user)):
    updated = user_store.update_user(user["id"], payload.model_dump(exclude_none=True))
    return user_store.public_user(updated)


class ChatTurn(BaseModel):
    role: str
    text: str


class CoachIn(BaseModel):
    message: str
    history: list[ChatTurn] = []


@app.post("/api/cv-analysis")
async def cv_analysis(file: UploadFile = File(...)):
    content = await file.read()
    if file.filename.lower().endswith(".pdf"):
        text = extract_text_from_pdf(content)
    else:
        text = content.decode("utf-8", errors="ignore")
    if not text.strip():
        raise HTTPException(400, "CV'den metin cikarilamadi (PDF taranmis bir goruntu olabilir)")
    try:
        result = gc.analyze_cv(text)
    except Exception as e:
        raise HTTPException(502, gc.friendly_error(e))
    result["filename"] = file.filename
    return result


@app.post("/api/job-match")
async def job_match(file: UploadFile = File(...), job_text: str = Form(...)):
    content = await file.read()
    if file.filename.lower().endswith(".pdf"):
        cv_text = extract_text_from_pdf(content)
    else:
        cv_text = content.decode("utf-8", errors="ignore")
    if not cv_text.strip():
        raise HTTPException(400, "CV'den metin cikarilamadi (PDF taranmis bir goruntu olabilir)")
    if not job_text.strip():
        raise HTTPException(400, "Is ilani metni bos olamaz")
    try:
        result = gc.analyze_job_match(cv_text, job_text)
    except Exception as e:
        raise HTTPException(502, gc.friendly_error(e))
    return result


@app.post("/api/coach")
def coach_chat(payload: CoachIn, user: dict = Depends(auth.get_current_user)):
    profile = user_store.public_user(user)
    stats = history_store.stats(user_id=user["id"])
    chat_history = [t.model_dump() for t in payload.history]
    try:
        reply = gc.career_coach_reply(payload.message, chat_history, profile, stats)
    except Exception as e:
        raise HTTPException(502, gc.friendly_error(e))
    return {"reply": reply}


@app.get("/api/roadmap")
def get_roadmap(user: dict = Depends(auth.get_current_user)):
    stats = history_store.stats(user_id=user["id"])
    if not stats.get("total_interviews"):
        raise HTTPException(400, "Yol haritasi olusturmak icin once en az bir mulakat tamamlamalisin")
    existing = roadmap_store.get_roadmap(user["id"])
    if existing:
        return existing
    try:
        generated = gc.generate_roadmap(stats)
    except Exception as e:
        raise HTTPException(502, gc.friendly_error(e))
    return roadmap_store.save_roadmap(user["id"], generated)


@app.post("/api/roadmap/regenerate")
def regenerate_roadmap(user: dict = Depends(auth.get_current_user)):
    stats = history_store.stats(user_id=user["id"])
    if not stats.get("total_interviews"):
        raise HTTPException(400, "Yol haritasi olusturmak icin once en az bir mulakat tamamlamalisin")
    try:
        generated = gc.generate_roadmap(stats)
    except Exception as e:
        raise HTTPException(502, gc.friendly_error(e))
    return roadmap_store.save_roadmap(user["id"], generated)


class RoadmapToggleIn(BaseModel):
    week_index: int
    task_index: int


@app.post("/api/roadmap/toggle")
def toggle_roadmap_task(payload: RoadmapToggleIn, user: dict = Depends(auth.get_current_user)):
    roadmap = roadmap_store.toggle_task(user["id"], payload.week_index, payload.task_index)
    if not roadmap:
        raise HTTPException(404, "Yol haritasi veya gorev bulunamadi")
    return roadmap


@app.get("/api/challenge/today")
def get_today_challenge(user: dict = Depends(auth.get_current_user)):
    existing = challenge_store.get_today(user["id"])
    if existing:
        return existing
    stats = history_store.stats(user_id=user["id"])
    try:
        generated = gc.generate_daily_challenge(stats)
    except Exception as e:
        raise HTTPException(502, gc.friendly_error(e))
    return challenge_store.create_today(user["id"], generated["question"])


class ChallengeAnswerIn(BaseModel):
    answer: str


@app.post("/api/challenge/answer")
def answer_today_challenge(payload: ChallengeAnswerIn, user: dict = Depends(auth.get_current_user)):
    today = challenge_store.get_today(user["id"])
    if not today:
        raise HTTPException(400, "Once bugunun sorusunu getir")
    if today.get("completed"):
        raise HTTPException(400, "Bugunun sorusu zaten cevaplandi")
    if not payload.answer.strip():
        raise HTTPException(400, "Cevap bos olamaz")
    try:
        result = gc.evaluate_challenge_answer(today["question"], payload.answer)
    except Exception as e:
        raise HTTPException(502, gc.friendly_error(e))
    record = challenge_store.submit_answer(user["id"], payload.answer, result.get("score", 0), result.get("feedback", ""))
    return record


@app.get("/api/challenge/stats")
def get_challenge_stats(user: dict = Depends(auth.get_current_user)):
    return challenge_store.compute_stats(user["id"])


class GithubConnectIn(BaseModel):
    username: str


@app.post("/api/portfolio/github")
def connect_github(payload: GithubConnectIn, user: dict = Depends(auth.get_current_user)):
    username = payload.username.strip().lstrip("@")
    if not username:
        raise HTTPException(400, "GitHub kullanici adi bos olamaz")
    try:
        profile = github_client.fetch_profile(username)
        repos = github_client.fetch_repos(username)
    except ValueError as e:
        raise HTTPException(404, str(e))
    user_store.update_user(user["id"], {"github_username": username})
    try:
        analysis = gc.analyze_github_profile(profile, repos)
    except Exception as e:
        raise HTTPException(502, gc.friendly_error(e))
    return {"profile": profile, "repos": repos, "analysis": analysis}


@app.get("/api/portfolio")
def get_portfolio(user: dict = Depends(auth.get_current_user)):
    username = (user.get("github_username") or "").strip()
    if not username:
        raise HTTPException(400, "Henuz bir GitHub hesabi baglanmadi")
    try:
        profile = github_client.fetch_profile(username)
        repos = github_client.fetch_repos(username)
    except ValueError as e:
        raise HTTPException(404, str(e))
    try:
        analysis = gc.analyze_github_profile(profile, repos)
    except Exception as e:
        raise HTTPException(502, gc.friendly_error(e))
    return {"profile": profile, "repos": repos, "analysis": analysis}


@app.post("/api/portfolio/disconnect")
def disconnect_github(user: dict = Depends(auth.get_current_user)):
    user_store.update_user(user["id"], {"github_username": ""})
    return {"ok": True}


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
