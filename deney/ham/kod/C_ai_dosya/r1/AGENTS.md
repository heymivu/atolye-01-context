# notlar — Yapay Zekâ Kodlama Ajanı Rehberi

Bu belge, projeye yeni gelen bir yapay zekâ kodlama ajanının ilk gün ihtiyaç duyacağı her şeyi tek yerde toplar. İşe başlamadan önce baştan sona oku. Proje küçüktür, ama kuralları sıradışıdır; bu kurallar çoğu genel alışkanlıkla çelişir. Alışkanlıkla yazdığın kod, bu projede hatalı sayılır.

## 1. Proje amacı

`notlar`, Python 3.12 ile yazılmış küçük bir komut satırı not defteridir. Kullanıcı terminalden bir not ekler, sonra notları tarih sırasıyla listeler. Notlar, betiğin yanındaki `notlar.json` dosyasında saklanır. Projenin dili Türkçedir: kod, docstring, mesajlar ve bu belge Türkçe yazılır.

Projenin amaçları şunlardır:

- Çok az kodla, anlaşılır ve test edilebilir bir araç sunmak.
- Yalnızca Python standart kütüphanesini kullanmak; kurulum gerektirmemek.
- Küçük kuralların (tek kapıdan tarih, tek kapıdan çıktı) disiplinle uygulandığı örnek bir kod tabanı olmak.

Projenin amacı olmayan şeyler: grafik arayüz, ağ erişimi, eşzamanlı çok kullanıcılı kullanım, veritabanı, paket olarak yayımlanma. Bunları kendiliğinden ekleme.

## 2. Standart dışı kurallar (uyulması zorunlu)

Aşağıdaki beş kural pazarlık konusu değildir. Her değişiklikte kontrol et.

1. **Tarih tek kapıdan alınır.** Kod içinde `datetime.now()` veya `date.today()` doğrudan çağrılmaz. Her yerde `tarih.bugun()` kullanılır. Bunun nedeni, testlerde sahte tarih verebilmektir. Gerçek `date.today()` çağrısı yalnızca `tarih.py` içinde bulunabilir.
2. **Ekrana `print` ile yazılmaz.** Bilgi için `log.bilgi(...)`, hata için `log.hata(...)` kullanılır. `print`, `sys.stdout.write` ve `sys.stderr.write` çağrıları yalnızca `log.py` içinde bulunur.
3. **Test dosyası adı `x_test.py` biçimindedir.** `test_x.py` biçimi kullanılmaz. Örnek: `notlar_test.py`. Testler `python -m unittest` ile çalışır; pytest kullanılmaz.
4. **Tanımlayıcılar ve docstring'ler Türkçedir.** Fonksiyon, değişken ve docstring Türkçe yazılır (örnek: `ekle`, `listele`, `etiket`). Koda İngilizce tanımlayıcı eklenmez.
5. **Yeni bağımlılık eklenmez.** `pip` yok, `requirements.txt` yok. Yalnızca standart kütüphane.

### Kuralların gerekçesi ve sınırı

- Kural 1 ve 2, test edilebilirlik içindir: tarih ve çıktı tek noktadan geçtiği için testte kolayca değiştirilebilir ya da yakalanabilir.
- Kural 3 ve 4, projenin tutarlı bir kimliği olsun diye vardır. "Daha yaygın olan" biçime geçmek için gerekçe sayılmaz.
- Kural 5, projenin kurulumsuz çalışmasını korur. Bir ihtiyaç standart kütüphaneyle karşılanamıyorsa dur ve kullanıcıya sor; kendin bağımlılık ekleme.

## 3. Komutlar

- Not ekle: `python notlar.py ekle "metin"`
- Notları listele: `python notlar.py listele`
- Testleri koştur: `python -m unittest notlar_test -v`

Komutları proje klasörünün içinden çalıştır. `notlar.py`, `tarih` ve `log` modüllerini aynı klasörden içe aktarır; başka bir dizinden çalıştırırsan içe aktarma başarısız olabilir.

## 4. Mimari ve dosya dosya açıklama

Mimari bilerek düzdür: bir ana modül, iki yardımcı modül, bir test dosyası. Katman, sınıf hiyerarşisi veya eklenti sistemi yoktur.

### `notlar.py` — ana modül

İşin tamamı burada yapılır. İçeriği:

