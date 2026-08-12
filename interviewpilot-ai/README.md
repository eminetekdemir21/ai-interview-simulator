# InterviewPilot AI

Yapay zeka destekli, gercek zamanli mulakat pratik uygulamasi. Kullanicinin CV'sini ve
basvurdugu is ilanini okuyup, secilen sirkete/role ozel teknik mulakat sorulari uretir,
verilen cevaplari puanlar ve mulakat sonunda detayli bir performans raporu (PDF dahil)
cikarir. Google Gemini API kullanir.

## Ozellikler (hepsi gercek, calisan)

- **Coklu kullanici sistemi** — herkes kendi e-posta/sifresiyle kayit olur, giris yapar;
  her kullanicinin CV'si, mulakat gecmisi, istatistikleri ve profili tamamen izole tutulur
- **Sifremi Unuttum / E-posta Dogrulama** — gercek e-posta gonderimiyle (Resend ya da SMTP) calisir:
  sifre sifirlama linki ve 6 haneli dogrulama kodu gercekten mail olarak gonderilir
- **Sirket Bazli Mulakat Modu** — 28 sirket (Google, Amazon, Meta, ASELSAN, Turkcell, ...)
  icin farkli odak alani ve mulakat tarzi baglami
- **Canli mulakat odasi** — CV + is ilanina gore AI'nin urettigi sorular, her cevap icin
  aninda puan + geri bildirim, bir sonraki soruya otomatik gecis
- **Sesli cevap** — mikrofon butonuyla konusarak cevap verilebilir (tarayicinin yerlesik
  konusma tanima ozelligiyle, Chrome/Edge)
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

Daha once JSON dosyalarinda (`users.json`, `history.json`, ...) veri biriktiyse, bunlari
yeni SQLite veritabanina tasimak icin tek seferlik gecis scriptini calistir (guvenlidir,
tekrar calistirilirsa mevcut kayitlarin uzerine yazmaz):

```bash
cd interviewpilot-ai/backend
python migrate_json_to_sqlite.py
```

## Calistirma

```bash
cd interviewpilot-ai/backend
uvicorn main:app --reload --port 8001
```

Tarayicida `http://127.0.0.1:8001` — kayit ol, giris yap, kullanmaya basla.

## Mimari

- **Backend**: FastAPI (Python), tum HTML/CSS/JS dosyalarini da ayni sunucudan servis eder.
  Tum kalici veriler tek bir SQLite veritabaninda (`backend/data/interviewpilot.db`) tutulur:
  kullanicilar (SHA-256 + salt ile hashlenmis sifreler), giris oturumlari, aktif/tamamlanmis
  mulakatlar, yol haritalari ve gunluk meydan okuma gecmisi. Aktif bir mulakat oturumu bile
  her cevaptan sonra veritabanina yazilir; sunucu yeniden baslasa da devam eden bir mulakat
  kaybolmaz. `backend/db.py` baglanti ve sema yonetimini yapar; ekstra bir pip bagimliligi
  eklenmedi (Python'un yerlesik `sqlite3` modulu kullanildi). Eski JSON dosyalarindan
  (`users.json`, `history.json`, ...) gecis icin `backend/migrate_json_to_sqlite.py` scripti
  bir kez calistirilir (bkz. Kurulum).
- **Frontend**: Vanilla HTML/CSS/JS, sayfa gecislerinde `sessionStorage` kullanir.
- **AI**: Google Gemini API (`google-generativeai` SDK). Her cagri ayri bir thread'de calisir
  ve en fazla 25 saniye beklenir; sure asilirsa kullaniciya net bir hata mesaji doner
  (Gemini SDK'sinin kendi ic tekrar deneme mantigi bu sinirlar olmadan cok uzun surebiliyordu).
- **GitHub entegrasyonu**: OAuth gerektirmez, GitHub'in genel (public) REST API'sini
  kullanici adiyla sorgular; ekstra bagimlilik eklememek icin Python'un standart
  `urllib` kutuphanesiyle yazilmistir.

## Internete yayinlama (deploy)

Proje [Render](https://render.com) gibi ucretsiz bir platformda calisacak sekilde hazir
(`render.yaml` ve `Procfile` dahil edildi). Render ile adimlar:

1. [render.com](https://render.com)'da GitHub hesabinla giris yap.
2. **New +** → **Web Service** → `ai-interview-simulator` reponu sec.
3. Render `render.yaml` dosyasini otomatik algilar (yoksa manuel ayarla):
   - Root Directory: `interviewpilot-ai/backend`
   - Build Command: `pip install -r ../requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Environment sekmesinden `GEMINI_API_KEY` degerini kendi key'inle gir (`GEMINI_MODEL` ve
   `COOKIE_SECURE` zaten `render.yaml`'da tanimli).
5. **Deploy** — birkac dakika icinde `https://<proje-adin>.onrender.com` adresinde canli olur.

**Onemli sinir**: Render'in ucretsiz plani dosya sistemini kalici tutmaz — her yeniden
deploy'da (ya da uzun sure inaktif kalip "uyandiginda") `backend/data/interviewpilot.db`
sifirlanir, yani tum kullanicilar ve mulakat gecmisi silinir. Bu, bir portfolyo/demo linki
paylasmak icin sorun degildir, ama gercek kullanicilarin kalici veri biriktirmesini
istiyorsan Render'in ucretli "Persistent Disk" ozelligini eklemen ya da SQLite yerine
harici, kalici bir veritabani (orn. Render'in ucretsiz PostgreSQL'i) kullanman gerekir —
bu proje kapsaminda yapilmadi.

## Bilinen sinirlar

- Aktif mulakat oturumlari bellek ici (sunucu yeniden baslarsa devam eden bir mulakat
  kaybolur, ama tamamlanmis mulakatlar `history.json`'da kalir).
- Basit dosya tabanli depolama (gercek bir veritabani yerine JSON dosyalari) — kucuk
  olcekli/tek makinede calisan bir proje icin yeterli, yuksek trafik icin uygun degil.
- Sesli cevap (mikrofon) tarayicinin yerlesik Web Speech API'sini kullanir; Chrome ve Edge'de
  calisir, Firefox ve Safari'de tarayici destegi kisitli/yok (bu durumda mikrofon butonu
  otomatik olarak devre disi gorunur, metinle cevaplamaya devam edilebilir).
- LinkedIn entegrasyonu yok (gercek OAuth basvurusu/onayi gerektirdigi icin bu proje
  kapsaminda eklenmedi; GitHub genel API'si OAuth gerektirmedigi icin eklendi).
