# -*- coding: utf-8 -*-
"""notlar testleri. Koş: python -m unittest notlar_test -v"""
import os, unittest
import notlar, tarih, log


class NotlarTesti(unittest.TestCase):
    def setUp(self):
        notlar.DOSYA = os.path.join(os.path.dirname(__file__), "_test_notlar.json")
        if os.path.exists(notlar.DOSYA):
            os.remove(notlar.DOSYA)
        tarih.SABIT = "2026-01-02"

    def tearDown(self):
        if os.path.exists(notlar.DOSYA):
            os.remove(notlar.DOSYA)
        tarih.SABIT = None

    def test_ekle_ve_oku(self):
        notlar.ekle("süt al")
        n = notlar.oku()
        self.assertEqual(len(n), 1)
        self.assertEqual(n[0]["tarih"], "2026-01-02")
        self.assertEqual(n[0]["metin"], "süt al")

    def _listele_ciktisi(self, argv):
        satirlar = []
        eski = log.bilgi
        log.bilgi = satirlar.append
        try:
            self.assertEqual(notlar.ana(argv), 0)
        finally:
            log.bilgi = eski
        return satirlar

    def test_etiketli_ekle(self):
        eski = log.bilgi
        log.bilgi = lambda m: None
        try:
            notlar.ana(["ekle", "--etiket", "iş", "rapor", "yaz"])
            notlar.ana(["ekle", "süt al"])
        finally:
            log.bilgi = eski
        n = notlar.oku()
        self.assertEqual(n[0]["etiket"], "iş")
        self.assertEqual(n[0]["metin"], "rapor yaz")
        self.assertNotIn("etiket", n[1])

    def test_etiketle_listele(self):
        eski = log.bilgi
        log.bilgi = lambda m: None
        try:
            notlar.ana(["ekle", "--etiket", "iş", "rapor"])
            notlar.ana(["ekle", "--etiket", "ev", "süpür"])
            notlar.ana(["ekle", "etiketsiz"])
        finally:
            log.bilgi = eski
        cikti = self._listele_ciktisi(["listele", "--etiket", "iş"])
        self.assertEqual(len(cikti), 1)
        self.assertIn("rapor", cikti[0])

    def test_etiketsiz_listele_hepsini_verir(self):
        eski = log.bilgi
        log.bilgi = lambda m: None
        try:
            notlar.ana(["ekle", "--etiket", "iş", "rapor"])
            notlar.ana(["ekle", "etiketsiz"])
        finally:
            log.bilgi = eski
        self.assertEqual(len(self._listele_ciktisi(["listele"])), 2)

    def test_etiket_degeri_eksik(self):
        eski = log.hata
        log.hata = lambda m: None
        try:
            self.assertEqual(notlar.ana(["listele", "--etiket"]), 1)
        finally:
            log.hata = eski


if __name__ == "__main__":
    unittest.main()
