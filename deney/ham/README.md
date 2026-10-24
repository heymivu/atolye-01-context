# Ham çıktılar

Modelin deneyde ürettiği her şey, olduğu gibi (düzeltilmedi, kısaltılmadı). Sonuç tabloları [`../SONUC.md`](../SONUC.md)'de.

## `kafe/` — Köşe Kahve, üç hafta Instagram planı (deneyin 2. turu)
- `A_prompt/` tek uzun mesaj: her hafta yeni sohbet, aynı metin. Dosya yok, yalnız çıktılar.
- `B_dosya/` üç kısa dosya (insan yazımı): `TALIMAT.md`, `DURUM.md`, `ORNEKLER.md`. `DURUM.md` koşu sonundaki hâli; model her işten sonra kendisi güncelledi.
- `C_ai_dosya/` aynı üç dosya, ama talimatı yapay zekâ yazdı (2.291 kelime).
- Her kolda `r1`–`r3` üç bağımsız tekrar; `cikti_T1/T2/T3.md` birinci, ikinci, üçüncü haftanın çıktısı.
- Görevler: [`../girdiler/gorevler.md`](../girdiler/gorevler.md). İkinci haftanın mesajı ilk turda "bu hafta Pazartesi kapalıyız" idi; tek haftalık okunabildiği için "önümüzdeki üç hafta Pazartesileri kapalıyız" yapılıp ikinci ve üçüncü hafta yeniden koşuldu. A kolunun birinci hafta çıktıları ilk turdan (A'da dosya olmadığından birinci hafta iki turda aynı).
- Model bazı notlarda kafe sahibi Ayşe'nin yanında deneyi yürüten kişinin adını da anıyor; metne dokunulmadı.

## `kod/` — küçük not defteri reposu, aynı istek
Her kolda `r1`–`r3`: koşu sonundaki kod ve (B, C'de) `AGENTS.md` / `DURUM.md`. Başlangıç hâli ve `kontrol.py`: [`../kod/`](../kod/).

← [Deney](../README.md)
