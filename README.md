# AI Interview Simulator

CV'ni ve is ilanini yukleyip Google Gemini API ile kisisellestirilmis, adim adim
zorlasan bir teknik mulakat simulasyonu yasayabilecegin bir web uygulamasi.
Her soruya verdigin cevap puanlanir, eksik noktalar soylenir; sonunda genel
bir skor (orn. 78/100) ve guclu/zayif yon raporu alirsin.

## Ozellikler

- CV (PDF) ve is ilani (PDF veya metin) yukleme
- CV + is ilanina gore kisisellestirilmis, birbirini takip eden teknik sorular
- Her cevap icin 0-100 puan + geri bildirim + eksik nokta tespiti
- Mulakat sonunda genel skor, guclu/zayif yonler ve ozet degerlendirme
- Tamamlanan mulakatlar otomatik olarak gecmise kaydedilir (`backend/data/history.json`)
  ve "📚 Geçmiş Mülakatlarım" ekranindan tekrar goruntulenebilir
- Sonuc raporu tek tikla PDF olarak indirilebilir (Turkce karakter destekli)
- Basit, tek sayfalik web arayuzu

## Kurulum

1. Python 3.10+ kurulu oldugundan emin ol.
2. Bagimliliklari kur:

   ```
   cd ai_interview_simulator/backend
   pip install -r ../requirements.txt
   ```

3. Ucretsiz Gemini API key al: https://aistudio.google.com/apikey
   (Google hesabinla giris yap, "Create API key" de, kredi karti istemez)

4. `ai_interview_simulator/.env.example` dosyasini `.env` olarak kopyala ve
   key'ini yapistir:

   ```
   cp .env.example .env
   ```

   `.env` icinde:
   ```
   GEMINI_API_KEY=senin_api_keyin
   GEMINI_MODEL=gemini-2.5-flash
   ```

   `.env` dosyasi `backend/` klasoru ile ayni seviyede (proje kok klasorunde)
   olmali; `main.py` onu otomatik yukler (`python-dotenv`).

5. Sunucuyu baslat:

   ```
   cd backend
   uvicorn main:app --reload
   ```

6. Tarayicida ac: http://127.0.0.1:8000

## Nasil Calisir

1. **CV ve is ilani yukle** — CV'ni PDF olarak, is ilanini PDF ya da metin
   olarak yukle.
2. **Mulakat basla** — Gemini, CV ve is ilanina gore ilk teknik soruyu uretir.
3. **Cevapla** — Her cevabin puanlanir, geri bildirim alirsin, sonraki soru
   otomatik gelir (toplam 6 soru, `session_store.py` icinde `total_questions`
   degeri ile ayarlanabilir).
4. **Sonuc raporu** — Mulakat bitince genel skor, guclu/zayif yonler ve
   ozet tavsiye gosterilir.

## Proje Yapisi

```
ai_interview_simulator/
  backend/
    main.py            FastAPI uygulamasi ve API endpoint'leri
    gemini_client.py    Gemini API ile soru uretme / degerlendirme
    pdf_utils.py         PDF -> metin cikarma (CV/is ilani okuma)
    pdf_report.py         Sonuc raporunu indirilebilir PDF'e cevirir
    session_store.py     Bellek ici oturum yonetimi (aktif mulakat)
    history_store.py      Tamamlanmis mulakatlarin JSON'a kaydedilmesi
    models.py             Pydantic veri modelleri
    fonts/                PDF'lerde Turkce karakterler icin DejaVu Sans fontu
    data/                 (otomatik olusur) gecmis mulakat kayitlari, git'e girmez
  frontend/
    index.html            Tek sayfalik arayuz
  requirements.txt
  .env.example
```

## API Uc Noktalari (ozet)

- `POST /api/session`, `/api/upload-cv`, `/api/upload-job`, `/api/start`, `/api/answer` — mevcut mulakat akisi
- `GET /api/result/{session_id}` — final raporu getirir (ilk cagrida uretir ve gecmise kaydeder, sonrakilerde kayittan doner)
- `GET /api/history` — tamamlanmis tum mulakatlarin ozet listesi
- `GET /api/history/{id}` — bir kaydin tam raporu
- `GET /api/history/{id}/pdf` — o kaydi PDF olarak indirir

## Onemli Notlar

- Aktif (devam eden) mulakat oturumlari hala bellekte tutulur; sunucu
  yeniden baslatilinca yarim kalmis bir mulakat silinir. Ama **tamamlanmis**
  mulakatlar artik `backend/data/history.json` dosyasina kaydedilir ve
  sunucu yeniden baslasa da kaybolmaz.
- `backend/data/` klasoru kisisel CV/mulakat icerigi barindirdigi icin
  `.gitignore` ile git'e dahil edilmez — GitHub'a pushlarken bu veriler
  paylasilmaz.
- PDF raporlar `backend/fonts/` altindaki DejaVu Sans fontuyla uretilir, bu
  yuzden Turkce karakterler (ı, ş, ğ, ç, ö, ü) PDF'te dogru gorunur; ayrica
  kullanicinin bilgisayarinda ekstra font kurulumu gerekmez.
- Gemini'nin ucretsiz katmani dakikada/gunde belirli sayida istekle
  sinirlidir; yogun test sirasinda "rate limit" hatasi alirsan birkac saniye
  bekleyip tekrar dene. Sonuc ekrani artik kayitli raporu tekrar kullandigi
  icin, sayfayi yenilemek ekstra Gemini istegi harcamaz.
- Gelistirme fikirleri (staj sunumunda "gelecek adimlar" olarak da
  gosterebilirsin): sesli mulakat (Whisper + TTS), coklu is ilani/rol
  secenegi, kullanici hesaplari ve gecmis mulakatlari karsilastirmali
  analitik.
