"""Gercek e-posta gonderimi icin kucuk bir yardimci. Ekstra bir pip
bagimliligi eklememek icin Python'un yerlesik smtplib/email kutuphanelerini
kullanir. Herhangi bir SMTP saglayicisiyla calisir (Gmail App Password ile
test edilmistir, bkz. README).

Ortam degiskenleri ayarlanmamissa (SMTP_HOST/SMTP_USER/SMTP_PASSWORD),
e-posta gonderilemez ve MailerNotConfigured firlatilir — cagiran taraf
bunu yakalayip kullaniciya anlamli bir mesaj gosterir."""
import os
import smtplib
from email.mime.text import MIMEText


class MailerNotConfigured(Exception):
    pass


def _config():
    host = os.getenv("SMTP_HOST")
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")
    if not host or not user or not password:
        raise MailerNotConfigured(
            "E-posta gonderimi yapilandirilmamis (.env dosyasina SMTP_HOST, "
            "SMTP_USER, SMTP_PASSWORD ekle)"
        )
    return {
        "host": host,
        "port": int(os.getenv("SMTP_PORT", "587")),
        "user": user,
        "password": password,
        "from": os.getenv("SMTP_FROM") or user,
    }


def send_email(to_email: str, subject: str, body_text: str):
    cfg = _config()
    msg = MIMEText(body_text, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = cfg["from"]
    msg["To"] = to_email

    with smtplib.SMTP(cfg["host"], cfg["port"], timeout=15) as server:
        server.starttls()
        server.login(cfg["user"], cfg["password"])
        server.sendmail(cfg["from"], [to_email], msg.as_string())


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
