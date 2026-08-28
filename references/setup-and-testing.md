# Kurulum, Bağımlılıklar ve Test Ortamı

Bu referansı skill'i kurarken, hedef oyunun toolchain'ini hazırlarken veya oyunu
YouTube ortamına göndermeden önce test ederken kullan.

## 1. Skill'i Codex'e kurma

GitHub repository yayınlandıktan sonra `<owner>` alanını gerçek GitHub kullanıcı
veya organization adıyla değiştir.

### Git ile kurulum

Windows PowerShell:

```powershell
git clone https://github.com/<owner>/youtube-playables-integration.git "$env:USERPROFILE\.codex\skills\youtube-playables-integration"
```

macOS/Linux:

```bash
git clone https://github.com/<owner>/youtube-playables-integration.git "${CODEX_HOME:-$HOME/.codex}/skills/youtube-playables-integration"
```

Güncellemek için skill klasöründe `git pull` çalıştır. Kurulumdan sonra yeni bir
Codex görevi açıp skill'i açıkça çağır:

```text
$youtube-playables-integration bu web oyununu YouTube Playables için hazırla,
paketle ve readiness raporu çıkar.
```

Manuel alternatif olarak repository'yi indirip klasörün tamamını aynı
`youtube-playables-integration` hedef dizinine kopyala. Yalnız `SKILL.md` dosyasını
kopyalama; `references/` ve `scripts/` da gereklidir.

## 2. NPM gerekiyor mu?

YouTube Playables SDK için `npm install` gerekmez ve varsayımsal bir YouTube SDK
paketi yüklenmemelidir. Resmî SDK, bütün oyun kodundan önce `index.html` içine
eklenen şu script ile gelir:

```html
<script src="https://www.youtube.com/game_api/v1"></script>
```

NPM, pnpm veya Yarn yalnızca hedef oyunun kendi build sistemi bunları kullanıyorsa
gereklidir. Önce repo dosyalarını incele ve lockfile'a göre mevcut package
manager'ı koru:

| Bulunan dosya | Tercih edilen kurulum |
| --- | --- |
| `package-lock.json` | `npm ci` |
| Yalnız `package.json` | `npm install` |
| `pnpm-lock.yaml` | `pnpm install --frozen-lockfile` |
| `yarn.lock` | Projenin Yarn sürümüne uygun immutable/frozen install |
| Hiçbiri | Paket yöneticisi ekleme; vanilla oyun doğrudan çalışabilir |

Kurulumdan önce `node --version` ve ilgili package manager sürümünü kontrol et.
Lockfile silme veya başka package manager ile yeniden üretme. Yeni dependency
ancak mevcut build için gerçekten gerekiyorsa eklenmeli; release runtime'ında
CDN veya remote package çağrısı bırakılmamalıdır.

## 3. Build komutunu bulma

`package.json` varsa `scripts` alanını oku. `npm run build` veya `npm run dev`
komutlarının var olduğunu tahmin etme. Engine projelerinde motorun resmî web
export akışını kullan; çıkan root `index.html` ve bütün asset'leri denetle.

Skill'in kendi bundle validator'ı Python standard library dışında dependency
istemez:

```bash
python scripts/validate_playables_bundle.py path/to/release
python scripts/validate_playables_bundle.py path/to/release.zip --json
```

## 4. Oyunu yerelde çalıştırma

Önce projenin mevcut dev-server komutunu kullan. Yoksa dependency kurmadan basit
bir static server açılabilir:

```bash
python -m http.server 8080 --directory path/to/release
```

Sonra `http://localhost:8080` adresini aç. Oyunu `file://` ile açma; browser ve
asset davranışı gerçek web serving koşullarından farklı olabilir.

Yerel çalışmada SDK no-op olabilir. Bu yüzden yalnız local smoke test ile
`loadData`, `saveData`, lifecycle, pause/audio veya ads entegrasyonuna `PASS`
verme.

## 5. Resmî çevrimiçi Test Suite

Yerel oyun açıldıktan sonra:

1. [YouTube Playables SDK Test Suite'i aç](https://developers.google.com/youtube/gaming/playables/test_suite).
2. URL alanına oyunun çalışan adresini, örneğin `http://localhost:8080`, gir.
   Resmî revision history'ye göre localhost testi HTTPS gerektirmez.
3. Loading mock'u ve SDK kontrollerini çalıştır; console, network, CSP, lifecycle,
   save/load, score, audio ve pause/resume sonuçlarını incele.
4. URL'yi veya build'i değiştirdikten sonra Test Suite içindeki refresh
   kontrolüyle yeniden çalıştır.
5. Test Suite sonucu ile repo validator sonucunu readiness raporuna ayrı ayrı
   yaz. Test Suite başarı sonucu certification onayı değildir.

Test Suite guide'daki güncel Content Security Policy değerini ayrıca yerel
response override olarak test et. CSP metnini bu repository'den kopyalayıp kalıcı
doğru varsayma; resmî sayfadan güncel halini al.

## 6. Developer Portal içindeki gerçek YouTube testi

Portal erişimi davet ve onboard edilmiş YouTube channel yetkisi gerektirebilir.
Release ZIP'i oluşturup Portal'a yükledikten sonra:

1. Release creation tamamlanana kadar bekle.
2. Sol menüde açılan **Verify and test** bölümüne gir.
3. Buradaki **Test Suite Link** ile ingested build'i doğrula.
4. **YouTube Dev Link** ile desktop web ve mobile web üzerinde test et.
5. Dev Link'i güvenli biçimde kendi cihazlarına aktararak YouTube Android ve iOS
   uygulamalarında test et; dev/staging linkini dışarıya açık paylaşma.
6. Ancak bütün kontroller tamamlandıktan sonra **Submit for Certification**
   kullan.

Portal erişimi yoksa teknik entegrasyon ve açık Test Suite testi yapılabilir;
Portal build'i, gerçek YouTube uygulamaları ve certification durumu
`NEEDS PORTAL` olarak kalmalıdır.

## 7. Tam test sırası

```text
Dependency/toolchain tespiti
  → temiz production build
  → local smoke test
  → statik bundle validator
  → güncel CSP testi
  → açık Playables Test Suite
  → Portal release
  → Portal Test Suite Link
  → YouTube Dev Link: desktop/mobile web/Android/iOS
  → preflight checklist
  → Submit for Certification
```

## Resmî kaynaklar

- [Getting started](https://developers.google.com/youtube/gaming/playables/reference/getting_started)
- [Open Playables Test Suite](https://developers.google.com/youtube/gaming/playables/test_suite)
- [Test Suite guide and CSP](https://developers.google.com/youtube/gaming/playables/reference/test_suite_guide)
- [Developer Portal testing workflow](https://developers.google.com/youtube/gaming/playables/developer_portal)
- [Revision history](https://developers.google.com/youtube/gaming/playables/certification/revisionhistory)

