# Oyun Tasarımı ve Erişilebilirlik

Bu dosya, oyunun yalnızca teknik olarak açılmasını değil, YouTube Playables
incelemesinde kullanılabilir ve anlaşılır bulunmasını hedefler. Gereksinimler
değişebileceği için yayın öncesinde canlı İngilizce dokümanları yeniden kontrol
et.

## Ekran ve yerleşim

- Oyun 9:32 ile 32:9 dahil farklı en-boy oranlarında çalışmalı; orientation veya
  posture kilitlememeli.
- Resize sırasında oyun state'i kaybolmamalı. Canvas backing store, CSS boyutu ve
  input koordinat dönüşümü birlikte güncellenmeli.
- Oyun alanı ekranı doldurmuyorsa ortalanmış letterbox/pillarbox kullan; kritik
  kontrolleri güvenli alanların dışında bırakma.
- İlk görünen ekran loading/splash olabilir. `gameReady()` çağrıldığında oyuncu
  gerçekten etkileşime başlayabilmeli.
- Test Suite'in gizli Android WebView'i başlangıçta `0 × 0` olabilir. Kod sıfır
  boyutta hata vermemeli ve daha sonra gelen resize ile toparlanmalı.

## Kontroller ve oyun akışı

- Bütün zorunlu etkileşimler touch ve mouse ile yapılabilmeli. Keyboard desteği
  güçlü biçimde önerilir.
- Input'a yapay gecikme ekleme. Görsel geri bildirim dokunma anında görünmeli.
- `Escape` modal/overlay kapatmalı; bu tuşta `preventDefault()` kullanma.
- Oyunun içine YouTube'a benzeyen menü, kapatma, paylaşma veya çıkış kontrolü
  koyma. Haricî link ve paylaşım çağrısı kullanma.
- Kısa ve anlaşılır onboarding ver; temel mekanik mümkün olduğunca ilk oyun
  sırasında öğrenilebilsin.
- Haptics kullanılıyorsa oyuncuya kapatma seçeneği sun.

## Görsel ve işitsel erişilebilirlik

- WCAG 2.1 AA seviyesini hedefle: metin kontrastı, okunabilir punto, görünür
  focus ve yalnız renge dayanmayan bilgi aktarımı kullan.
- Metinleri görsele gömmek yerine mümkünse gerçek metin olarak göster; zoom ve
  lokalizasyona dayanıklı tut.
- Hızlı yanıp sönme, yoğun ekran sallanması ve sürekli hareket için azaltma veya
  kapatma seçeneği değerlendir.
- Sesle verilen kritik bilgiyi görsel olarak da ilet. Müzik/SFX gibi ayrıntılı
  kontroller olabilir, fakat host mute her zaman üstündür.
- Accessibility metadata/tag alanları Portal'da değişebilir. Alan adlarını tahmin
  etme; yayın gününde Portal ve güncel gereksinim sayfasından doğrula.

## Metadata ve thumbnail

- Doğru title, genre, description, publisher/developer ve istenen thumbnail
  oranlarını sağla.
- Metadata oyunun gerçek içeriğini temsil etmeli; yanıltıcı vaat veya görsel
  kullanma.
- Resmî tasarım kuralına göre title, description ve thumbnail içine fazladan
  branding/logo yerleştirme.
- Thumbnail'leri küçük boyutta, açık/koyu yüzeylerde ve farklı crop oranlarında
  test et; önemli öğeleri kenarlara yaslama.

## Lokalizasyon

- İngilizce zorunludur. Diğer diller isteğe bağlıdır.
- Locale'i yalnızca `ytgame.system.getLanguage()` ile al; `navigator.language`
  veya `navigator.languages` kullanma.
- Locale'i cloud save'e yazma. Dil değişince UI'yı yeniden kurabilecek şekilde
  metin anahtarları kullan.
- Uzun çeviriler, RTL, CJK fontları, satır kırılması ve sayı biçimlerini test et.
  Gerekli bütün fontları bundle içinde self-host et.

## Tasarım QA matrisi

En az şu kombinasyonları elle doğrula:

| Alan | Senaryolar |
| --- | --- |
| Boyut | dar portrait, telefon landscape, 16:9, ultrawide, `0 × 0` → normal |
| Input | touch, mouse, keyboard, hızlı tekrar, aynı anda iki pointer |
| Overlay | pause, ad, modal, resize sırasında modal, Escape |
| Erişilebilirlik | keyboard-only, yüksek zoom, reduced motion, audio kapalı |
| Dil | English, en uzun çeviri, RTL varsa RTL, eksik anahtar fallback'i |

## Resmî kaynaklar

- [Design requirements](https://developers.google.com/youtube/gaming/playables/certification/requirements_design)
- [Design best practices](https://developers.google.com/youtube/gaming/playables/certification/best_practices_design)
- [Internationalization and localization](https://developers.google.com/youtube/gaming/playables/certification/requirements_i18n_l10n)
- [Accessibility requirements](https://developers.google.com/youtube/gaming/playables/certification/requirements_accessibility)

