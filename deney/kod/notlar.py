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


def ekle(metin):
    """Yeni not ekler; tarih olarak tarih.bugun() kullanılır."""
    notlar = oku()
    notlar.append({"tarih": tarih.bugun(), "metin": metin})
    yaz(notlar)
    log.bilgi("eklendi: %s" % metin)


def listele():
    """Tüm notları tarih sırasıyla yazar."""
    for n in oku():
        log.bilgi("%s  %s" % (n["tarih"], n["metin"]))


def ana(argv):
    """Komut satırı girişi."""
    if len(argv) >= 2 and argv[0] == "ekle":
        ekle(" ".join(argv[1:]))
    elif argv[:1] == ["listele"]:
        listele()
    else:
        log.hata("kullanım: notlar.py ekle \"metin\" | listele")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(ana(sys.argv[1:]))
