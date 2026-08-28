---
name: youtube-playables-guide
description: Guide AI agents through preparing, integrating, auditing, packaging, and testing HTML5, Canvas, WebGL, Unity WebGL, Godot Web, or Flutter Web games for YouTube Playables. Use for SDK implementation, certification readiness, game-design compliance, privacy review, monetization, bundle validation, Test Suite preparation, and Developer Portal release work; not for ordinary YouTube video embeds or native mobile builds.
---

# YouTube Playables Guide

Bu skill, mevcut bir web oyununun YouTube Playables'a teknik olarak entegre
edilmesini ve certification öncesi uçtan uca denetlenmesini sağlar. Dosya, sınıf
ve build sistemi adlarını hedef projeye göre uyarla; örnek projedeki isimleri
körlemesine kopyalama.

## Kaynak otoritesi

- Görev başında resmi İngilizce Playables gereksinimlerini ve
  [revision history](https://developers.google.com/youtube/gaming/playables/certification/revisionhistory)
  sayfasını kontrol et. Kurallar sık değiştiği için bu skill'deki tarihli
  snapshot'ı tek başına son söz kabul etme.
- Zorunlu kurallar için yalnızca Google/YouTube'un resmi dokümanlarını kaynak
  kabul et. Resmi GitHub örnekleri ve üçüncü taraf template'ler uygulama örneği
  olabilir; certification kuralı belirleyemez.
- `MUST`/`MUST NOT` yayın engeli, `SHOULD` güçlü öneri, `MAY` opsiyon olarak ele
  alınmalı. Belirsizliği zorunlu kural gibi sunma.
- Portal erişimi veya gerçek cihaz/Test Suite sonucu görülmeden "certification
  ready" ya da "certification passed" deme.

## Her görevde uygulanacak kapılar

- Playables runtime'ı bir SPA ve standart web build'i olmalı; root'ta
  `index.html` bulunmalı.
- SDK bütün oyun kodundan önce yüklenmeli ve `window.ytgame` ezilmemeli.
- Playables ortamında progress yalnızca `loadData()`/`saveData()` ile tutulmalı;
  cloud load tamamlanmadan save yapılmamalı.
- Oyun harici URL, analytics, remote config, CDN, database veya özel leaderboard
  çağrısı yapmamalı. Yalnızca açıkça gerekli Google/YouTube API'leri istisnadır.
- Oyun isim, kullanıcı adı, yaş, konum, parola veya başka kişisel bilgi
  istememeli/toplamamalı; login, hesap oluşturma ve QR benzeri ekran göstermemeli.
- Touch ve mouse bütün etkileşimlerde çalışmalı; oyun viewport değişince state
  kaybetmemeli ve orientation/posture kilitlememeli.
- Host pause tüm execution'ı; YouTube mute bütün ses çıkışını durdurmalı.
- Off-platform reklam, ödeme veya satın alma eklenmemeli. Reklam varsa yalnızca
  YouTube ads API'leri ve eşleşen Portal ayarları kullanılmalı.
- İçerik 13+ genel kitleye uygun, özgün/yetkili/lisanslı olmalı; çocuklara özel,
  yanıltıcı, duplicate veya hakları temizlenmemiş build yayınlanmamalı.

## Referans yönlendirmesi

- Skill kurulumu, NPM/pnpm/Yarn dependency hazırlığı, local server veya resmî
  test ortamı gerektiğinde
  [setup-and-testing.md](references/setup-and-testing.md) dosyasını oku.
- Her planlama veya audit görevinde
  [official-requirements.md](references/official-requirements.md) dosyasını oku.
- SDK bridge, lifecycle, cloud save, score, pause/audio veya ads kodlarken
  [implementation-guide.md](references/implementation-guide.md) dosyasını oku.
- Responsive UI, input, onboarding veya accessibility çalışırken
  [game-design-and-accessibility.md](references/game-design-and-accessibility.md)
  dosyasını oku.
- Unity, Godot, Flutter ya da framework export'u uyarlarken
  [engine-notes.md](references/engine-notes.md) dosyasını oku.
- ZIP, CSP, Test Suite, metadata, Portal veya certification işlerinde
  [release-and-certification.md](references/release-and-certification.md)
  dosyasını oku.
- Teslimden önce [preflight-checklist.md](references/preflight-checklist.md)
  dosyasını uygula. Bundle varsa `scripts/validate_playables_bundle.py` çalıştır.

## Çalışma akışı

1. Runtime, engine/framework, giriş HTML'i, build output'u, asset yolları,
   storage, score, game loop, audio, input ve monetization noktalarını çıkar.
2. İlk olarak yayın engellerini ara: dış çağrılar, kişisel veri, login, remote
   content, absolute path, unsupported filename, off-platform ads/IAP, debug ve
   hakları belirsiz içerik.
3. SDK'yı tek bir bridge/adapter arkasına al; lifecycle ve cloud load tamamlanana
   kadar gameplay manager'larını başlatma.
4. Save schema migration, canonical score, pause/resume, host audio ve gerekiyorsa
   YouTube ads entegrasyonunu uygula.
5. Responsive/input/accessibility gereksinimlerini gerçek viewport ve cihaz
   davranışıyla ele al.
6. Temiz release output'u üret; debug/cheat/local ad simulation dosyalarını çıkar.
7. Bundle validator, syntax/unit test, CSP testi ve temiz profil senaryolarını
   çalıştır; ardından oyunu resmî çevrimiçi
   [Playables Test Suite](https://developers.google.com/youtube/gaming/playables/test_suite)
   içinde doğrula.
8. Portal release'i varsa **Verify and test** bölümündeki Test Suite Link ve
   YouTube Dev Link ile desktop web, mobile web, Android ve iOS testlerini yap.
9. Portal gerektiren kontrolleri ayrı işaretle; tahmin ederek PASS verme.

## Teslim formatı

Sonuçta kısa bir readiness raporu ver:

- `PASS`: Kod veya üretilen artifact ile doğrulandı.
- `FAIL`: Somut ihlal var; dosya/konum ve düzeltme belirtilmeli.
- `NEEDS PORTAL`: Developer Portal, uploaded build veya gerçek YouTube ortamı
  gerekiyor.
- `UNVERIFIED`: Manuel cihaz, hak sahipliği ya da kullanıcı kararı gerekiyor.

Değişen dosyaları, çalıştırılan testleri, kalan blokları ve ilgili resmi kaynak
linklerini rapora ekle. Otomatik testlerin kapsamını aşan bir onay verme.