- `DOSYA`: `notlar.json` dosyasının mutlak yolu. Modülün bulunduğu klasörden `os.path` ile hesaplanır. Çalışma dizininden bağımsızdır. Testler bu değişkeni geçici bir dosyaya yönlendirir; bu yüzden diğer işlevler dosya yolunu sabit yazmamalı, her zaman `DOSYA` değişkenini okumalıdır.
- `oku()`: Not listesini dosyadan okur. Dosya yoksa boş liste döner. Dosya bozuksa şu an `json.load` hatası yükselir (bkz. hata yönetimi).
- `yaz(notlar)`: Not listesini UTF-8 olarak ve `ensure_ascii=False`, `indent=1` ile yazar. Türkçe karakterler olduğu gibi saklanır.
- `ekle(metin)`: Listeyi okur, `{"tarih": tarih.bugun(), "metin": metin}` kaydını ekler, yazar ve `log.bilgi` ile bildirir.
- `listele()`: Tüm notları dosyadaki sıraya göre (ekleme sırası, yani tarih sırası) `log.bilgi` ile yazar. Biçim: `TARİH  METİN` (iki boşlukla ayrılmış).
- `ana(argv)`: Komut satırı girişi. `ekle` için en az bir metin parçası bekler ve parçaları boşlukla birleştirir. `listele` için ek argüman istemez. Tanınmayan veya eksik komutta `log.hata` ile kullanım mesajı yazar ve `1` döner; başarıda `0` döner.
- `if __name__ == "__main__"` bloğu: `sys.exit(ana(sys.argv[1:]))` çağırır. Çıkış kodu böylece kabuğa iletilir.

### `tarih.py` — tarih kapısı

- `SABIT`: Varsayılanı `None`. Doluysa (örnek: `"2026-01-02"`) `bugun()` onu döner. Yalnızca testler değiştirir.
- `bugun()`: `SABIT` doluysa onu, değilse `datetime.date.today().isoformat()` değerini (YYYY-MM-DD) döner.

Bu modülde başka tarih işlevi eklemen gerekirse (ör. tarih aralığı), gene burada ve gene `SABIT` mantığına uyumlu yaz.

### `log.py` — çıktı kapısı

- `bilgi(mesaj)`: Mesajı satır sonuyla stdout'a yazar.
- `hata(mesaj)`: Mesajın başına `HATA: ` ekleyip stderr'e yazar.

Bilgi ve hata ayrı akışlara gittiği için kabukta `2>` yönlendirmesiyle ayrılabilir. Bu davranışı bozma.

### `notlar_test.py` — testler

`unittest.TestCase` tabanlı `NotlarTesti` sınıfı vardır.

- `setUp`: `notlar.DOSYA` değerini klasördeki `_test_notlar.json` dosyasına çevirir, varsa eskisini siler ve `tarih.SABIT = "2026-01-02"` ayarlar.
- `tearDown`: Geçici dosyayı siler ve `tarih.SABIT` değerini `None` yapar.
- `test_ekle_ve_oku`: Bir not ekler; listede tek kayıt olduğunu, tarihin sahte tarih ve metnin beklenen metin olduğunu doğrular.

### `DURUM.md` — durum notu

Proje durumunu tutan kısa belge: son güncelleme tarihi, "Şu an", "Son yapılan iş" ve "Sıradaki" bölümleri. İş bitince "Son yapılan iş" satırı güncellenir.

### `AGENTS.md` — kısa kural dosyası

Projenin kısa kural özetidir. Bu belge onun ayrıntılı eşlenik sürümüdür; çelişki görürsen kısa `AGENTS.md` ve kod esastır, ardından bu belgeyi düzelt.

### `notlar.json` — veri (çalışma sırasında oluşur)

Depoda bulunması gerekmez; ilk `ekle` çağrısında oluşur. Kişisel not içerebileceği için sürüm denetimine alınmamalıdır (bkz. git akışı).

## 5. Veri biçimi

`notlar.json`, bir JSON dizisidir. Her eleman iki alanlı bir nesnedir:

```json
[
 {
  "tarih": "2026-01-02",
  "metin": "süt al"
 }
]
```

- `tarih`: ISO 8601 tarih dizgisi, `YYYY-MM-DD`.
- `metin`: Serbest metin; Türkçe karakterler kaçışsız saklanır.
- Dosya UTF-8 kodludur. Girinti 1 boşluktur (`indent=1`). Bu biçimi değiştirme; mevcut dosyalarla uyumu bozar.
- Boş liste `[]` geçerlidir. Dosyanın hiç olmaması da "not yok" anlamına gelir.
- Sıra: kayıtlar eklenme sırasıyla tutulur, `listele` ek sıralama yapmaz.

### Şema değişikliği kuralı

