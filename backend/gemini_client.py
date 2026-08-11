import os
import json
import google.generativeai as genai

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")


def friendly_error(e: Exception) -> str:
    """Gemini/HTTP hatalarini kullaniciya okunakli Turkce mesaja cevirir."""
    text = str(e)
    lower = text.lower()
    if "resource_exhausted" in lower or "429" in text or "quota" in lower:
        return (
            "Gemini API gunluk/dakikalik kullanim limitine ulasildi. "
            "Birkac dakika (kotaya gore bazen 24 saate kadar) bekleyip tekrar dene, "
            "ya da .env dosyasindaki GEMINI_MODEL degerini farkli bir modelle degistir."
        )
    if "api key not valid" in lower or "invalid api key" in lower or "permission" in lower:
        return "Gemini API key gecersiz gorunuyor. .env dosyasindaki GEMINI_API_KEY degerini kontrol et."
    if "json" in lower and ("expecting value" in lower or "decode" in lower):
        return "Yapay zekadan gelen yanit beklenmedik formattaydi, lutfen tekrar dene."
    return f"Yapay zeka servisinde beklenmeyen bir hata olustu: {text[:200]}"

_configured = False


def _ensure_configured():
    global _configured
    if _configured:
        return
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY bulunamadi. .env dosyasina key'ini ekle "
            "(bkz. .env.example)."
        )
    genai.configure(api_key=api_key)
    _configured = True


def _model(json_mode: bool = True):
    _ensure_configured()
    generation_config = {}
    if json_mode:
        generation_config["response_mime_type"] = "application/json"
    return genai.GenerativeModel(
        GEMINI_MODEL, generation_config=generation_config
    )


def _history_to_text(history) -> str:
    if not history:
        return "(henuz soru sorulmadi)"
    lines = []
    for i, qa in enumerate(history, 1):
        lines.append(f"Soru {i}: {qa.question}")
        if qa.answer:
            lines.append(f"Cevap {i}: {qa.answer}")
        if qa.score is not None:
            lines.append(f"Puan {i}: {qa.score}/100 - {qa.feedback}")
    return "\n".join(lines)


def generate_next_question(cv_text: str, job_text: str, history) -> str:
    """CV, is ilani ve gecmis soru-cevaplara gore yeni bir teknik mulakat
    sorusu uretir."""
    model = _model(json_mode=True)
    prompt = f"""Sen deneyimli bir teknik mulakat yapan (interviewer) yapay zeka asistanisin.
Adayin CV'sine ve basvurdugu is ilanina gore ona teknik mulakat sorulari soruyorsun.
Sorular; is ilanindaki gereksinimlere, adayin CV'sindeki deneyimlere uygun ve
kademeli olarak derinlesen (onceki cevaba gore takip sorusu da olabilir) sorular olmali.
Sadece TEK bir soru uret, aciklama ekleme.

CV:
{cv_text[:4000]}

Is Ilani:
{job_text[:2000]}

Simdiye kadarki mulakat gecmisi:
{_history_to_text(history)}

Su ana kadar {len(history)} soru soruldu. Bir sonraki soruyu uret.
Eger gecmiste cevaplar zayifsa o konuyu daha basit sekilde tekrar sorabilir ya da
eksik kalan konuyu derinlestirebilirsin.

Yalnizca su JSON formatinda cevap ver:
{{"question": "<soru metni>"}}
"""
    response = model.generate_content(prompt)
    data = json.loads(response.text)
    return data["question"]


def evaluate_answer(question: str, answer: str, job_text: str) -> dict:
    """Verilen cevabi puanlar ve geri bildirim uretir."""
    model = _model(json_mode=True)
    prompt = f"""Sen deneyimli bir teknik mulakat degerlendiricisisin.
Asagidaki soruya adayin verdigi cevabi degerlendir.

Is Ilani (baglam icin):
{job_text[:1500]}

Soru: {question}
Adayin cevabi: {answer}

Cevabi 0-100 arasi puanla (teknik dogruluk, netlik, derinlik dikkate alinarak).
Kisa ve yapici bir geri bildirim yaz (2-3 cumle).
Eksik kalan veya bahsedilmesi gereken noktalari belirt.

Yalnizca su JSON formatinda cevap ver:
{{"score": <0-100 arasi tam sayi>, "feedback": "<geri bildirim>", "missing_points": "<eksik noktalar>"}}
"""
    response = model.generate_content(prompt)
    return json.loads(response.text)


def generate_final_report(cv_text: str, job_text: str, history) -> dict:
    """Tum mulakat gecmisine gore genel bir rapor uretir."""
    model = _model(json_mode=True)
    prompt = f"""Sen bir teknik mulakat degerlendirme raporu hazirlayan yapay zeka asistanisin.
Asagidaki mulakat gecmisine gore adayin genel performansini degerlendir.

Is Ilani:
{job_text[:1500]}

Mulakat Gecmisi:
{_history_to_text(history)}

Yalnizca su JSON formatinda cevap ver:
{{
  "overall_score": <0-100 arasi tam sayi, tum sorularin ortalamasina yakin ama genel izlenimi de yansitan>,
  "strengths": ["<guclu yon 1>", "<guclu yon 2>"],
  "weaknesses": ["<zayif yon 1>", "<zayif yon 2>"],
  "summary": "<2-3 cumlelik genel degerlendirme ve tavsiye>"
}}
"""
    response = model.generate_content(prompt)
    return json.loads(response.text)
