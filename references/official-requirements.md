# Resmi YouTube Playables Gereksinimleri

Son araştırma: **2026-08-28**. Bu dosya resmi İngilizce Google/YouTube
dokümanlarının uygulanabilir özetidir; İngilizce canlı sayfalar her zaman
otoritedir. Görev başında [revision history](https://developers.google.com/youtube/gaming/playables/certification/revisionhistory)
kontrol edilmelidir.

## Gereksinim dili

- `MUST` / `MUST NOT`: Certification için zorunlu veya yasak.
- `SHOULD` / `SHOULD NOT`: Güçlü öneri; sapma gerekçesi anlaşılmalı.
- `MAY`: Opsiyonel.
- `EXPECT`: Gelecekte zorunlu olması beklenen, şimdilik opsiyonel madde.

Kaynak: [Certification requirements](https://developers.google.com/youtube/gaming/playables/certification/requirements)

## 1. Runtime ve temel yapı

- Playable standart web API'leriyle üretilmiş web build'i olmalı. Canvas,
  WebGL ve JavaScript uygundur; web export üretebilen engine'ler kullanılabilir.
- Build bir Single Page Application olmalı.
- Bundle root'unda `index.html` bulunmalı.
- SDK, oyun kodunun tamamından önce yüklenmeli:

```html
<script src="https://www.youtube.com/game_api/v1"></script>
```

- Global `ytgame` değişkeni ezilmemeli. Host tespiti hem `typeof ytgame` hem de
  `ytgame.IN_PLAYABLES_ENV` ile yapılmalı.
- Playables; desteklenen desktop browser'larda ve YouTube Android/iOS
  uygulamalarında çalışmalı.

Kaynaklar: [Overview](https://developers.google.com/youtube/gaming/playables),
[Getting started](https://developers.google.com/youtube/gaming/playables/reference/getting_started),
[SDK reference](https://developers.google.com/youtube/gaming/playables/reference/sdk),
[Privacy requirements](https://developers.google.com/youtube/gaming/playables/certification/requirements_privacydata)

## 2. Lifecycle, save, score, audio ve pause

### Game ready

- Görünür ve açıkça loading olduğunu anlatan ilk frame/splash hazır olduğunda
  `firstFrameReady()` çağrılmalı.
- `gameReady()` yalnızca ana menü veya oynanabilir sahne gerçekten kullanıcı
  etkileşimine hazır olduğunda çağrılmalı.
- Loading/splash veya etkileşimsiz UI hâlâ görünürken `gameReady()` çağrılmamalı.

### Cloud save

- Kullanıcının kaydedildiğini bekleyeceği material progress noktalarında
  `saveData()` çağrılmalı.
- Playables içindeki progress başka bir mekanizmayla tutulmamalı.
- `loadData()` başarıyla tamamlanmadan `saveData()` çağrılmamalı.
- Eski oyun sürümlerinin save verileri yeni sürümlerde hata/crash olmadan
  kullanılmalı ve beklenen progress korunmalı.
- Milestone'larda otomatik save yapılmalı. Exit sırasındaki final flush yalnızca
  best-effort'tür ve içerik uzunluğu 64 KiB ile sınırlı olabilir.
- Save valid, well-formed UTF-16 string olmalı.

### Score

- `sendScore()` opsiyoneldir. Kullanılırsa tek ve tutarlı bir progress boyutu
  seçilmeli.
- Gönderilen highest score ile cloud save içindeki best score aynı olmalı.
- Değer integer ve JavaScript maximum safe integer sınırında olmalı.

### Audio

- Başlangıçta `isAudioEnabled()`, değişikliklerde
  `onAudioEnabledChange()` kullanılmalı.
- YouTube mute aktifken hiçbir ses çıkmamalı; oyun içi audio kontrolleri bu
  host kararını geçersiz kılamamalı.
- Device volume kontrolü gözetilmeli ve ses beklenmedik anda başlamamalı.
- Genel mute butonu göstermek önerilmez; music/SFX/speech gibi granular
  kontroller eklenebilir fakat host mute her zaman üstündür.

### Pause/resume

- `onPause()` sonrası game loop, rendering, input, music, timer, network ve tüm
  execution durmalı; yalnızca `onResume()` sonrası devam etmeli.
- Page Visibility API veya benzer web API'leri host pause kaynağı olarak
  kullanılmamalı; Playables callback'leri tek otorite olmalı.
- Pause sırasında save önerilir. Pause sonrası resume garantisi yoktur.

Kaynaklar: [Integration requirements](https://developers.google.com/youtube/gaming/playables/certification/requirements_integration),
[SDK reference](https://developers.google.com/youtube/gaming/playables/reference/sdk)

## 3. Teknik ve paket limitleri

| Konu | Zorunlu | Önerilen |
| --- | --- | --- |
| Initial bundle | `< 30 MiB` | `< 15 MiB` |
| Total bundle | `< 250 MiB` | Minimal indirme ve lazy loading |
| Tek dosya | `< 30 MiB` | `< 512 KiB` |
| Cloud save | `< 3 MiB` | `< 500 KiB` |
| Etkileşime hazır olma | — | `< 5 saniye` |
| Peak JavaScript heap | `<= 512 MB` | Daha düşük hedef |
| Dosya sayısı | `<= 8000` | Daha az dosya |

- Initial bundle, page load başlangıcından `gameReady()` çağrısına kadar indirilen
  transfer boyutudur; uploaded build/Test Suite gerçek ölçüm için tercih edilir.
- Reproducible crash olmamalı ve oyun YouTube uygulamasını/siteyi çökertmemeli.
- Bütün bundle referansları relative olmalı; absolute path kullanılmamalı.
- Her path segmenti yalnızca alphanumeric, `_`, `-`, `.` karakterleri içermeli.

Kaynaklar: [Stability and performance](https://developers.google.com/youtube/gaming/playables/certification/requirements_stability),
[Certification FAQ](https://developers.google.com/youtube/gaming/playables/support/certification_faq)

## 4. Privacy, veri ve dış erişim

- Oyun ve geliştirici Google Privacy Policy'ye uymalı.
- Oyun dış URL veya servise çağrı yapmamalı. Yalnızca başka teknik
  gereksinimleri karşılamak için açıkça gerekli Google/YouTube API'leri istisna.
- Kısıtlamaları aşmaya çalışma, proxy/tunnel veya gizli fallback eklenmemeli.
- Analytics için istisna yoktur. Remote database, level, config, leaderboard,
  asset veya API çağrısı yoktur; bütün game data bundle içinde olmalı. Seçilmiş
  title'lar için pilot erişim ancak YouTube'un yazılı onayıyla mümkündür.
- QR kod gibi görünen veya işlev gören grafik gösterilmemeli.
- Clipboard yalnızca oyuncunun açık paste eylemine cevap olarak okunabilir.
- Oyun isim, yaş, konum, username, password veya başka kişisel bilgi istememeli
  ya da toplamamalı.
- Login veya account creation ekranına benzeyen UI gösterilmemeli.
- Obfuscation yasaktır. Normal minification, dosya birleştirme ve TypeScript
  transpilation uygundur; işlevi saklayan teknikler uygun değildir.
- YouTube, incelenemeyen `WASM`, `eval()` veya web worker kullanımını kendi
  takdirinde reddedebilir. Kullanımı gerekçeli, sınırlı ve denetlenebilir tut.

Kaynaklar: [Privacy requirements](https://developers.google.com/youtube/gaming/playables/certification/requirements_privacydata),
[Certification FAQ](https://developers.google.com/youtube/gaming/playables/support/certification_faq)

## 5. Responsive tasarım ve input

- Oyun bütün aspect ratio'larda oynanabilir ve viewport değişince otomatik
  uyarlanabilir olmalı. Resmi örnek aralık 9:32'den 32:9'a uzanır.
- Viewport doldurulmuyorsa oyun ortalanmalı ve pillarbox/letterbox kullanılmalı.
- Orientation veya device posture kilitlenmemeli.
- Resize sırasında state/progress korunmalı; restart/refresh yapılmamalı veya
  kullanıcı hızla önceki state'e dönebilmelidir.
- Touch ve mouse bütün etkileşimlerde desteklenmeli; input gecikmemeli veya
  görmezden gelinmemeli.
- UI component'lerinde hata veya beklenmeyen davranış olmamalı.
- Keyboard directional/text input için önerilir; modal'lar `Esc` ile kapanmalı.
  `Esc` event'inde `preventDefault()` kullanılmamalı.
- Haptics varsa aç/kapat kontrolü zorunludur.
- Text ve grafikler bütün resolution, density ve oranlarda net render edilmeli.
- Son seviye veya içerik sonunda kullanıcıya içeriğin tamamlandığı anlatılmalı.

Kaynaklar: [Design requirements](https://developers.google.com/youtube/gaming/playables/certification/requirements_design),
[Design best practices](https://developers.google.com/youtube/gaming/playables/certification/best_practices_design)

## 6. Yasak UI ve metadata davranışları

- Oyun içinde paylaşım prompt'u gösterilmemeli.
- Kullanıcıyı başka site/oyuna götüren clickable external link gösterilmemeli.
- Ek user agreement, terms veya privacy consent ekranı gösterilmemeli.
- YouTube Playables close/mute/menu aksiyonlarına benzeyen ikonlar host
  kontrollerinin yakınına konmamalı.
- In-game exit/quit butonu bulunmamalı.
- Portal'da title, genre, description, publisher/developer ve gerekli thumbnail
  alanları doldurulmalı.
- Resmi design requirement, thumbnail/title/description içinde branding veya
  logo kullanılmamasını ister. Portal'ın canlı alan yönergeleri ayrıca kontrol
  edilmelidir.

Kaynak: [Design requirements](https://developers.google.com/youtube/gaming/playables/certification/requirements_design)

## 7. Dil ve accessibility

- İngilizce destek zorunludur.
- Locale gerekiyorsa yalnızca `ytgame.system.getLanguage()` kullanılmalı.
  `navigator.language(s)` kullanılmamalı ve locale cloud save'e yazılmamalı.
- WCAG AA için best effort güçlü öneridir.
- 24 Ağustos 2026 revision kaydı, Accessible Gaming Initiative discovery ve
  metadata doğruluğu için yeni game accessibility tags eklendiğini bildirir.
  Tag adları ve Portal alanları canlı doküman/Portal'dan doğrulanmalı; tahmin
  edilmemelidir.

Kaynaklar: [i18n/L10n requirements](https://developers.google.com/youtube/gaming/playables/certification/requirements_i18n_l10n),
[Accessibility requirements](https://developers.google.com/youtube/gaming/playables/certification/requirements_accessibility),
[Revision history](https://developers.google.com/youtube/gaming/playables/certification/revisionhistory)

## 8. Monetization

- Off-platform monetization, reklam veya in-app purchase yasaktır.
- YouTube'un sağladığı ads API'leri kullanılabilir.
- Pre-roll YouTube tarafından otomatik yönetilir.
- Interstitial doğal kırılma noktalarında kullanılmalı; oyuncuya ödül vermek
  için kullanılmamalı.
- Rewarded ad oyuncunun açık isteğiyle çağrılmalı. Her reward type için sabit,
  benzersiz ve kullanıcı verisi içermeyen ID kullanılmalı; ödül yalnızca
  Promise `true` dönerse verilmelidir.
- Ads kullanılırken host audio ve pause/resume davranışı çalışmaya devam etmeli.
- Ads özellikleri Developer Portal monetization ayarlarında da açılmalı.

Kaynaklar: [Monetization requirements](https://developers.google.com/youtube/gaming/playables/certification/requirements_monetization),
[Monetization reference](https://developers.google.com/youtube/gaming/playables/reference/monetization),
[SDK reference](https://developers.google.com/youtube/gaming/playables/reference/sdk)

## 9. Trust & Safety ve haklar

- YouTube Community Guidelines'a uyulmalı.
- Oyun çocuklara özel hedeflenmemeli veya "made for kids" olmamalı; 13+ genel
  kitleye uygun olmalı.
- Title, thumbnail ve description yanıltıcı olmamalı.
- YouTube Developer Terms of Service'e uyulmalı.
- Trademark, copyright, music, trade dress, name/likeness ve diğer haklar
  dağıtım için temizlenmiş olmalı.
- 25 Ağustos 2026 güncellemesine göre upload özgün, yetkili veya uygun lisanslı
  içeriği temsil etmeli; platformdaki başka bir Playable'ın duplicate veya
  substantially identical build'i olmamalı.
- Certification dev/staging linkleri test amacı dışında paylaşılmamalı.

Kaynaklar: [Trust and Safety requirements](https://developers.google.com/youtube/gaming/playables/certification/requirements_trustsafety),
[Revision history](https://developers.google.com/youtube/gaming/playables/certification/revisionhistory)

## 10. Hızlı yayın engeli listesi

Aşağıdakilerden biri varsa readiness `FAIL` olmalı:

- SDK'dan önce çalışan oyun scripti.
- Loading görünürken `gameReady()`.
- `loadData()` öncesi save veya Playables progress için localStorage.
- Analytics, Firebase/Supabase, custom API, CDN veya remote level çağrısı.
- Oyuncu adı/login/hesap/kişisel veri girişi.
- Off-platform ads/IAP/ödeme.
- Touch veya mouse akışlarından birinin eksik olması.
- Resize'da state kaybı veya orientation lock.
- Host pause sırasında loop/render/audio/network devam etmesi.
- Absolute asset path, desteklenmeyen filename, root'ta olmayan `index.html`.
- Çocuklara özel, yanıltıcı, duplicate veya hakları belirsiz içerik.
