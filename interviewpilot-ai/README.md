# InterviewPilot AI

Yapay zeka destekli, gercek zamanli mulakat pratik uygulamasi. Kullanicinin CV'sini ve
basvurdugu is ilanini okuyup, secilen sirkete/role ozel teknik mulakat sorulari uretir,
verilen cevaplari puanlar ve mulakat sonunda detayli bir performans raporu (PDF dahil)
cikarir. Google Gemini API kullanir.

## Ozellikler (hepsi gercek, calisan)

- **Coklu kullanici sistemi** — herkes kendi e-posta/sifresiyle kayit olur, giris yapar;
  her kullanicinin CV'si, mulakat gecmisi, istatistikleri ve profili tamamen izole tutulur
- **Sirket Bazli Mulakat Modu** — 28 sirket (Google, Amazon, Meta, ASELSAN, Turkcell, ...)
  icin farkli odak alani ve mulakat tarzi baglami
- **Canli mulakat odasi** — CV + is ilanina gore AI'nin urettigi sorular, her cevap icin
  aninda puan + geri bildirim, bir sonraki soruya otomatik gecis
- **Sonuc raporu** — genel skor, teknik/iletisim/ozguven/sistem tasarimi alt skorlari,
  guclu/zayif yonler, PDF olarak indirme (Turkce karakter destekli)
- **Dashboard ve Gecmis Mulakatlarim** — gercek mulakat kayitlarindan hesaplanan istatistikler
  (ortalama skor, en yuksek skor, calisma serisi, en sik tekrar eden zayif/guclu yon)
- **CV Analizi** — yuklenen CV'yi ATS uyumlulugu ve icerik kalitesi acisindan degerlendirir
- **Is Uyumu** — CV'yi bir is ilaniyla karsilastirir, gercek uyum skoru + eslesen/eksik
  anahtar kelimeleri cikarir
- **Analitik** — skor trendi, beceri bazli ortalama, mulakat turu dagilimi ve sirket bazli
  ortalama skorlar dahil, tamami gercek mulakat verilerinden hesaplanan grafikler
- **Ogrenme Yol Haritasi** — gercek zayif konulara gore AI'nin urettigi kisisellestirilmis,
  ilerlemesi kaydedilen haftalik ogrenme plani
- **Gunluk Meydan Okuma** — her gun AI'nin urettigi yeni bir mini teknik soru, gercek
  seri (streak) ve haftalik ilerleme takibi
- **Portfolyo** — GitHub kullanici adini baglayarak gercek genel repo verilerinden AI
  destekli portfolyo degerlendirmesi
- **AI Kariyer Kocu** — kullanicinin gercek istatistiklerini baglam alan serbest sohbet

## Kurulum

```bash
cd interviewpilot-ai/backend
pip install -r ../requirements.txt
```

`.env` dosyasini `interviewpilot-ai/backend/.env` olarak olustur (`.env.example`'i kopyala):

```
GEMINI_API_KEY=senin_api_keyin      # https://aistudio.google.com/apikey
GEMINI_MODEL=gemini-3.5-flash-lite  # Gemini 3 ailesi onerilir (2.0/2.5 modelleri kaldirildi)
```

## Calistirma

```bash
cd interviewpilot-ai/backend
uvicorn main:app --reload --port 8001
```

Tarayicida `http://127.0.0.1:8001` — kayit ol, giris yap, kullanmaya basla.

## Mimari

- **Backend**: FastAPI (Python), tum HTML/CSS/JS dosyalarini da ayni sunucudan servis eder.
  Oturumlar (`session_store.py`) bellek ici tutulur; kimlik dogrulama httpOnly cerez
  (`auth.py`) ile yapilir. Kalici veriler basit JSON dosyalarinda tutulur (gercek bir
  veritabani degil, proje kapsami icin yeterli): `backend/data/users.json` (hesaplar,
  SHA-256 + salt ile hashlenmis sifreler), `backend/data/history.json` (tamamlanmis
  mulakatlar, kullaniciya gore izole), `backend/data/roadmap.json` (yol haritalari),
  `backend/data/challenges.json` (gunluk meydan okuma gecmisi).
- **Frontend**: Vanilla HTML/CSS/JS, sayfa gecislerinde `sessionStorage` kullanir.
- **AI**: Google Gemini API (`google-generativeai` SDK). Her cagri ayri bir thread'de calisir
  ve en fazla 25 saniye beklenir; sure asilirsa kullaniciya net bir hata mesaji doner
  (Gemini SDK'sinin kendi ic tekrar deneme mantigi bu sinirlar olmadan cok uzun surebiliyordu).
- **GitHub entegrasyonu**: OAuth gerektirmez, GitHub'in genel (public) REST API'sini
  kullanici adiyla sorgular; ekstra bagimlilik eklememek icin Python'un standart
  `urllib` kutuphanesiyle yazilmistir.

## Bilinen sinirlar

- Aktif mulakat oturumlari bellek ici (sunucu yeniden baslarsa devam eden bir mulakat
  kaybolur, ama tamamlanmis mulakatlar `history.json`'da kalir).
- Basit dosya tabanli depolama (gercek bir veritabani yerine JSON dosyalari) — kucuk
  olcekli/tek makinede calisan bir proje icin yeterli, yuksek trafik icin uygun degil.
- Sesli mulakat modu arayuzde gorunur ama pasif (sadece metin tabanli cevap destekleniyor).
- LinkedIn entegrasyonu yok (OAuth gerektirdigi icin bu proje kapsaminda eklenmedi).
