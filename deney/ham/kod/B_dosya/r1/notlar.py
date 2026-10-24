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
    """Yeni not ekler; tarih olarak tarih.bugun() kullanılır. Etiket verilirse nota yazılır."""
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
        if n.get("etiket"):
            log.bilgi("%s  [%s] %s" % (n["tarih"], n["etiket"], n["metin"]))
        else:
            log.bilgi("%s  %s" % (n["tarih"], n["metin"]))


def etiket_ayir(argv):
    """Argümanlardan --etiket değerini ayırır; (etiket, kalan_argümanlar) döner.
    Değer eksikse (None, None) döner."""
    if "--etiket" not in argv:
        return None, list(argv)
    i = argv.index("--etiket")
    if i + 1 >= len(argv):
        return None, None
    return argv[i + 1], argv[:i] + argv[i + 2:]


def ana(argv):
    """Komut satırı girişi."""
    etiket, kalan = etiket_ayir(argv)
    if kalan is None:
        log.hata("--etiket için değer gerekli")
        return 1
    if kalan[:1] == ["ekle"] and len(kalan) >= 2:
        ekle(" ".join(kalan[1:]), etiket)
    elif kalan[:1] == ["listele"]:
        listele(etiket)
    else:
        log.hata("kullanım: notlar.py ekle [--etiket e] \"metin\" | listele [--etiket e]")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(ana(sys.argv[1:]))
