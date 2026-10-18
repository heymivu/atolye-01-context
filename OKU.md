# Bağlam şablonu: yapay zekâ seni her seferinde unutmasın

Mivu Atölye 1'in dosyaları. Video: "Yapay Zekâ Seni Her Seferinde Unutuyor. 3 Dosya Bunu Bitiriyor." (bağlantı yayından sonra eklenecek)

Fikir basit: her sohbette her şeyi baştan anlatma. Üç kısa dosya yaz, yapay zekâ her seferinde önce onları okusun.

| Dosya | Ne işe yarar | Uzunluk |
|---|---|---|
| Talimat | Kimsin, nasıl konuşursun, kurallar, yapma listesi | 20–200 satır |
| Durum | Nerede kaldık, bu hafta ne değişti, sırada ne var. **Her işten sonra güncellenir.** | ~10 satır |
| Örnekler | 2–3 gerçek iyi çıktı (ton ve biçim için) | kısa |

## Hangi klasör senin için?

### Kod yazmıyorum (ChatGPT / Claude Projects) → `kodsuz/`
10 dakikalık kurulum: `kodsuz/KURULUM.md`.
1. ChatGPT'de ya da Claude'da yeni bir **proje** aç.
2. `Proje-Talimati.md` içeriğini doldur, projenin talimat alanına yapıştır.
3. `Durum-Notu.md` ve `Ornekler.md` dosyalarını doldur, projeye dosya olarak yükle.
4. Her sohbetin sonunda şunu yaz: **"Durum notunu bu sohbete göre güncelle, tamamını ver."** Çıkan metni eski `Durum-Notu.md`'nin yerine yükle.
   Projects'te yapay zekâ dosyayı kendisi değiştiremez; bu bir dakikalık adım senin.

### Kod yazıyorum (Claude Code, Codex, Cursor, Copilot…) → `kodlu/`
1. `kodlu/` içindekileri projenin köküne kopyala.
2. `AGENTS.md`'yi doldur (komutlar, kurallar, yapma listesi). 200 satırın altında tut.
3. `CLAUDE.md` tek satır: `@AGENTS.md`. Claude Code, aynı klasörde CLAUDE.md varsa AGENTS.md'yi kendiliğinden okumaz; bu satır ikisini bağlar.
4. Ajan her oturumda `Durum.md`'yi ve `Handoff.md`'nin son girdilerini okur, iş bitince günceller (AGENTS.md'de yazdığı için).

## Beş kural
1. **Kısa.** Her satıra sor: bunu silersem model hata yapar mı? Yapmazsa sil.
2. **Ölçülebilir.** "Güzel yaz" değil; "en fazla bir emoji", "her gönderi soruyla biter".
3. **Durum notu.** On satır, her işten sonra güncellenir. Hatırlamanın kendisi bu.
4. **Örnek.** Üç gerçek çıktı, uzun tariften iyidir.
5. **Yapma listesi.** Yasaklar, sınırlar, dokunulmayacak dosyalar.

Ve bir alışkanlık: **bir şey değiştiğinde sohbete değil dosyaya yaz.**

## Bunu yapay zekâya yazdırma
"Bana kapsamlı bir talimat dosyası yaz" deme. Denememizde yapay zekâya yazdırılan 2.300 kelimelik dosya kurallara daha iyi uymadı, %13–20 daha fazla token harcadı ve çelişkiyi çıktıda söylemedi. Kısa yaz, kendin yaz.

## Deney
`deney/` klasöründe videodaki kafe deneyinin girdileri, puanlayıcısı ve sonuç raporu var. Kendin tekrar koşabilirsin.

## Lisans
Kod ve betikler MIT (`LICENSE`). Şablon metinleri CC BY 4.0: kullan, değiştir, kaynak göster.
