# InterviewPilot AI — 8 Günlük Gerçekleştirme Planı

Amaç: Dün tasarlanan InterviewPilot AI arayüzünü (dashboard, şirket bazlı mülakat modu, mülakat odası, rapor) örnek veri yerine gerçek çalışan bir backend'e bağlamak. Var olan `ai_interview_simulator` projesindeki çalışan Gemini AI mantığı temel alınacak.

## Kapsam kararları
- **Giriş sistemi:** Basit, tek kullanıcılı. Gerçek şifre/veritabanı sistemi kurulmayacak — giriş ekranından direkt dashboard'a geçilecek. Bu, projeyi zamanında bitirmek için gereken bir sadeleştirme.
- **Gerçek çalışacak özellikler:** Mülakat akışı (CV+iş ilanı → soru-cevap → puanlama → rapor), şirket bazlı mod (seçilen şirkete göre farklı soru tarzı), dashboard + geçmiş (gerçek kayıtlardan hesaplanan istatistikler).
- **Demo veride kalacaklar:** Liderlik tablosu, topluluk, admin panel, portfolyo/GitHub taraması — bunlar çok kullanıcılı sistem ya da dış servis entegrasyonu gerektirir, kapsam dışı bırakıldı.

## Gün 1 — Backend Temeli
- InterviewPilot AI için ayrı bir FastAPI backend'i kur (mevcut `ai_interview_simulator/backend` mantığından uyarlanarak).
- CV/iş ilanı yükleme, oturum yönetimi, `.env`/Gemini bağlantısı.
- Gecmiş mülakat kaydı (JSON tabanlı, `ai_interview_simulator` projesindeki gibi).

## Gün 2 — Şirket Bazlı Mülakat Modu
- 28 şirket için prompt şablonları (odak alanlarına göre — örn. ASELSAN'a gömülü sistemler, Google'a algoritma/system design sorusu).
- `interview-setup.html`'i gerçek backend'e bağlama (rol/seviye/tür/şirket seçimi → oturum başlatma).

## Gün 3 — Mülakat Odası
- `interview-room.html`'i canlı hale getirme: soru çekme, cevap gönderme, puan/geri bildirim gösterme.
- Statik mock transkript yerine gerçek soru-cevap akışı.

## Gün 4 — Sonuç Raporu
- `report.html`'i gerçek rapor verisiyle doldurma (genel skor, güçlü/zayıf yönler, özet).
- PDF indirme özelliğinin bu projeye taşınması.

## Gün 5 — Dashboard + Geçmiş
- Gerçek tamamlanmış mülakatlardan hesaplanan KPI'lar (ortalama skor, seri, toplam mülakat sayısı).
- Grafiklerin (haftalık skor, radar) gerçek veriyle çalışması.
- `history.html`'in gerçek kayıtları listelemesi.

## Gün 6 — Giriş Akışı ve Profil
- Basit tek kullanıcılı giriş akışının bağlanması (login ekranından dashboard'a).
- `profile.html`'in gerçek kullanıcı/istatistik verisiyle doldurulması.

## Gün 7 — AI Kariyer Koçu (opsiyonel/esnek gün)
- Sohbet ekranının Gemini'ye bağlanması, geçmiş mülakat verisini bağlam olarak kullanması.
- Zaman kalırsa: küçük iyileştirmeler, ekstra cilalama.

## Gün 8 — Test, Hata Ayıklama, Teslim
- Uçtan uca test (tüm akış: yükleme → mülakat → rapor → dashboard → PDF).
- README güncelleme, kurulum talimatları, staj sunumu için özet.

---
*Not: Bu plan esnek — bir gün uzarsa bir sonrakine sarkabilir, önemli olan sırayla ilerlemek.*
