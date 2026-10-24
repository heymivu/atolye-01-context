# -*- coding: utf-8 -*-
"""notlar: komut satırı not defteri. Notlar notlar.json dosyasında tutulur."""
import json, os, sys
import tarih, log

DOSYA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notlar.json")


def oku():
    """Not listesini dosyadan okur; dosya yoksa boş liste döner."""
    if not os.path.exists(DOSYA):
        return []
    with open(DOSYA, encoding="utf-8") as f:
        return json.load(f)


def yaz(notlar):
    """Not listesini dosyaya yazar."""
    with open(DOSYA, "w", encoding="utf-8") as f:
        json.dump(notlar, f, ensure_ascii=False, indent=1)


def ekle(metin, etiketler=()):
    """Yeni not ekler; tarih olarak tarih.bugun() kullanılır. Etiket isteğe bağlıdır."""
    notlar = oku()
    kayit = {"tarih": tarih.bugun(), "metin": metin}
    if etiketler:
        kayit["etiket"] = list(etiketler)
    notlar.append(kayit)
    yaz(notlar)
    log.bilgi("eklendi: %s" % metin)


def listele(etiket=None):
    """Notları tarih sırasıyla yazar; etiket verilirse yalnız o etiketliler."""
    for n in oku():
        if etiket is None or etiket in n.get("etiket", []):
            log.bilgi("%s  %s" % (n["tarih"], n["metin"]))


def etiketleri_ayir(argumanlar):
    """--etiket DEĞER çiftlerini ayırır; (etiketler, kalanlar) döner, değer eksikse None."""
    etiketler, kalan = [], []
    i = 0
    while i < len(argumanlar):
        if argumanlar[i] == "--etiket":
            if i + 1 >= len(argumanlar):
                return None
            etiketler.append(argumanlar[i + 1])
            i += 2
        else:
            kalan.append(argumanlar[i])
            i += 1
    return etiketler, kalan


KULLANIM = "kullanım: notlar.py ekle [--etiket ETİKET] \"metin\" | listele [--etiket ETİKET]"


def ana(argv):
    """Komut satırı girişi."""
    komut = argv[:1]
    ayrildi = etiketleri_ayir(argv[1:])
    if ayrildi is None or komut not in (["ekle"], ["listele"]):
        log.hata(KULLANIM)
        return 1
    etiketler, kalan = ayrildi
    if komut == ["ekle"] and kalan:
        ekle(" ".join(kalan), etiketler)
    elif komut == ["listele"] and not kalan and len(etiketler) <= 1:
        listele(etiketler[0] if etiketler else None)
    else:
        log.hata(KULLANIM)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(ana(sys.argv[1:]))
