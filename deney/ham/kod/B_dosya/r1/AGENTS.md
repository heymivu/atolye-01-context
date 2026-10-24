# notlar — ajan kuralları
Küçük komut satırı not defteri (Python 3.12, yalnız standart kütüphane). Dil: Türkçe.

## Kurallar (standart dışı; uy)
1. Tarih için `datetime.now()` ya da `date.today()` doğrudan çağrılmaz; her yerde `tarih.bugun()` kullanılır (testlerde sahte tarih için).
2. Ekrana `print` ile yazılmaz; `log.bilgi(...)` ve `log.hata(...)` kullanılır.
3. Test dosyasının adı `test_x.py` değil, `x_test.py` biçimindedir (örnek: `notlar_test.py`). Testler `python -m unittest` ile koşar.
4. Fonksiyon, değişken ve docstring Türkçe (örnek: `ekle`, `listele`, `etiket`). İngilizce tanımlayıcı eklenmez.
5. Yeni bağımlılık eklenmez (pip, requirements yok).

## Komutlar
- Çalıştır: `python notlar.py ekle "metin"` · `python notlar.py listele`
- Test: `python -m unittest notlar_test -v`

## Bitirince
- Testler geçmeli. `DURUM.md`'deki "Son yapılan iş" satırını güncelle.
