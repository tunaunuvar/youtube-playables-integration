# Release ve Sertifikasyon Akışı

## 1. Erişim ve Portal

Developer Portal şu anda private preview/invitation-only olabilir. Davet, uygun
YouTube channel erişimi ve gerekli channel manager yetkileri yayın sürecinden
önce doğrulanmalıdır. Portal erişimi olmadan teknik bundle hazırlanabilir ama
yayın sonucu garanti edilemez.

## 2. Release paketi

- Temiz production build üret; debug menüleri, test ads, devtools, source server
  bağımlılıkları ve gizli staging URL'lerini çıkar.
- ZIP kökünde `index.html` bulunmalı; fazladan üst klasör olmamalı.
- Bütün dosya yolları relative olmalı ve yalnız alfanümerik, `_`, `-`, `.`
  karakterleri kullanılmalı.
- Paket sınırları: initial bundle `<30 MiB` (hedef `<15 MiB`), toplam `<250 MiB`,
  her dosya `<30 MiB` (hedef `<512 KiB`), en fazla 8000 dosya.
- Save `<3 MiB`, tercihen `<500 KiB`; beklenen loading süresi 5 saniyenin altında
  ve JS heap en fazla 512 MB olmalı.
- Repo validator'ını hem klasör hem son ZIP üzerinde çalıştır. Initial transfer,
  runtime heap ve davranış kontrollerini ayrıca ölç.

## 3. Test Suite ve cihaz testi

Yerel release'i HTTP ile serve ettikten sonra doğrudan
[resmî Playables Test Suite'i](https://developers.google.com/youtube/gaming/playables/test_suite)
aç ve çalışan localhost URL'sini test et. Ayrıntılı kurulum ve sıralama için
[setup-and-testing.md](setup-and-testing.md) dosyasını uygula.

Resmî Test Suite ile en az şunları kontrol et:

- SDK load/order, lifecycle, audio, pause/resume, save/load ve score.
- CSP altında dynamic script/worker/font/asset davranışı. Dynamic script
  üretiliyorsa Test Suite'in verdiği nonce'u devral.
- Desktop web, mobile web, Android YouTube ve iOS YouTube.
- İlk kurulum, bozuk/eski save migration, offline/network hata yolları, ad cancel
  ve uygulamanın arka plana gidip dönmesi.
- `0 × 0` başlangıç WebView'i ve sonraki resize.

Test CSP'sinin güncel metnini dokümandan al; sabit bir kopyayı sonsuza kadar
doğru kabul etme.

## 4. İçerik, haklar ve gizlilik kontrolü

- Oyun Community Guidelines'a uymalı, 13+ genel kitle için tasarlanmalı ve
  “made for kids” olmamalı.
- Kod, isim, marka, müzik, ses, görsel ve kişilik hakları için yayın yetkisini
  belgeleyebilmelisin.
- Oyun özgün veya yetkili/lisanslı olmalı; mevcut bir Playable'ın duplicate ya
  da substantially identical sürümü olmamalı.
- İsim, yaş, konum, kullanıcı adı, parola gibi kişisel bilgiler isteme veya
  toplama. Login/account oluşturma hissi veren UI ve QR-benzeri görseller koyma.
- Analytics, remote database, remote leaderboard, external assets/levels veya
  başka endpoint çağrıları kullanma; yalnız resmen istenen Google/YouTube API'leri
  ve yazılı pilot istisnaları hariçtir.
- Dev/staging oyun bağlantılarını dışarıyla paylaşma.

## 5. Monetization ayarı

- Off-platform ads, IAP veya ödeme kullanma. Yalnız YouTube ads API'lerini kullan.
- Preroll otomatik olabilir. Interstitial doğal ara noktasında gösterilmeli ve
  ödül vermemeli.
- Rewarded ad yalnız açık opt-in ile çağrılmalı; reward ID sabit, benzersiz ve
  kişisel olmayan bir değer olmalı; ödülü yalnız API `true` dönerse ver.
- Portal'daki monetization ayarını oyunun gerçek davranışıyla eşleştir.

## 6. Portal gönderimi

1. ZIP, gerekli thumbnail oranları ve doğru metadata'yı yükle.
2. Ads/monetization ve erişilebilirlik alanlarını güncel Portal seçenekleriyle
   doldur; dokümanda bulunmayan tag adlarını uydurma.
3. Release oluşturulduktan sonra **Verify and test** bölümündeki **Test Suite
   Link** ile ingested build'i, **YouTube Dev Link** ile desktop/mobile web ve
   YouTube Android/iOS uygulamalarını test et.
4. Certification'a gönder. Aynı anda yalnız bir certification review kısıtı
   bulunabileceğini planlamaya dahil et.
5. Ret gerekçesini requirement ID ve reproducible case olarak kaydet; düzeltip
   yeni build üret ve tüm regresyon matrisini yeniden çalıştır.

## Resmî kaynaklar

- [Developer Portal](https://developers.google.com/youtube/gaming/playables/developer_portal)
- [Test Suite guide](https://developers.google.com/youtube/gaming/playables/reference/test_suite_guide)
- [Open Playables Test Suite](https://developers.google.com/youtube/gaming/playables/test_suite)
- [Certification FAQ](https://developers.google.com/youtube/gaming/playables/support/certification_faq)
- [Trust and safety](https://developers.google.com/youtube/gaming/playables/certification/requirements_trustsafety)
- [Monetization requirements](https://developers.google.com/youtube/gaming/playables/certification/requirements_monetization)
- [Revision history](https://developers.google.com/youtube/gaming/playables/certification/revisionhistory)
