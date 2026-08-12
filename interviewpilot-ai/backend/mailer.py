"""Gercek e-posta gonderimi icin kucuk bir yardimci. Ekstra bir pip
bagimliligi eklememek icin Python'un yerlesik kutuphaneleri kullanir.
Iki yontemi destekler:

1. Resend (onerilen, kurulumu kolay) — RESEND_API_KEY ayarlanmissa
   Resend'in HTTP API'si (urllib ile) kullanilir. 2FA/uygulama sifresi
   gerektirmez, sadece resend.com'da hesap acip bir API key almak yeterli.
2. SMTP (orn. Gmail App Password) — RESEND_API_KEY yoksa ama SMTP_HOST/
   SMTP_USER/SMTP_PASSWORD varsa smtplib ile gonderilir.

Hicbiri ayarlanmamissa MailerNotConfigured firlatilir — cagiran taraf
bunu yakalayip kullaniciya anlamli bir mesaj gosterir."""
import json
import os
import smtplib
import urllib.error
import urllib.request
from email.mime.text import MIMEText


class MailerNotConfigured(Exception):
    pass


def _send_via_resend(to_email: str, subject: str, body_text: str, api_key: str):
    from_addr = os.getenv("RESEND_FROM") or "onboarding@resend.dev"
    payload = json.dumps({
        "from": from_addr,
        "to": [to_email],
        "subject": subject,
        "text": body_text,
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            resp.read()
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Resend e-posta gonderimi basarisiz ({e.code}): {detail}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Resend'e baglanilamadi: {e}")


def _send_via_smtp(to_email: str, subject: str, body_text: str):
    host = os.getenv("SMTP_HOST")
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")
    port = int(os.getenv("SMTP_PORT", "587"))
    from_addr = os.getenv("SMTP_FROM") or user

    msg = MIMEText(body_text, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_email

    with smtplib.SMTP(host, port, timeout=15) as server:
        server.starttls()
        server.login(user, password)
        server.sendmail(from_addr, [to_email], msg.as_string())


def send_email(to_email: str, subject: str, body_text: str):
    resend_key = os.getenv("RESEND_API_KEY")
    if resend_key:
        _send_via_resend(to_email, subject, body_text, resend_key)
        return

    smtp_configured = os.getenv("SMTP_HOST") and os.getenv("SMTP_USER") and os.getenv("SMTP_PASSWORD")
    if smtp_configured:
        _send_via_smtp(to_email, subject, body_text)
        return

    raise MailerNotConfigured(
        "E-posta gonderimi yapilandirilmamis (.env dosyasina RESEND_API_KEY "
        "ya da SMTP_HOST/SMTP_USER/SMTP_PASSWORD ekle)"
    )


def send_password_reset(to_email: str, reset_url: str):
    send_email(
        to_email,
        "InterviewPilot AI - Sifre Sifirlama",
        f"Sifreni sifirlamak icin asagidaki linke tikla (30 dakika gecerlidir):\n\n{reset_url}\n\n"
        "Bu talebi sen yapmadiysan bu e-postayi yok sayabilirsin.",
    )


def send_verification_code(to_email: str, code: str):
    send_email(
        to_email,
        "InterviewPilot AI - E-posta Dogrulama Kodu",
        f"E-postani dogrulamak icin kodun: {code}\n\nBu kod 15 dakika gecerlidir.",
    )
