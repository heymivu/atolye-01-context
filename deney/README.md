# Deney: tek mesaj mı, üç dosya mı, yapay zekâya yazdırılmış dosya mı?

- `TASARIM.md`: soru, kollar, ölçüm, hipotezler.
- `girdiler/`: kurgusal Köşe Kahve TALIMAT, DURUM, ÖRNEKLER ve üç haftalık görev cümleleri.
- `puanla.py`: 8 kuralı makineyle sayar. Kullanım: `python puanla.py <cikti.md> <T1|T2|T3>`.
- `kod/`: yan deney (küçük not defteri reposu, 5 standart dışı kural, `kontrol.py`).
- `SONUC.md`: sonuçlar ve sınırlar.

Tekrar koşmak için: bir klasöre üç dosyayı koy, yapay zekâ aracına "önce bu dosyaları oku" de, görevleri sırayla ver, her çıktıyı `puanla.py` ile puanla.
- `ham/`: modelin bütün çıktıları, dokunulmadan: kafe deneyi (3 kurulum × 3 tekrar × 3 hafta) ve kod görevi (3 × 3). C kolunun 2.291 kelimelik talimatı `ham/kafe/C_ai_dosya/r1/TALIMAT.md`.
- `veri/`: koşu başına token (`token.csv`) ve kural puanları (`puanlar_v1.json`, `puanlar_v2.json`).

← [Ana sayfa](../README.md)
