# InterviewPilot AI — Mobil Uygulama

Bu klasor, InterviewPilot AI'nin gercek bir Android/iOS uygulamasi olarak
calisan halidir (Expo/React Native ile yazildi). Ayni backend'i (Render'daki
canli siteni) kullanir, ayri bir sunucu kurmana gerek yok.

## Onemli: bu kismi kendi bilgisayarinda calistirmalisin

Bu proje burada (Claude'un calisma ortaminda) derlenip telefonda test
edilemiyor — gercek bir emulator/cihaz gerektiriyor. Asagidaki adimlari
**kendi bilgisayarinda** (PowerShell) uygula.

## 1) Backend adresini ayarla

`mobile/src/config.js` dosyasini ac ve `API_BASE_URL` degerini kendi Render
adresinle degistir (sonunda `/` OLMASIN):

```js
export const API_BASE_URL = "https://senin-render-adresin.onrender.com";
```

## 2) Gereksinimler

- [Node.js](https://nodejs.org) (LTS surum) kurulu olmali
- Telefonuna **Expo Go** uygulamasini indir (App Store / Play Store'da ucretsiz)

## 3) Kurulum ve calistirma

PowerShell'de:

```
cd C:\Users\EXCALIBUR\Desktop\ai_interview_simulator\interviewpilot-ai\mobile
npm install
npx expo start
```

Terminalde bir QR kod cikacak:

- **Android**: Expo Go uygulamasini ac, "Scan QR Code" ile bu kodu tarat.
- **iPhone**: Telefonun kendi Kamera uygulamasiyla QR kodu tarat, cikan
  bildirime dokunup Expo Go'da ac.

Telefon ve bilgisayar **ayni Wi-Fi agina** bagli olmali.

Bir seyi degistirdiginde (kod kaydettiginde) uygulama telefonda otomatik
yenilenir, yeniden QR taratmana gerek yok.

## Kapsam (su an neler var)

Web sitesindeki tum ana ozellikler mobilde de mevcut:

- Giris / Kayit Ol
- Dashboard (gercek istatistikler: seri, ortalama skor, toplam mulakat, en
  yuksek skor)
- Yeni Mulakat: CV/is ilani yukleme (PDF), sirket secimi, seviye ve mulakat
  turu secimi
- Canli Mulakat Odasi: soru-cevap dongusu, aninda puan ve geri bildirim
- Sonuc Raporu: genel skor, alt skorlar, guclu/zayif yonler
- Gecmis Mulakatlarim listesi
- Analitik: alt beceri ortalamalari, skor gecmisi, sirket bazinda ortalama
- Yol Haritasi: haftalik plan, gorev tamamlama, yeniden olusturma
- Gunluk Meydan Okuma: gunluk soru, seri takibi
- Portfolyo: GitHub baglama ve AI destekli degerlendirme
- Is Uyumu: CV + is ilani karsilastirma
- CV Analizi: ATS uyumlulugu degerlendirmesi
- AI Kariyer Kocu: sohbet arayuzu
- Profil: ad/hedef rol guncelleme, cikis yap

Dashboard'daki "Tum Ozellikler" butonundan bu ekranlarin tumune ulasilir.

## Android icin direkt kurulabilir APK (Expo Go gerekmez)

Expo Go ile QR kod tarama ugrasmak istemiyorsan, telefona direkt kurulan
gercek bir APK dosyasi olusturabilirsin. Bunun icin ucretsiz bir Expo hesabi
gerekir ([expo.dev](https://expo.dev) uzerinden aninda acilir).

PowerShell'de:

```
cd C:\Users\EXCALIBUR\Desktop\ai_interview_simulator\interviewpilot-ai\mobile
npm install -g eas-cli
eas login
eas build --platform android --profile preview
```

- `eas login` sana bir e-posta/sifre sorar (expo.dev hesabin yoksa terminalde
  hesap olusturma secenegi de cikar).
- `eas build` komutu projeyi Expo'nun bulut sunucularina yukler ve orada
  derler; bu genelde **10-15 dakika** surer, terminalde ilerlemesini
  gorebilirsin.
- Bitince terminalde ve [expo.dev](https://expo.dev/accounts) hesabinin
  "Builds" sekmesinde indirilebilir bir **.apk linki** cikar.
- Bu linki telefonunda ac (ya da bilgisayarda indirip telefona aktar),
  "Bilinmeyen kaynaklardan yukleme" (Unknown sources) iznini ac, kur.
  Artik uygulama normal bir uygulama gibi telefonunda, Expo Go'ya gerek yok.

Kod degistirdiginde (yeni ekran/ozellik eklendiginde) bu APK otomatik
guncellenmez — degisiklik sonrasi `eas build` komutunu tekrar calistirip
yeni APK'yi kurman gerekir.

## iPhone icin

Apple'in kurallari geregi iPhone'da gercek bir kurulum dosyasi (IPA) sadece
ucretli Apple Developer hesabiyla (yillik ~99$) mumkun — bu adim atlanabilir.
Ucretsiz test icin en pratik yol Expo Go: App Store'dan **Expo Go**
uygulamasini indir, `npx expo start` calisirken cikan QR kodu iPhone'un
kendi Kamera uygulamasiyla tarat, cikan bildirime dokun.

## Gercek bir Play Store / App Store yayini

Play Store'a koymak icin `eas build --platform android --profile production`
ile AAB dosyasi olusturulur ve Google Play Console'a (tek seferlik 25$
kayit ucreti) yuklenir. App Store icin Apple Developer hesabi gerekir.
Bu adimlar simdilik kapsam disi, istersen ileride birlikte yapariz.
