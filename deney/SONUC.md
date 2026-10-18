# Deney sonucu — tek prompt / üç dosya / yapay zekâya yazdırılmış dosya (2026-10-18)

Model: tüm kollarda Claude Sonnet 5.5 (alt ajan). Tasarım: `TASARIM.md`. Puanlama makineyle (`puanla.py`, `kod/kontrol.py`), çelişki durumları elle etiketlendi.
Koşu sayısı: kafe v1 27 + kafe v2 24 + kod 9 = **60 koşu**. v1'de T2 "bu hafta Pazartesi" dediği için süreklilik ölçümü belirsizdi; v2'de "önümüzdeki üç hafta Pazartesileri" denip T2–T3 yeniden koşuldu. Aşağıdaki sonuçlar **v2** ve **kod** deneyinden; v1 yalnız kural uyumu ve token için sayıldı.

## 1. Kural uyumu (8 kural × 3 gönderi, her koşuda)
| | A tek prompt | B üç dosya (insan) | C üç dosya (AI şişkin) |
|---|---|---|---|
| T1 (3 tekrar) | 0 ihlal | 0 | 0 |
| T2 | 0 | 0 | 0 |
| T3 | 0 | 0 | 0 |
| Kod görevi (5 kural + test) | 0 ihlal, 3/3 test geçti | 0, 3/3 | 0, 3/3 |
**Bulgu 1:** Kısa ve net 8 kural, nerede durursa dursun uygulandı. "Sihirli prompt" da, "sihirli dosya" da yok. Kuralları bir kez net yazmak yetiyor.

## 2. Süreklilik: 3. haftada Pazartesi hâlâ kapalı mı? (yalnız T2'de söylendi)
| | A | B | C |
|---|---|---|---|
| Pazartesi'yi kapalı tuttu | **0/3** | **3/3** | **3/3** |
A'nın üçünde de Pazartesi'ye "badem sütlü latte duyurusu" kondu: kapalı günde gönderi. B ve C'de DURUM.md'ye T2'de yazılan "üç Pazartesi kapalı" satırı okundu, plan ona göre kuruldu.
**Bulgu 2 (videonun omurgası):** Prompt'un öldüğü yer bu. Her hafta aynı uzun metni yapıştıran kullanıcı geçen haftanın kararını taşımıyor; 10 satırlık bir DURUM dosyası taşıyor. "Yapay zekâ seni her seferinde unutuyor" sorununun çözümü hafıza değil, dosya.

## 3. Çelişki: "Yeni ürün: badem sütlü latte" vs dosyadaki "süt: yalnız inek ve yulaf"
| | A | B | C |
|---|---|---|---|
| Badem'i yazdı | **3/3** (v2: 1'i altına "menüde sayıldı, teyit edilmeli" notu düştü, 2'si sessiz; v1'de 1'i gizli HTML yorumu) | 0/3 | 0/3 |
| Yazmadı, çıktıda görünür notla sordu | — | **3/3** | 0/3 |
| Yazmadı, uyarıyı yalnız DURUM.md'ye yazdı ("ÇELİŞKİ / AÇIK SORU"; çıktıda sessiz) | — | — | **3/3** |
**Bulgu 3:** Dosyadaki kural, sohbetteki yeni bilgiye karşı kazanıyor. B güvenli ama bloke ediyor ("Ayşe onaylasın"); C hem bloke ediyor hem söylemiyor (kullanıcı çıktıya bakınca badem yok, neden yok belli değil). A kullanıcıyı dinledi ama marka kuralını sessizce çiğnedi.
Ders: bağlam dosyası **canlı belge**. Kural değişiyorsa sohbette söyleme, dosyayı güncelle (TALIMAT'a "badem sütü eklendi" yaz). Bu, atölyede gösterilecek "doğru kullanım" anı.

## 4. Maliyet (alt ajan toplam token; sistem istemi dâhil, kollar arası kıyas için)
| | A | B | C | C / B |
|---|---|---|---|---|
| Kafe v2 ortalama | ~72.000 | ~75.300 | ~85.300 | **+%13** |
| Kafe v1 ortalama | ~70.700 | ~74.600 | ~86.700 | **+%16** |
| Kod görevi | ~72.700 | ~73.400 | ~88.500 | **+%20** |
İnsan yazımı 3 dosya (B) tek prompt'tan ~%4 pahalı (dosya okuma araç çağrıları). AI yazımı şişkin dosya (C) B'den %13–20 pahalı, çıktı daha iyi değil.
**Bulgu 4:** ICLR 2026 (Gloaguen ve ark.) bulgusuyla uyumlu: yapay zekâya yazdırılan bağlam dosyası maliyeti ~%20 artırır, başarıyı artırmaz.

## 5. Kod deneyinde kapsam taşması (C kolu)
C r1 istenmeyen `.gitignore` ekledi (şişkin AGENTS.md'de "git akışı" bölümü vardı); C kolu 7–10 test yazdı, A/B 5. Sonuç aynı, iş fazla.
**Bulgu 5:** Şişkin dosya ajanı "daha çok şey yapmaya" itiyor; istenmeyen iş = gözden geçirme yükü.

## 6. Hipotez karnesi
- H1 (T1'de A ≈ B): **doğrulandı.**
- H2 (T2–T3'te B > A süreklilikte): **doğrulandı** (3/3 vs 0/3).
- H3 (C, B'den pahalı, uyum daha yüksek değil): **doğrulandı** (+%13–20; uyum eşit; çelişkide daha kötü: sessiz).
- Beklenmeyen: dosya kuralının yeni bilgiye karşı "kazanması" (Bulgu 3). Videoda bunu saklamıyoruz; tam tersine ders bu.


## Sınırlar
Tek model ailesi; kurgusal iş; 3 tekrar; modeller yazılımla çağrıldı (sohbet arayüzü değil); token sayıları sistem istemi dâhil, mutlak değil göreli okunmalı; süreklilik ölçümü ilk sürümde tasarım hatası nedeniyle geçersizdi, ikinci sürümde düzeltildi.
