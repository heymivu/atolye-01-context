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
    if etiket:
        log.bilgi("eklendi [%s]: %s" % (etiket, metin))
    else:
        log.bilgi("eklendi: %s" % metin)


def listele(etiket=None):
    """Notları tarih sırasıyla yazar; etiket verilirse yalnız o etiketlileri."""
    for n in oku():
        if etiket and n.get("etiket") != etiket:
            continue
        ek = " [%s]" % n["etiket"] if n.get("etiket") else ""
        log.bilgi("%s%s  %s" % (n["tarih"], ek, n["metin"]))


def etiket_ayir(argv):
    """argv içinden --etiket DEGER çiftini ayırır; (etiket, kalan_argümanlar) döner.
    Değer eksikse ValueError fırlatır."""
    if "--etiket" not in argv:
        return None, list(argv)
    i = argv.index("--etiket")
    if i + 1 >= len(argv):
        raise ValueError("--etiket için değer gerekli")
    return argv[i + 1], argv[:i] + argv[i + 2:]


def ana(argv):
    """Komut satırı girişi."""
    try:
        etiket, kalan = etiket_ayir(argv)
    except ValueError as e:
        log.hata(str(e))
        return 1
    if len(kalan) >= 2 and kalan[0] == "ekle":
        ekle(" ".join(kalan[1:]), etiket)
    elif kalan == ["listele"]:
        listele(etiket)
    else:
        log.hata("kullanım: notlar.py ekle [--etiket ad] \"metin\" | listele [--etiket ad]")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(ana(sys.argv[1:]))
