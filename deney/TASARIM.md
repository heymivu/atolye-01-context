# Deney tasarımı — "Tek prompt mu, üç dosya mı, yapay zekâya yazdırılmış dosya mı?"

Tarih: 2026-10-18. Model: tüm kollarda aynı (Claude Sonnet 5.5, alt ajan olarak; sıcaklık varsayılan). Tekrar: her kol × her görev 3 kez.

## Soru
Aynı iş, aynı model. Bağlam üç biçimde verilirse kural uyumu, süreklilik (önceki haftanın kararlarını hatırlama), düzeltme ihtiyacı ve token maliyeti nasıl değişir?

## İş: kurgusal "Köşe Kahve" (Kadıköy) için haftalık Instagram planı + 3 gönderi
Üç ardışık görev (üç hafta):
- **T1** İlk haftanın planı + 3 gönderi.
- **T2** "Bu hafta Pazartesi tadilat, kapalıyız; planı ona göre değiştir." + 3 gönderi.
- **T3** "Yeni ürün geldi: badem sütlü latte. Bu haftanın planı + 3 gönderi." (Pazartesi hâlâ kapalı: yalnız T2'de söylendi; süt kuralı değişti: güncellenmeli.)

## Kollar
| Kol | Bağlam nasıl veriliyor | Her görevde |
|---|---|---|
| **A Tek prompt** | Marka bilgisi, kurallar, geçmiş gönderiler ve görev tek uzun mesajda | Yeni oturum; kullanıcı aynı uzun metni yapıştırır + görevi ekler (gerçek kullanım: insanlar sohbeti yeniden başlatır, önceki haftanın kararını tekrar yazmayı unutur) |
| **B Üç dosya (insan yazımı)** | `TALIMAT.md` (kim, ton, 8 kural) + `DURUM.md` (nerede kaldık) + `ORNEKLER.md` (3 eski gönderi) | Yeni oturum; ajan önce üç dosyayı okur, işi yapar, **DURUM.md'yi günceller** (bir sonraki hafta için) |
| **C Üç dosya, TALIMAT yapay zekâya yazdırılmış** | B ile aynı, ama TALIMAT.md yerine aynı bilgiden yapay zekânın ürettiği "kapsamlı" uzun dosya | B ile aynı protokol |

A kolunda T2/T3 isteği aynı kısa cümle; kullanıcı Pazartesi bilgisini T3'te tekrar yazmaz (gerçekçi). B/C'de bu bilgi DURUM.md'de durur (ajan yazdıysa).

## Ölçüm (makineyle; `puanla.py`)
Her gönderi için 8 kural (TALIMAT.md'de aynı sırayla):
1. Yasak kelime yok: indirim, kampanya, bedava, ücretsiz, % işareti, promosyon, hediye
2. Üstünlük iddiası yok: "en iyi", "en lezzetli", "en güzel", "Türkiye'nin", "eşsiz", "mükemmel", "muhteşem"
3. En fazla 1 emoji
4. Son cümle soru (metin "?" ile biter)
5. 30–80 kelime (hashtag'ler hariç)
6. Tam 3 hashtag ve biri #KöşeKahve
7. "Siz" hitabı: "sen", "senin", "sana" yok
8. Süt bilgisi doğru: T1–T2'de "badem" geçmez; T3'te "sadece inek ve yulaf" tarzı eski ifade geçmez
Plan için: T2 ve T3'te Pazartesi'ye gönderi/konu konmamış (süreklilik). Biçim: "## Plan" tablosu + "## Gönderi 1/2/3".
Ek: düzeltme turu (ihlal varsa tek düzeltme mesajı, sonra yeniden puan; 0/1), token (alt ajan kullanım raporundan).

## Hipotezler (önceden yazıldı; sonuç ne çıkarsa o)
- H1: T1'de A ≈ B (bilgi eşit). H2: T2–T3'te B > A (süreklilik: Pazartesi, süt güncellemesi). H3: C, B'den daha fazla token harcar ve kural uyumu B'den yüksek değildir (ETH/ICLR 2026 bulgusu). Çürütülürse videoda söylenir.

## Sınırlar
Tek model ailesi; kurgusal iş; alt ajan = Claude Code ile aynı model ama arayüz değil (çekimde gerçek Claude Code kullanılacak, sayılar bu deneyden). ChatGPT Projects kodsuz gösterim için, ölçüme dahil değil.
