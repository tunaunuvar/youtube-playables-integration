# YouTube Playables Preflight Checklist

Her maddeyi `PASS`, `FAIL`, `NEEDS PORTAL` veya `UNVERIFIED` olarak işaretle.
`FAIL` bulunan build'i yayın adayı sayma.

## Paket

- [ ] ZIP kökünde `index.html` var; üst klasör yok.
- [ ] Uygulama SPA ve bütün yollar relative.
- [ ] Dosya adı, file count ve boyut limitleri geçiyor.
- [ ] Bütün oyun verisi, asset ve fontlar bundle içinde.
- [ ] Analytics, remote service ve beklenmeyen external URL yok.
- [ ] Debug/test/staging kodu release'ten çıkarıldı.

## SDK ve lifecycle

- [ ] SDK bütün oyun kodundan önce yükleniyor ve `ytgame` overwrite edilmiyor.
- [ ] `firstFrameReady()` görünür loading/splash üzerinde bir kez çağrılıyor.
- [ ] `gameReady()` yalnız oyun etkileşime hazırken ve bir kez çağrılıyor.
- [ ] Host pause execution/render/audio/input/network'ü tamamen durduruyor.
- [ ] Resume büyük delta veya çift loop üretmiyor.
- [ ] Host audio state'i başlangıçta ve callback ile oyun sesini yönetiyor.

## Veri ve skor

- [ ] Playables progress yalnız cloud save kullanıyor.
- [ ] Başarılı `loadData()` beklenmeden `saveData()` çağrılmıyor.
- [ ] Save schema versioned, validate/migrate ediliyor ve limit altında.
- [ ] Material progress olaylarında save var; exit flush tek güvence değil.
- [ ] Canonical score integer ve saved best ile tutarlı.
- [ ] Kişisel bilgi toplanmıyor; login/account UI yok.

## Oynanış ve tasarım

- [ ] Touch ve mouse ile bütün zorunlu etkileşimler yapılabiliyor.
- [ ] 9:32–32:9, resize ve `0 × 0` → normal senaryosu çalışıyor.
- [ ] Escape modalları kapatıyor ve prevent edilmiyor.
- [ ] Haricî link/paylaşım/exit veya YouTube-lookalike kontrol yok.
- [ ] İngilizce tam; locale yalnız `ytgame.system.getLanguage()` ile alınıyor.
- [ ] WCAG AA hedefleri, audio'suz kullanım ve keyboard akışı test edildi.

## Reklam ve içerik

- [ ] Off-platform monetization, ödeme veya IAP yok.
- [ ] Rewarded ad açık opt-in, stable reward ID ve `true`-only grant kullanıyor.
- [ ] Interstitial yalnız doğal ara noktasında ve ödülsüz.
- [ ] Oyun 13+ general audience; Community Guidelines'a uygun.
- [ ] Bütün IP/müzik/marka/likeness hakları belgeli.
- [ ] Oyun özgün/yetkili ve duplicate/substantially identical değil.
- [ ] Metadata doğru; thumbnail/title/description branding kuralına uygun.

## Doğrulama ve Portal

- [ ] `scripts/validate_playables_bundle.py` son ZIP üzerinde PASS.
- [ ] Test Suite CSP ve tüm lifecycle senaryoları PASS.
- [ ] Desktop web, mobile web, Android ve iOS test edildi.
- [ ] Portal metadata, thumbnail, monetization ve accessibility alanları tamam.
- [ ] Gönderim günü revision history ve canlı İngilizce gereksinimler kontrol edildi.

