import os
import json
import concurrent.futures
import google.generativeai as genai

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

# Gemini SDK'sinin "request_options timeout" ayari bazi durumlarda (ic
# retry/backoff mantigi yuzunden) beklenenden cok daha uzun surebiliyor.
# Bunu kesin olarak sinirlamak icin cagriyi ayri bir thread'de yapip,
# sonucu en fazla TIMEOUT_SECONDS kadar bekliyoruz; sure dolarsa
# (arka plandaki thread hala calisiyor olsa bile) kullaniciya hemen
# net bir hata donduruyoruz.
_executor = concurrent.futures.ThreadPoolExecutor(max_workers=8)
TIMEOUT_SECONDS = 25


def _generate(model, prompt):
    future = _executor.submit(model.generate_content, prompt)
    try:
        return future.result(timeout=TIMEOUT_SECONDS)
    except concurrent.futures.TimeoutError:
        raise TimeoutError(
            f"Gemini istegi {TIMEOUT_SECONDS} saniye icinde tamamlanmadi (deadline exceeded)"
        )


def friendly_error(e: Exception) -> str:
    """Gemini/HTTP hatalarini kullaniciya okunakli Turkce mesaja cevirir."""
    text = str(e)
    lower = text.lower()
    # Teshis icin gercek hatayi terminale yazdir (kullaniciya gosterilen
    # mesaj sadelestirilmis oldugu icin asil sebep burada gorunur).
    print("=" * 60)
    print("[GEMINI HATASI - TAM DETAY]")
    print(repr(e))
    print("=" * 60)
    if "deadline" in lower or "timeout" in lower or "504" in text:
        return (
            "Gemini API zamaninda yanit vermedi (25 saniye icinde). "
            "Sunucu tarafinda gecici bir yavaslama olabilir, lutfen tekrar dene."
        )
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


def _context_block(context: dict | None) -> str:
    """Sirket Bazli Mulakat Modu icin ek baglam metni uretir. context
    None/bos ise genel mod calisir (eski davranisla ayni)."""
    if not context:
        return ""
    lines = ["", "Mulakat Baglami:"]
    if context.get("company_name"):
        lines.append(f"- Hedef sirket: {context['company_name']}")
    if context.get("style_hint"):
        lines.append(f"- Bu sirketin mulakat tarzi: {context['style_hint']}")
    if context.get("role"):
        lines.append(f"- Basvurulan rol: {context['role']}")
    if context.get("difficulty"):
        lines.append(f"- Seviye: {context['difficulty']}")
    if context.get("interview_type"):
        lines.append(f"- Mulakat turu: {context['interview_type']} (buna uygun sorular sor)")
    lines.append("Sorulari yukaridaki sirket tarzina ve seviyeye uygun sekilde uret.")
    return "\n".join(lines)


def generate_next_question(cv_text: str, job_text: str, history, context: dict | None = None) -> str:
    """CV, is ilani, gecmis soru-cevaplar ve (varsa) sirket/rol baglamina
    gore yeni bir teknik mulakat sorusu uretir."""
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
{_context_block(context)}

Simdiye kadarki mulakat gecmisi:
{_history_to_text(history)}

Su ana kadar {len(history)} soru soruldu. Bir sonraki soruyu uret.
Eger gecmiste cevaplar zayifsa o konuyu daha basit sekilde tekrar sorabilir ya da
eksik kalan konuyu derinlestirebilirsin.

Yalnizca su JSON formatinda cevap ver:
{{"question": "<soru metni>"}}
"""
    response = _generate(model, prompt)
    data = json.loads(response.text)
    return data["question"]


def evaluate_answer(question: str, answer: str, job_text: str, context: dict | None = None) -> dict:
    """Verilen cevabi puanlar ve geri bildirim uretir."""
    model = _model(json_mode=True)
    prompt = f"""Sen deneyimli bir teknik mulakat degerlendiricisisin.
Asagidaki soruya adayin verdigi cevabi degerlendir.

Is Ilani (baglam icin):
{job_text[:1500]}
{_context_block(context)}

Soru: {question}
Adayin cevabi: {answer}

Cevabi 0-100 arasi puanla (teknik dogruluk, netlik, derinlik dikkate alinarak).
Kisa ve yapici bir geri bildirim yaz (2-3 cumle).
Eksik kalan veya bahsedilmesi gereken noktalari belirt.

