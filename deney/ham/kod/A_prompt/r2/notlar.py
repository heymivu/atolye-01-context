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


def ekle(metin, etiket=None):
    """Yeni not ekler; tarih olarak tarih.bugun() kullanılır. Etiket isteğe bağlıdır."""
    notlar = oku()
    kayit = {"tarih": tarih.bugun(), "metin": metin}
    if etiket:
        kayit["etiket"] = etiket
    notlar.append(kayit)
    yaz(notlar)
    log.bilgi("eklendi: %s" % metin)


def listele(etiket=None):
    """Notları tarih sırasıyla yazar; etiket verilirse yalnız o etiketlileri."""
    for n in oku():
        if etiket and n.get("etiket") != etiket:
            continue
        etiket_yazi = "  [%s]" % n["etiket"] if n.get("etiket") else ""
        log.bilgi("%s  %s%s" % (n["tarih"], n["metin"], etiket_yazi))


def etiket_ayir(argumanlar):
    """--etiket DEĞER çiftini ayırır; (etiket, kalan_argümanlar) döner. Değer yoksa ValueError."""
    kalan = list(argumanlar)
    if "--etiket" not in kalan:
        return None, kalan
    i = kalan.index("--etiket")
    if i + 1 >= len(kalan):
        raise ValueError("--etiket için değer gerekli")
    etiket = kalan[i + 1]
    del kalan[i:i + 2]
    return etiket, kalan


def ana(argv):
    """Komut satırı girişi."""
    kullanim = 'kullanım: notlar.py ekle [--etiket ad] "metin" | listele [--etiket ad]'
    if not argv or argv[0] not in ("ekle", "listele"):
        log.hata(kullanim)
        return 1
    try:
        etiket, kalan = etiket_ayir(argv[1:])
    except ValueError as h:
        log.hata(str(h))
        return 1
    if argv[0] == "ekle":
        if not kalan:
            log.hata(kullanim)
            return 1
        ekle(" ".join(kalan), etiket)
    else:
        listele(etiket)
    return 0


if __name__ == "__main__":
    sys.exit(ana(sys.argv[1:]))
