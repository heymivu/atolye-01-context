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


def ekle(metin, etiketler=None):
    """Yeni not ekler; tarih olarak tarih.bugun() kullanılır. Etiket isteğe bağlıdır."""
    notlar = oku()
    kayit = {"tarih": tarih.bugun(), "metin": metin}
    if etiketler:
        kayit["etiket"] = list(etiketler)
    notlar.append(kayit)
    yaz(notlar)
    log.bilgi("eklendi: %s" % metin)


def listele(etiket=None):
    """Notları tarih sırasıyla yazar; etiket verilirse yalnız o etiketlileri."""
    for n in oku():
        if etiket and etiket not in n.get("etiket", []):
            continue
        log.bilgi("%s  %s" % (n["tarih"], n["metin"]))


def ayikla(argv):
    """argv içinden --etiket değerlerini ayırır; (kalan, etiketler) döner.
    --etiket'ten sonra değer yoksa None döner."""
    kalan, etiketler = [], []
    i = 0
    while i < len(argv):
        if argv[i] == "--etiket":
            if i + 1 >= len(argv):
                return None
            etiketler.append(argv[i + 1])
            i += 2
        else:
            kalan.append(argv[i])
            i += 1
    return kalan, etiketler


def ana(argv):
    """Komut satırı girişi."""
    ayrik = ayikla(argv)
    if ayrik is not None:
        kalan, etiketler = ayrik
        if len(kalan) >= 2 and kalan[0] == "ekle":
            ekle(" ".join(kalan[1:]), etiketler)
            return 0
        if kalan == ["listele"] and len(etiketler) <= 1:
            listele(etiketler[0] if etiketler else None)
            return 0
    log.hata("kullanım: notlar.py ekle [--etiket e] \"metin\" | listele [--etiket e]")
    return 1


if __name__ == "__main__":
    sys.exit(ana(sys.argv[1:]))