Yeni alan eklenecekse (ör. `etiket`, sıradaki iş), eski kayıtlarla uyumlu olacak biçimde yap: eski kayıtlarda alan bulunmayabilir, okurken `n.get("etiket", [])` gibi varsayılan kullan. Dosyayı toplu dönüştüren bir göç betiği yazmadan önce kullanıcıya sor.

## 6. Kodlama standartları

- Python 3.12; yalnızca standart kütüphane.
- Her dosya `# -*- coding: utf-8 -*-` satırıyla başlar (mevcut dosyalar gibi).
- Dosyaları `open(..., encoding="utf-8")` ile aç; kodlamayı asla varsayılana bırakma (Windows'ta varsayılan farklıdır).
- Her modülün ve her işlevin Türkçe, tek satırlık bir docstring'i olur.
- Adlandırma: küçük harf, gerekirse alt çizgi; Türkçe sözcükler (`ekle`, `listele`, `oku`, `yaz`, `etiket`). Türkçe karakterli tanımlayıcıdan kaçın; ASCII karşılığını yaz (ör. `sayi`, `silinen`), çünkü mevcut kod da böyledir.
- Dizgi biçimlendirmede mevcut kodla tutarlı ol (`%` biçimi kullanılıyor). Tutarlılık yeni biçim denemekten önemlidir.
- Küçük işlevler yaz. Bir işlev tek iş yapsın; G/Ç (`oku`, `yaz`) ile iş mantığı (`ekle`) ayrı kalsın.
- Yeni modül eklemek yerine mevcut modüle işlev eklemeyi, ancak modül belirgin biçimde şişerse yeni modül açmayı tercih et.
- Gereksiz soyutlama, sınıf veya tasarım deseni getirme. Bu bir 60 satırlık araçtır.

## 7. Hata yönetimi

Mevcut davranış sade ve bilinçlidir:

- Komut hatası (bilinmeyen komut, eksik argüman): `log.hata` ile kullanım mesajı, çıkış kodu `1`.
- Dosya yoksa: sessizce boş liste.
- Bozuk JSON: şu an `json.JSONDecodeError` yükselir ve program iz çıktısıyla düşer. Bunu iyileştirmek istersen: hatayı yakala, `log.hata` ile anlaşılır bir mesaj yaz, dosyayı **silme veya üzerine yazma**, çıkış kodu `1` ile bitir.
- Yazma hataları (izin, disk dolu): şu an yükselir. İyileştirirken kısmi yazılmış dosya riskini düşün (bkz. performans ve güvenilirlik).

Kurallar:

- Hata mesajlarını `log.hata` ile yaz; `print` veya doğrudan `sys.stderr` kullanma.
- Boş `except:` yazma; yakaladığın hata türünü belirt.
- Kullanıcı verisini kaybettirecek hiçbir hata yolu bırakma. Şüphede kalırsan dosyaya dokunmadan hata ver.
- Çıkış kodları: `0` başarı, `1` kullanım/genel hata. Yeni kodlar eklersen belgele.

## 8. Test stratejisi

- Çerçeve: `unittest`. Dosya adı `x_test.py`. Koşum: `python -m unittest notlar_test -v`.
- Testler gerçek `notlar.json` dosyasına asla dokunmaz. `setUp` içinde `notlar.DOSYA` değiştirilir ve `tearDown` içinde geçici dosya silinir. Yeni testler aynı kalıbı izler.
- Tarih gerektiren her test `tarih.SABIT` kullanır ve `tearDown` içinde `None` yapar. Gerçek tarihe bağlı test yazma.
- Çıktı testleri: `log` çıktısını doğrulaman gerekirse `unittest.mock.patch` ile `sys.stdout`/`sys.stderr` yakala (standart kütüphane, kural 5'e uygun).
- Her yeni işlev için en az bir olumlu ve bir olumsuz/uç durum testi ekle: boş liste, dosya yok, Türkçe karakterli metin, birden fazla not, eksik argüman.
- Test adları `test_` ile başlar ve Türkçe anlatır (`test_ekle_ve_oku`).
- Bir hatayı düzeltirken önce hatayı yeniden üreten başarısız bir test yaz, sonra düzelt.
- Birleştirmeden önce tüm test paketi geçmelidir. Başarısız testi silerek ya da gevşeterek "geçirme".

## 9. Git akışı

Depoda özel bir dal kuralı belgelenmemiştir; makul varsayılanlar:

- Küçük, tek amaçlı değişiklikler yap; her commit tek bir işi anlatsın.
- Commit mesajı Türkçe, kısa ve eylem odaklı olsun (ör. "Etiket alanı eklendi").
- Commit'ten önce testleri koştur; geçmiyorsa commit etme.
- `notlar.json` ve `_test_notlar.json` dosyaları `.gitignore` içinde olmalıdır; kişisel veri depoya girmesin. Yoksa ekle ve kullanıcıya söyle.
- Push, dal silme, geçmiş yeniden yazma gibi geri dönüşü zor işlemleri kullanıcı açıkça istemeden yapma.
- İş bitince `DURUM.md` değişikliği de aynı commit'e girer.

## 10. Güvenlik notları

- Tüm veri yereldir; ağ erişimi yoktur ve eklenmemelidir.
- `notlar.json` düz metindir; şifre, anahtar veya kimlik bilgisi saklama. Kullanıcı yanlışlıkla yazarsa bu proje onu korumaz.
- Kullanıcı girdisini asla `eval`, `exec`, `os.system` veya `subprocess` ile çalıştırma. Girdi yalnızca veri olarak JSON'a yazılır.
- Dosya yolu, sabit `DOSYA` değişkeninden gelir; kullanıcıdan yol kabul eden bir özellik eklenecekse yol geçişi (`..`) ve beklenmeyen konumlara yazma risklerini düşün ve sor.
- JSON'u yalnızca `json` modülüyle oku; `pickle` kullanma.
- Hata mesajlarına gereksiz iç ayrıntı (tam yol, kullanıcı adı) koyma.
- Kodda gizli bilgi, anahtar veya kişisel veri bulundurma; test verileri yapay olmalıdır.

## 11. Performans ve güvenilirlik notları

- Mevcut yaklaşım: her işlemde dosyanın tamamı okunur ve tamamı yazılır. Bin düzeyindeki notlar için sorun yoktur. Erken optimizasyon yapma.
- `ekle` oku-değiştir-yaz döngüsüdür ve atomik değildir. İki işlem aynı anda çalışırsa son yazan kazanır; bu bilinen bir sınırdır. Tek kullanıcılı bir araç için kabul edilmiştir.
- Yazma sırasında program kesilirse dosya yarım kalabilir. İyileştirme gerekirse: geçici dosyaya yaz, sonra `os.replace` ile yerine koy (standart kütüphane, atomik).
- `listele` her seferinde hepsini yazar. Sayfalama veya filtre gerekene kadar bu böyle kalır.
- Başlangıç süresi önemlidir: ağır içe aktarma ekleme. Şu an yalnızca `json`, `os`, `sys` ve `datetime` kullanılır.

## 12. Sık yapılan hatalar

Yeni ajanların en çok düştüğü tuzaklar:

1. `date.today()` veya `datetime.now()` yazmak. Doğrusu `tarih.bugun()`.
2. Hata ayıklarken `print` bırakmak. Doğrusu `log.bilgi`/`log.hata`; ve bırakmamak.
3. Test dosyasını `test_notlar.py` diye adlandırmak. Doğrusu `notlar_test.py`.
4. İngilizce tanımlayıcı veya docstring yazmak (`add_note`, `"""Reads notes."""`).
5. `pytest`, `click`, `rich`, `requests` gibi paketleri eklemek, `requirements.txt` oluşturmak.
6. Testte gerçek `notlar.json`'u kullanmak ya da `tarih.SABIT` değerini `tearDown` içinde sıfırlamamak; sonraki testleri bozar.
7. `open()` çağrısında `encoding="utf-8"` unutmak; Windows'ta Türkçe karakterler bozulur.
8. Dosya yolunu sabit yazmak; testin yönlendirmesi çalışmaz. Her zaman `DOSYA` kullan.
9. Betiği başka dizinden çalıştırıp içe aktarma hatası almak.
10. `ensure_ascii` ve `indent` ayarlarını değiştirip veri biçimini bozmak.
11. Kök neden yerine belirtiyi gidermek; ör. başarısız testi silmek.
12. Kapsam dışına çıkmak: istenmeyen yeniden düzenleme, ek özellik, biçim değişikliği.

## 13. Sık sorulan sorular

**Neden `print` yasak?** Çıktının tek noktadan geçmesi, testte yakalamayı, ileride biçim veya dosya günlüğü eklemeyi kolaylaştırır.

**Neden `x_test.py`?** Projenin bilinçli adlandırma kararıdır. Test dosyası, sınadığı modülün adının yanında alfabetik olarak durur. Tartışmak yerine uygula.

**Yeni modül açabilir miyim?** Evet, gerekirse; ama önce mevcut modüllerde çözüm ara. Yeni modül de Türkçe adlı olmalı, aynı kurallara uymalı ve test dosyası `modul_test.py` olmalıdır.

**İngilizce bir kütüphane anahtar sözcüğü ya da standart ad kaçınılmaz olduğunda?** Dilin kendi sözcükleri (`def`, `return`) ve standart kütüphane adları (`json.load`) elbette kullanılır; kural, bizim tanımladığımız adları kapsar.

**Bir özellik için paket gerekiyorsa?** Standart kütüphaneyle çözmeye çalış (`argparse`, `json`, `os`, `unittest.mock`). Olmuyorsa dur ve kullanıcıya sor.

**Çıktı biçimini değiştirebilir miyim?** Kullanıcı istemedikçe hayır; `listele` çıktısı betiklerle okunuyor olabilir.

**Testler nerede koşar?** Proje klasöründe: `python -m unittest notlar_test -v`.

**Belge ile kod çelişirse?** Önce kısa `AGENTS.md` ve çalışan kodu esas al, sonra belgeyi düzelt ve kullanıcıya bildir.

## 14. İleride planlanan özellikler

`DURUM.md`'ye göre sıradaki iş **etiket özelliğidir**. Aşağıdakiler yön gösterir; kullanıcı istemeden başlama.

- **Etiket**: Nota bir veya birden çok etiket eklemek (ör. `ekle "metin" --etiket alisveris`), `listele` ile etikete göre süzmek. Veri biçimine isteğe bağlı `etiket` alanı eklenir (bkz. şema değişikliği kuralı). Komut satırı ayrıştırması büyürse `argparse` kullanılabilir (standart kütüphane).
- **Sil / tamamla**: Not silme veya tamamlandı işareti; silme işlemi için onay ya da geri alma düşünülmeli.
- **Arama**: Metinde sözcük arama.
- **Tarihe göre süzme**: Belirli gün veya aralık; `tarih` modülünde, `SABIT` ile uyumlu.
- **Güvenli yazma**: Geçici dosya + `os.replace`.
- **Bozuk dosya yönetimi**: Anlaşılır hata ve yedekten kurtarma.

Her özellik: önce test, sonra kod, sonra `DURUM.md`.

## 15. Kontrol listeleri

### Başlamadan önce

- [ ] `AGENTS.md`, `DURUM.md` ve bu belgeyi oku.
- [ ] İlgili modülü ve `notlar_test.py` dosyasını oku.
- [ ] Mevcut testleri koştur; başlangıçta yeşil olduklarını doğrula.
- [ ] İsteğin kapsamını ve hangi dosyaların değişeceğini belirle.

### Kod yazarken

- [ ] Tarih için yalnızca `tarih.bugun()` kullanıldı.
- [ ] Çıktı için yalnızca `log.bilgi` / `log.hata` kullanıldı; `print` yok.
- [ ] Tanımlayıcılar ve docstring'ler Türkçe.
- [ ] Yeni bağımlılık yok.
- [ ] Dosya işlemlerinde `encoding="utf-8"` ve `DOSYA` değişkeni kullanıldı.
- [ ] Gereksiz kapsam genişlemesi yok.

### Test yazarken

- [ ] Dosya adı `x_test.py` biçiminde.
- [ ] `setUp`/`tearDown` ile gerçek veri korunuyor, `tarih.SABIT` sıfırlanıyor.
- [ ] Olumlu ve uç durum testleri var.
- [ ] `python -m unittest notlar_test -v` tümüyle geçiyor.

### Bitirirken

- [ ] Testler geçiyor.
- [ ] `DURUM.md` içindeki "Son yapılan iş" satırı ve gerekirse "Şu an"/"Sıradaki" güncellendi.
- [ ] `grep` ile `print(`, `date.today`, `datetime.now` kalıntısı kontrol edildi (yalnızca `tarih.py` ve `log.py` içinde olabilir).
- [ ] Geçici dosyalar (`_test_notlar.json`, `notlar.json`) commit'e girmiyor.
- [ ] Kullanıcıya ne yaptığını, neyi doğruladığını ve neyin yapılmadığını kısaca bildir.

## 16. Çalışma tarzı hakkında son notlar

- Kısa ve doğrudan çalış; kullanıcıyla Türkçe konuş.
- Emin olmadığın ayrıntıyı uydurma; koda bak, gerekirse sor.
- Bu belgedeki "makul varsayılan" ifadeleri projenin kesin kararı değildir; kullanıcı aksini söylerse onu izle.
- Küçük, doğrulanmış adımlarla ilerle: değiştir, test et, kaydet.
