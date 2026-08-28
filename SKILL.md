---
name: youtube-playables-integration
description: Integrate browser-based HTML5 games with the YouTube Playables SDK, including lifecycle, cloud save, score submission, host pause/audio, rewarded ads, release packaging, and local validation. Use when adapting an existing web game for YouTube Playables; not for YouTube video embeds or native mobile SDKs.
---

# YouTube Playables Integration

Bu skill, mevcut bir HTML5/Canvas/WebGL oyununun YouTube Playables ortamına
uyarlanmasını yönlendirir. Projeye göre dosya ve sınıf adlarını uyarla; Sling
Dunk'teki isimleri körlemesine kopyalama.

## Çalışma kuralları

- Önce giriş dosyasını, script sırasını, mevcut save modelini, oyun döngüsünü,
  skor kaynağını, ses katmanını ve reklam akışını incele.
- YouTube API çağrılarını tek bir bridge/adapter arkasında tut. Oyun modülleri
  doğrudan `ytgame` çağırmamalı.
- Yerel tarayıcıda SDK olmadan çalışan bir fallback bırak. Fallback, Playables
  cloud save yerine local storage kullanabilir; Playables ortamında local
  storage'ı progress kaynağı kabul etme.
- `firstFrameReady()` görünür loading/splash frame'inden sonra; `gameReady()`
  yalnızca oyun gerçekten etkileşimliyken ve loading ekranı kaldırılmışken,
  üstelik ilkinden sonra çağrılmalı.
- `loadData()` tamamlanmadan `saveData()` çağırma. Save çağrılarını sıraya al,
  hataları oyun akışını kilitlemeden raporla.
- YouTube'a gönderilen skor, oyunun kalıcı best score değeriyle aynı canonical
  integer olmalı; her frame veya her popup'ta skor gönderme.
- `requestRewardedAd()` sonucu `true` olmadan ödülü verme. Her ödül tipi için
  kullanıcı verisi içermeyen sabit ve benzersiz bir reward ID kullan.
- Host pause durumunda update/timer/physics/input/particle/ses akışını durdur;
  resume'da önceki state'i koruyarak devam ettir.
- Release bundle'da yalnızca relative dosya yolları, gerekli runtime dosyaları
  ve izin verilen dış SDK URL'si bulunmalı. Debug paneli, cheat ve local reklam
  simülasyonu release'e sızmamalı.
- Resmi Playables dokümanlarını ve güncel limitleri görev sırasında doğrula;
  bu skill bir certification onayı değildir.

## Uygulama akışı

1. Projeyi keşfet ve Playables'a gidecek tek web runtime'ı belirle.
2. HTML girişinde SDK'yı tüm oyun kodundan önce yükle; görünür loading UI ekle.
3. `playablesBridge` benzeri adapter'ı oluştur ve aşağıdaki yüzeyi uygula:
   `isInPlayables()`, `initialize()`, `getInitialSave()`, `saveData()`,
   `sendScore()`, `requestRewardedAd()`, `sendGameReady()` ve runtime binding.
4. Bootstrap sırasında bridge'i initialize et, cloud save'i yükle, sonra oyun
   yöneticilerini oluştur ve bridge'e bind et.
5. Save schema'sını version'la; eski key/alan/ID'leri migrate et; material
   progress anlarında save et.
6. Oyun döngüsüne host pause/resume, ses katmanına host audio state, skor akışına
   best-score gönderimi ve reklam akışına rewarded adapter bağla.
7. Release builder ile debug ayıklanmış bundle ve ZIP üret; dosya adı, relative
   path, SDK sırası, dış URL ve boyut kontrollerini çalıştır.
8. Bridge unit testini, temiz profil testini ve Playables Test Suite cihaz
   testlerini çalıştır; certification tamamlandı iddiasında bulunma.

Core bridge ve Sling Dunk'te doğrulanmış uygulama noktaları için
[implementation-guide.md](references/implementation-guide.md) dosyasını oku.

## Bu skill'in mevcut kapsamı

Bu sürüm lifecycle, cloud save/load, versioned migration, canonical score,
host pause/resume, host audio, rewarded ad çağrı noktası, local fallback,
release packaging ve temel testleri kapsar. Leaderboard backend'i, analytics,
portal onboarding, certification, tam mobile QA ve sonraki monetization
iyileştirmeleri bu sürümün dışında bırakılmıştır.