Yalnizca su JSON formatinda cevap ver:
{{"score": <0-100 arasi tam sayi>, "feedback": "<geri bildirim>", "missing_points": "<eksik noktalar>"}}
"""
    response = _generate(model, prompt)
    return json.loads(response.text)


def _stats_block(stats: dict | None) -> str:
    if not stats or not stats.get("total_interviews"):
        return "Aday henuz hic mulakat pratigi tamamlamamis, gecmis performans verisi yok."
    lines = [
        f"- Toplam tamamlanan mulakat: {stats.get('total_interviews')}",
        f"- Ortalama skor: {stats.get('avg_score')}/100",
        f"- En yuksek skor: {stats.get('best_score')}/100",
        f"- Calisma serisi: {stats.get('streak_days')} gun",
    ]
    if stats.get("weakest_topic"):
        lines.append(f"- En sik tekrar eden zayif yon: {stats['weakest_topic']}")
    if stats.get("strongest_topic"):
        lines.append(f"- En sik tekrar eden guclu yon: {stats['strongest_topic']}")
    sub = stats.get("avg_sub_scores") or {}
    if sub:
        lines.append(
            f"- Ortalama alt skorlar: Teknik {sub.get('technical', 0)}, Iletisim {sub.get('communication', 0)}, "
            f"Ozguven {sub.get('confidence', 0)}, Sistem Tasarimi {sub.get('system_design', 0)}"
        )
    return "\n".join(lines)


def career_coach_reply(message: str, chat_history: list, profile: dict | None, stats: dict | None) -> str:
    """Kullanicinin gercek mulakat gecmisini/istatistiklerini baglam olarak
    kullanan, serbest sohbet tarzinda bir kariyer kocu yaniti uretir."""
    model = _model(json_mode=False)
    profile = profile or {}
    convo_lines = []
    for turn in chat_history[-12:]:
        role = "Kullanici" if turn.get("role") == "user" else "Kocu"
        convo_lines.append(f"{role}: {turn.get('text', '')}")
    convo_text = "\n".join(convo_lines) if convo_lines else "(henuz konusma yok)"

    prompt = f"""Sen InterviewPilot AI uygulamasinda calisan, samimi ve destekleyici bir yapay zeka kariyer kocususun.
Kullanicinin gercek mulakat pratigi verilerine gore kisisellestirilmis, somut tavsiyeler veriyorsun.
Kisa (en fazla 4-5 cumle), dogal ve konusma diliyle Turkce yaz. Gereksiz uzun liste yapma, sohbet gibi yaz.

Kullanici profili:
- Isim: {profile.get('name') or 'belirtilmemis'}
- Hedef rol: {profile.get('target_role') or 'belirtilmemis'}

Gercek mulakat istatistikleri:
{_stats_block(stats)}

Simdiye kadarki sohbet:
{convo_text}

Kullanicinin yeni mesaji: {message}

Yukaridaki gercek verilere dayanarak, uydurma rakam veya gerceklesmemis bir olay belirtmeden cevap ver.
Eger istatistik yoksa (henuz mulakat yapmamissa) onu once bir mulakat denemeye tesvik et.
"""
    response = _generate(model, prompt)
    return response.text.strip()


def generate_final_report(cv_text: str, job_text: str, history, context: dict | None = None) -> dict:
    """Tum mulakat gecmisine gore genel bir rapor uretir."""
    model = _model(json_mode=True)
    prompt = f"""Sen bir teknik mulakat degerlendirme raporu hazirlayan yapay zeka asistanisin.
Asagidaki mulakat gecmisine gore adayin genel performansini degerlendir.

Is Ilani:
{job_text[:1500]}
{_context_block(context)}

Mulakat Gecmisi:
{_history_to_text(history)}

Yalnizca su JSON formatinda cevap ver:
{{
  "overall_score": <0-100 arasi tam sayi, tum sorularin ortalamasina yakin ama genel izlenimi de yansitan>,
  "sub_scores": {{
    "technical": <0-100, teknik dogruluk ve derinlik>,
    "communication": <0-100, cevaplarin netligi ve anlatim kalitesi>,
    "confidence": <0-100, cevaplardaki kararlilik/ozguven izlenimi>,
    "system_design": <0-100, buyuk resmi gorme/mimari dusunme becerisi; yeterli veri yoksa makul bir tahmin yap>
  }},
  "strengths": ["<guclu yon 1>", "<guclu yon 2>"],
  "weaknesses": ["<zayif yon 1>", "<zayif yon 2>"],
  "summary": "<2-3 cumlelik genel degerlendirme ve tavsiye>"
}}
"""
    response = _generate(model, prompt)
    return json.loads(response.text)
