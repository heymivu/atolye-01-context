# Yapay zekâ seni her seferinde unutmasın: 3 dosyalık bağlam şablonu

**Mivu Atölye 1** · Video: *yayında bağlantı eklenecek*

Her yeni sohbette yapay zekâya her şeyi baştan anlatıyorsan, sorun prompt'ta değil. Bu repo, hatırlamayı **üç kısa dosyaya** devretmen için hazır şablonlar ve videodaki deneyin tüm dosyalarını içeriyor.

| Dosya | Ne işe yarar | Uzunluk |
|---|---|---|
| **Talimat** | Kimsin, nasıl konuşursun, kurallar, yapma listesi | 20–200 satır |
| **Durum** | Nerede kaldık, bu hafta ne değişti, sırada ne var. *Her işten sonra güncellenir.* | ~10 satır |
| **Örnekler** | 2–3 gerçek iyi çıktı (ton ve biçim için) | kısa |

---

## Hangi klasör senin için?

### Kod yazmıyorum → [`kodsuz/`](kodsuz/)
ChatGPT Projeler veya Claude Projects ile **10 dakikada kurulum**. Adımlar: [`kodsuz/KURULUM.md`](kodsuz/KURULUM.md)

1. Yeni bir **proje** aç.
2. [`Proje-Talimati.md`](kodsuz/Proje-Talimati.md)'yi doldur, projenin talimat alanına yapıştır.
3. [`Durum-Notu.md`](kodsuz/Durum-Notu.md) ve [`Ornekler.md`](kodsuz/Ornekler.md)'yi doldur, projeye dosya olarak ekle.
4. Her sohbetin sonunda yaz: **"Durum notunu bu sohbete göre güncelle, tamamını ver."** Çıkan metni eski durum notunun yerine yükle.

> Projects'te yapay zekâ proje dosyalarını kendiliğinden güncellemez. Bu bir dakikalık adım senin.

### Kod yazıyorum → [`kodlu/`](kodlu/)
Claude Code, Codex, Cursor, Copilot ve [AGENTS.md](https://agents.md) okuyan diğer araçlar için.

1. `kodlu/` içindekileri projenin köküne kopyala.
2. [`AGENTS.md`](kodlu/AGENTS.md)'yi doldur: komutlar, kurallar, yapma listesi. **200 satırın altında** tut.
3. [`CLAUDE.md`](kodlu/CLAUDE.md) tek satır: `@AGENTS.md`. Claude Code, aynı klasörde CLAUDE.md varsa yalnız onu okur; bu satır ikisini bağlar.
4. Ajan her oturumda `Durum.md`'yi ve `Handoff.md`'nin son girdilerini okur, iş bitince günceller.

```
kodlu/
├── AGENTS.md     kurallar (tüm araçlar okur)
├── CLAUDE.md     @AGENTS.md
├── Durum.md      şu an / sıradaki (yerinde güncellenir)
├── Handoff.md    oturum devir-teslim günlüğü
└── Dersler.md    tuzak defteri (2. kez olan kurala dönüşür)
```

---

## Beş kural

1. **Kısa.** Her satıra sor: *bunu silersem model hata yapar mı?* Yapmazsa sil.
2. **Ölçülebilir.** "Güzel yaz" değil; "en fazla bir emoji", "her gönderi soruyla biter".
3. **Durum notu.** On satır, her işten sonra güncellenir. Hatırlamanın kendisi bu.
4. **Örnek.** Üç gerçek çıktı, uzun tariften iyidir.
5. **Yapma listesi.** Yasaklar, sınırlar, dokunulmayacak dosyalar.

Ve bir alışkanlık: **bir şey değiştiğinde sohbete değil, dosyaya yaz.**

---

## Deneyde ne bulduk?

Kurgusal bir kafe için üç hafta boyunca Instagram planı yazdırdık. Aynı model, aynı istekler, üç kurulum, her biri üç tekrar. Ayrıntı: [`deney/`](deney/)

| | Tek uzun mesaj | 3 kısa dosya (insan yazımı) | 3 dosya (talimatı yapay zekâ yazdı, 2.300 kelime) |
|---|---|---|---|
| 8 kurala uyum | ihlal yok | ihlal yok | ihlal yok |
| 3. haftada "Pazartesi kapalı"yı hatırladı | **0 / 3** | **3 / 3** | **3 / 3** |
| Kuralla çelişen yeni istek | 3 / 3 kuralı çiğnedi | 3 / 3 yazmadı, açıkça sordu | 3 / 3 yazmadı, çıktıda söylemedi |
| Token (tek mesaja göre) | taban | %1–6 fazla | **%18–23 fazla** |

Kısacası: kısa ve net kurallara model her yerde uyuyor. Fark **süreklilikte**: geçen haftanın kararını mesaja eklemeyi unutursan model de unutur, dosyada yazılıysa unutmaz. Yapay zekâya yazdırılan uzun talimat dosyası daha iyi sonuç vermedi, daha pahalıya geldi.

> Sınırlar: tek model ailesi (Claude Sonnet 5.5, Ekim 2026), kurgusal iş, 3 tekrar. Ayrıntılar [`deney/SONUC.md`](deney/SONUC.md)'de.

---

## Bunu yapay zekâya yazdırma

"Bana kapsamlı bir talimat dosyası yaz" deme. Bizim denememizde de, 2026 tarihli bir araştırmada da (Gloaguen ve ark., ön baskı) yapay zekâya yazdırılan bağlam dosyaları başarıyı artırmadı, maliyeti artırdı. **Kısa yaz, kendin yaz.**

---

## Lisans

Kod ve betikler [MIT](LICENSE). Şablon metinleri [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): kullan, değiştir, kaynak göster.

*Mivu, yapay zekâyı anlatan küçük bir robot.* · YouTube / Instagram / TikTok / X: **@heymivu**
