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
    """Yeni not ekler; tarih olarak tarih.bugun() kullanılır. Etiket varsa nota yazılır."""
    notlar = oku()
    not_ = {"tarih": tarih.bugun(), "metin": metin}
    if etiket:
        not_["etiket"] = etiket
    notlar.append(not_)
    yaz(notlar)
    log.bilgi("eklendi: %s" % metin)


def listele(etiket=None):
    """Notları tarih sırasıyla yazar; etiket verilirse yalnız o etiketlileri."""
    for n in oku():
        if etiket and n.get("etiket") != etiket:
            continue
        log.bilgi("%s  %s" % (n["tarih"], n["metin"]))


def etiket_ayir(argv):
    """argv içinden --etiket DEĞER çiftini ayırır; (etiket, kalan_argümanlar) döner."""
    kalan = list(argv)
    if "--etiket" in kalan:
        i = kalan.index("--etiket")
        if i + 1 >= len(kalan):
            return None, None
        etiket = kalan[i + 1]
        del kalan[i:i + 2]
        return etiket, kalan
    return None, kalan


def ana(argv):
    """Komut satırı girişi."""
    etiket, kalan = etiket_ayir(argv)
    if kalan is None:
        log.hata("--etiket için değer gerekli")
        return 1
    if len(kalan) >= 2 and kalan[0] == "ekle":
        ekle(" ".join(kalan[1:]), etiket)
    elif kalan[:1] == ["listele"]:
        listele(etiket)
    else:
        log.hata("kullanım: notlar.py ekle [--etiket e] \"metin\" | listele [--etiket e]")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(ana(sys.argv[1:]))
