# Motor ve Framework Notları

Önce ortak Playables gereksinimlerini uygula; bu dosyadaki maddeler yalnızca
motorun ürettiği build'i o gereksinimlere yaklaştırır.

## Vanilla HTML5 / Canvas

- SDK script'ini `index.html` içindeki bütün oyun scriptlerinden önce koy.
- Ana loop'u tek yerde yönet; host pause'da RAF planlamasını, rendering'i,
  physics/timer/input/network işlerini durdur.
- Canvas CSS boyutu ile gerçek pixel boyutunu ayır ve pointer koordinatlarını
  buna göre dönüştür.
- Asset manifest kullan; bütün asset URL'leri relative ve bundle içinde olsun.

## Unity WebGL

- YouTube'un deneysel Unity wrapper'ını başlangıç noktası olarak incele, fakat
  wrapper'ın güncel SDK davranışını karşıladığını ayrıca doğrula.
- WebGL build üret. JS/C# bridge üzerinden lifecycle, save, score, audio ve ads
  çağrılarını tek adaptörde topla.
- YouTube sunucusunun otomatik gzip/brotli çözmesini varsayma. Unity compression
  varsayılan olarak kapalı tutulabilir; compression gerekiyorsa resmî wrapper'ın
  ZIP precompression/manual loader yaklaşımını takip et.
- JS heap üst sınırı 512 MB'dir. Texture, audio, asset bundle ve Unity memory
  ayarlarını gerçek cihazda ölç.
- Template'in eklediği analytics, CDN, remote font veya remote loader çağrılarını
  kaldır.

## Godot Web

- HTML5/Web export al ve tüm `.wasm`, `.pck`, worker ve yardımcı scriptleri
  bundle içine koy.
- Threaded export genellikle ek cross-origin header varsayımları getirir;
  Playables ortamında doğrulanmamışsa threads kapalı build'i tercih et.
- SDK'yı Godot loader'dan önce yükle ve JS bridge'i autoload/singleton katmanına
  bağla.
- Pause sırasında engine loop, audio ve input'u gerçekten durdur. Yalnızca oyun
  state flag'i değiştirmek yeterli değildir.
- WASM inceleme sırasında ek değerlendirme alabilir; debug symbols/source map ve
  kaynak üretim adımlarını inceleme için sakla, obfuscation kullanma.

## Flutter Web

- Resmî Flutter wrapper örneğini başlangıç noktası olarak kullan.
- Build'den base href'i kaldır; relative asset yollarını doğrula.
- `flutter build web --no-web-resources-cdn` kullan ve fontları/CDN kaynaklarını
  bundle içine al.
- SDK çağrılarını Dart JS interop katmanında tek adapter'da topla.
- CanvasKit/renderer boyutunu ve ilk transfer maliyetini ölç; initial bundle
  hedefini aşarsa renderer ve asset stratejisini yeniden değerlendir.

## Diğer motorlar için karar listesi

Bir motor veya exporter kullanmadan önce şu soruların tümüne cevap ver:

1. Root `index.html` ve script sırası kontrol edilebiliyor mu?
2. Tüm runtime/asset/fontlar haricî servis olmadan paketlenebiliyor mu?
3. Pause sırasında execution, rendering, audio, input ve network durabiliyor mu?
4. Cloud save yüklenmeden yazma yapılması engellenebiliyor mu?
5. Export 512 MB heap ve paket boyutu sınırlarında gerçek cihazda çalışıyor mu?
6. Üretilen WASM/JS incelemeye açık ve obfuscation'sız mı?

Bir yanıt hayırsa motor build'i sertifikasyona hazır sayma.

## Resmî kaynaklar

- [Unity wrapper](https://developers.google.com/youtube/gaming/playables/samples/unity_wrapper)
- [Flutter wrapper](https://developers.google.com/youtube/gaming/playables/samples/flutter_wrapper)
- [Official web game samples](https://github.com/google/web-game-samples)
- [Stability and performance](https://developers.google.com/youtube/gaming/playables/certification/requirements_stability)

