# InterviewPilot AI

Yapay zeka destekli, gercek zamanli mulakat pratik uygulamasi. Kullanicinin CV'sini ve
basvurdugu is ilanini okuyup, secilen sirkete/role ozel teknik mulakat sorulari uretir,
verilen cevaplari puanlar ve mulakat sonunda detayli bir performans raporu (PDF dahil)
cikarir. Google Gemini API kullanir.

## Ozellikler (gercek, calisan)

- **Sirket Bazli Mulakat Modu** — 28 sirket (Google, Amazon, Meta, ASELSAN, Turkcell, ...)
  icin farkli odak alani ve mulakat tarzi baglami
- **Canli mulakat odasi** — CV + is ilanina gore AI'nin urettigi sorular, her cevap icin
  aninda puan + geri bildirim, bir sonraki soruya otomatik gecis
- **Sonuc raporu** — genel skor, teknik/iletisim/ozguven/sistem tasarimi alt skorlari,
  guclu/zayif yonler, PDF olarak indirme (Turkce karakter destekli)
- **Dashboard ve Gecmis Mulakatlarim** — gercek mulakat kayitlarindan hesaplanan istatistikler
  (ortalama skor, en yuksek skor, calisma serisi, en sik tekrar eden zayif/guclu yon)
- **AI Kariyer Kocu** — kullanicinin gercek istatistiklerini baglam alan serbest sohbet
- **Basit tek kullanicili giris** — sifre korumali erisim, duzenlenebilir profil

> Not: `resume-analysis.html`, `job-match.html`, `portfolio.html`, `challenges.html`,
> `roadmap.html`, `analytics.html` sayfalari su an gercek backend'e baglanma asamasinda
> (bkz. proje ilerleme notlari). `leaderboard.html` ve `admin.html` kaldirildi — tek
> kullanicili bir uygulamada anlamli degillerdi.

## Kurulum

```bash
cd interviewpilot-ai/backend
pip install -r ../requirements.txt
```

`.env` dosyasini `interviewpilot-ai/backend/.env` olarak olustur (`.env.example`'i kopyala):

```
GEMINI_API_KEY=senin_api_keyin      # https://aistudio.google.com/apikey
GEMINI_MODEL=gemini-3.5-flash-lite  # Gemini 3 ailesi onerilir (2.0/2.5 modelleri kaldirildi)
AUTH_PASSWORD=giris_sifren
```

## Calistirma

```bash
cd interviewpilot-ai/backend
uvicorn main:app --reload --port 8001
```

Tarayicida `http://127.0.0.1:8001` — giris sifresiyle icere gir.

## Mimari

- **Backend**: FastAPI (Python), tum HTML/CSS/JS dosyalarini da ayni sunucudan servis eder.
  Oturumlar (`session_store.py`) bellek ici tutulur, sunucu yeniden baslatilinca sifirlanir.
  Tamamlanmis mulakatlar `backend/data/history.json`, profil bilgisi `backend/data/profile.json`
  dosyasinda kalici olarak saklanir (gercek bir veritabani degil, tek kullanicili proje icin
  yeterli basit bir dosya deposu).
- **Frontend**: Vanilla HTML/CSS/JS, sayfa gecislerinde `sessionStorage` kullanir.
- **AI**: Google Gemini API (`google-generativeai` SDK). Her cagri ayri bir thread'de calisir
  ve en fazla 25 saniye beklenir; sure asilirsa kullaniciya net bir hata mesaji doner
  (Gemini SDK'sinin kendi ic tekrar deneme mantigi bu sinirlar olmadan cok uzun surebiliyordu).

## Bilinen sinirlar

- Tek kullanicili basit sifre korumasi; coklu kullanici/gercek kimlik dogrulama yok.
- Oturumlar bellek ici (sunucu yeniden baslarsa devam eden bir mulakat kaybolur, ama
  tamamlanmis mulakatlar `history.json`'da kalir).
- Sesli mulakat modu arayuzde gorunur ama pasif (sadece metin tabanli cevap destekleniyor).
