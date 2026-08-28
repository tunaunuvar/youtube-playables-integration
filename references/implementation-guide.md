# YouTube Playables Entegrasyon Rehberi

Bu referans, Sling Dunk'te uygulanan entegrasyonun başka bir vanilla
HTML5/Canvas oyununa taşınabilecek şeklini anlatır. Proje adları, storage key'leri,
oyun sınıfları ve ödül ID'leri örnektir; hedef projede yeniden adlandırılmalıdır.

## 1. Giriş ve script sırası

Kök `index.html` tek release giriş noktası olmalı. SDK bütün oyun kodundan önce
yüklenmeli:

```html
<script src="https://www.youtube.com/game_api/v1"></script>
<script src="js/playables.js"></script>
```

Ardından loading UI, oyun modülleri ve en sonda bootstrap yüklenir. Loading UI
başlangıçta görünür olmalı; hata durumunda sonsuz spinner yerine kullanıcıya
retry veya anlaşılır hata gösterilmelidir.

Sling Dunk'teki karşılığı:

- `index.html`: SDK, loading ekranı, oyun script sırası ve dev block.
- `js/playables.js`: host adapter.
- `js/bootstrap.js`: initialize → runtime oluşturma → asset bekleme → ready.

## 2. Bridge tasarımı

Bridge'in görevi host API ile oyunun geri kalanı arasına tek bir sınır koymaktır.
Başlangıçta:

```js
this.sdk = typeof window.ytgame !== 'undefined' ? window.ytgame : null;
this.inPlayables = Boolean(this.sdk && this.sdk.IN_PLAYABLES_ENV);
```

Bridge şu davranışları sağlamalıdır:

| Bridge yüzeyi | Beklenen davranış |
| --- | --- |
| `isInPlayables()` | Host ortamı tespitini tek noktadan döndürür. |
| `initialize()` | `firstFrameReady`, callback binding ve Playables'ta `loadData()` işlemini bir kez başlatır; aynı anda gelen çağrıları aynı Promise'e bağlar. |
| `getInitialSave(primaryKey, legacyKeys)` | Host'ta initialize sırasında yüklenen cloud string'ini; local'de primary/legacy storage key'ini döndürür. |
| `saveData(serialized, localKey)` | Local'de adapter storage'a yazar; host'ta `saveData()` çağrılarını Promise queue ile sıraya alır ve load başarısızsa yazmaz. |
| `sendScore(value)` | Değeri `Math.floor` ile canonical non-negative integer'a çevirir, bekleyen save'in arkasından tekil best score gönderir. |
| `requestRewardedAd(rewardId)` | Host'ta `Promise<boolean>` sonucunu döndürür; local'de gerçek reklam yoksa `null`, hata olursa `false` döndürür. |
| `sendGameReady()` | Idempotent biçimde yalnızca bir kez çağrılır. |
| `reportWarning()` | Console ve varsa `ytgame.health` loglama yapar; hata oyunu kilitlemez. |

Önemli bridge state'leri:

```text
initialized / initializing
firstFrameSent / gameReadySent
cloudLoadSucceeded / initialSave
saveQueue
runtime
hostAudioEnabled
```

SDK method'larının iframe içinde geç hazır olabilme ihtimaline karşı sınırlı
timeout'lu method bekleme kullanılabilir. Timeout sonsuz beklemeye dönüşmemeli.

## 3. Lifecycle sırası

Önerilen akış:

```text
HTML loading görünür
  → bridge.initialize()
  → firstFrameReady() (initialize içinde, bir kez)
  → host callback'lerini bağla
  → loadData() tamamlanmasını bekle
  → oyun yöneticilerini oluştur
  → bridge.bindRuntime({ game, shop/save, sounds })
  → kritik asset'leri bekle (üst sınırla)
  → loading'i kaldır
  → gameReady() (yalnızca etkileşim hazırken)
```

Bootstrap içinde constructor'ların hazır olduğunu açıkça doğrulamak, eksik
script sırasını sessizce yutmak yerine retry ekranına düşürür. Kritik image
yüklemesi `Promise.all` ile yapılabilir; mutlaka timeout/fallback eklenmelidir.

## 4. Cloud save ve migration

Oyunun mevcut save sistemini önce versioned bir JSON schema'ya getir:

```json
{
  "schemaVersion": 2,
  "coins": 0,
  "unlockedSkins": ["classic"],
  "equippedSkin": "classic",
  "bestScoreClassic": 0,
  "leaderboard": { "classic": [] },
  "playerName": "PLAYER"
}
```

Gerçek oyunun ihtiyaç duyduğu alanları ekle; örnekteki alanları gereksiz yere
kopyalama. Load sırasında:

1. Host'ta `loadData()` sonucunu, local'de primary ve legacy key'leri oku.
2. JSON parse hatasında güvenli default state'e düş.
3. Eksik alanları default'la, sayıları integer/non-negative yap, listeleri
   deduplicate et ve tanınmayan skin/ID'leri filtrele.
4. Eski alan adlarını yeni alanlara taşı (`bestScore` → mod bazlı best gibi).
5. Eski ID'leri yeni ID'lere migrate et.
6. Normalized state'i güncel schema version'ıyla runtime'a ver.

Sling Dunk'te bunun özel örnekleri `dunk_shot_save_v1` legacy key'i,
`schemaVersion: 2`, `stars` → `coins`, `bestScore` fallback'i ve `neon` →
`baseball` ID migration'ıdır.

Save kuralları:

- İlk cloud load başarısızsa körlemesine `saveData()` ile üstüne yazma; kullanıcı
  verisini korumak için save'i durdur veya açık fallback kararı ver.
- Shop/progress değişimi, unlock/equip, level sonucu ve yeni best gibi material
  olaylarda save et; yalnızca `beforeunload`'a güvenme.
- Aynı anda çok save oluşabileceği için son çağrıları sıraya al.
- Save string'ini valid UTF-16 JSON olarak tut; 3 MiB hard limitinin altında,
  tercihen 500 KiB civarında kal.
- Playables progress'i localStorage'a bağlama. LocalStorage yalnızca local
  geliştirme fallback'i olmalı ve erişim hataları catch edilmelidir.

## 5. Skor gönderimi

Oyun içinde bir canonical skor seç. Örneğin Sling Dunk'te Playables'a yalnızca
Classic best score gönderiliyor; timed/frenzy/tour skorları ayrı tutuluyor.

Yeni best olduğunda sıra şu olmalı:

```js
const savePromise = shop.saveData();
Promise.resolve(savePromise).then(() => bridge.sendScore(bestScore));
```

Bridge içinde skor:

```js
const score = Math.max(0, Math.floor(Number(value) || 0));
await saveQueue.catch(() => {});
await ytgame.engagement.sendScore({ value: score });
```

Skoru her frame, her oyun over açılışında veya aynı rekor tekrar gösterildiğinde
gönderme. Gönderilen değer ile save içindeki best değerinin aynı olduğuna test
ekle.

## 6. Host pause/resume ve audio

Bridge, `ytgame.system` callback'lerini runtime'a yönlendirmelidir:

```js
hostAudioEnabled = ytgame.system.isAudioEnabled();
ytgame.system.onAudioEnabledChange(enabled => sounds.setHostAudioEnabled(enabled));
ytgame.system.onPause(() => {
  shop.saveData();
  game.pauseFromHost();
  sounds.suspendForHost();
});
ytgame.system.onResume(() => {
  game.resumeFromHost();
  sounds.resumeForHost();
});
```

Oyunda host pause ile kullanıcı pause'ını ayır. Örnek state:

```text
wasPausedBeforeHost
isHostPaused
loopStoppedByHost
```

Host pause sırasında `update()` çağrısı, timer, physics, input, particle ve ses
ilerlememeli. Resume'da `lastTime = performance.now()` ile büyük bir delta
oluşmasını önle; loop durduysa yalnızca bir yeni animation frame planla.

Audio katmanı iki kaynağı birleştirmeli:

```text
effectiveEnabled = userEnabled && hostAudioEnabled
```

Web Audio context çalışıyorsa `suspend()`; host tekrar açtıysa ve kullanıcı da
izin veriyorsa `resume()` kullan. Local user setting'i host audio state'iyle
karıştırma.

## 7. Rewarded ads

Oyuncunun açık isteğiyle çağır ve her ödül tipine sabit ID ata:

```js
const rewardId = type === 'continue' ? 'continue-run' : 'twenty-coins';
const earned = await bridge.requestRewardedAd(rewardId);
if (earned === true) {
  claimRewardOnce(type);
}
```

Kurallar:

- ID kullanıcı verisi içermemeli ve aynı ödül tipi için her seferinde aynı
  kalmalı.
- `true` dışında ödül verme; `false`, `null`, reject ve unavailable durumlarını
  başarısız say.
- Continue gibi ödüller için run başına tek kullanım guard'ı koy.
- Coin ödülü claim state'iyle duplicate claim'i engelle.
- Local geliştirmede gösterilen fake timer/modal branch'i Playables release'e
  girmemeli. Sadece local fallback olarak kalabilir.
- Ad açılırken oyunu pause et; sonuçtan sonra önceki pause durumunu doğru geri
  yükle.

## 8. Release bundle ve CSP testi

Release builder şu işleri otomatik yapmalı:

1. Temiz output klasörü oluştur.
2. Sadece `index.html`, CSS, JS ve asset runtime'ını kopyala.
3. Dev HTML block'unu ve `devtools.js`'i çıkar.
4. Local cache-busting query string'lerini release'te normalize et.
5. Root'ta `index.html`, relative path ve izin verilen filename kontrolü yap.
6. SDK'nin `playables.js`'ten önce geldiğini doğrula.
7. Beklenmeyen external URL'leri reddet.
8. File count, total size ve individual file size raporla.
9. ZIP oluştur ve ZIP root'unda `index.html` olduğunu doğrula.

Sling Dunk'teki `tools/build_playables.py` bu şeklin somut örneğidir. Safety
amacıyla output yolu `dist/playables` ile sınırlandırılmıştır; yeni projede de
output path'i açıkça doğrula. Güncel resmi limitleri yayın öncesi tekrar kontrol
et; mevcut referans hedefleri toplam 250 MiB, dosya başına 30 MiB, save başına
3 MiB ve dosya adlarında relative/izinli karakterlerdir.

Playables benzeri CSP ile local server çalıştırılabilir. Sunucu cache'i kapatmalı
ve test CSP'sini opsiyonel flag ile eklemelidir; normal local geliştirmeyi
gereksiz yere kısıtlama.

## 9. Test sırası

Önce hızlı statik ve bridge kontrolleri:

```bash
node --check js/playables.js
node --check js/game.js
node --check js/shop.js
node tools/test_playables_bridge.js
python tools/build_playables.py
git diff --check
```

Bridge test mock'u en az şunları doğrulamalı:

- `firstFrameReady` → `loadData` sırası.
- LocalStorage'ın Playables testinde kullanılmaması.
- Pause/resume callback'lerinin game ve sound runtime'ına ulaşması.
- Başlangıç audio state'inin runtime'a aktarılması.
- Save queue ve `sendScore` sırası.
- Rewarded ad ID'si ve `true` sonucu.
- `gameReady`'nin idempotent olması.

Sonra temiz profilde ilk açılış, save/load, migration, yeni best, pause/resume,
audio toggle, resize/touch, ad unavailable/error/cancel ve reward duplicate
senaryolarını test et. En sonda desktop web, mobile web, Android/iOS YouTube ve
Playables Test Suite üzerinde doğrula.

## 10. Bu snapshot'ta bilinçli olarak kapsam dışı kalanlar

Sling Dunk uygulamasının bu aşamasında aşağıdakiler tamamlanmış entegrasyon
parçası sayılmamalı:

- Global/remote leaderboard backend'i.
- Analytics veya harici skor/save endpoint'i.
- Developer Portal onboarding ve certification sonucu.
- Tüm resmi Test Suite cihaz kontrolleri.
- Bozuk/kota aşımı save için son kullanıcıya özel UX.
- Production'da local rewarded-ad simülasyonunun tamamen kaldırılması.

Bu konular yeni bir sonraki iterasyonda ayrı karar ve test gerektirir.

## Resmi kaynaklar

- [Getting started](https://developers.google.com/youtube/gaming/playables/reference/getting_started)
- [SDK reference](https://developers.google.com/youtube/gaming/playables/reference/sdk)
- [Integration requirements](https://developers.google.com/youtube/gaming/playables/certification/requirements_integration)
- [Monetization / rewarded ads](https://developers.google.com/youtube/gaming/playables/reference/monetization)
- [Stability and performance](https://developers.google.com/youtube/gaming/playables/certification/requirements_stability)
- [Certification requirements](https://developers.google.com/youtube/gaming/playables/certification/requirements)
