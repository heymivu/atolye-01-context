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

    def _listele_cikti(self, etiket=None):
        satirlar = []
        eski = log.bilgi
        log.bilgi = satirlar.append
        try:
            notlar.listele(etiket)
        finally:
            log.bilgi = eski
        return satirlar

    def test_etiketli_ekle(self):
        notlar.ekle("rapor yaz", "iş")
        notlar.ekle("süt al")
        n = notlar.oku()
        self.assertEqual(n[0]["etiket"], "iş")
        self.assertNotIn("etiket", n[1])

    def test_listele_etikete_gore(self):
        notlar.ekle("rapor yaz", "iş")
        notlar.ekle("süt al")
        notlar.ekle("toplantı", "iş")
        self.assertEqual(len(self._listele_cikti("iş")), 2)
        self.assertEqual(len(self._listele_cikti("yok")), 0)

    def test_listele_etiketsiz_hepsini_verir(self):
        notlar.ekle("rapor yaz", "iş")
        notlar.ekle("süt al")
        self.assertEqual(len(self._listele_cikti()), 2)

    def test_komut_satiri_etiket(self):
        self.assertEqual(notlar.ana(["ekle", "--etiket", "iş", "rapor", "yaz"]), 0)
        self.assertEqual(notlar.oku()[0]["etiket"], "iş")
        self.assertEqual(notlar.oku()[0]["metin"], "rapor yaz")
        self.assertEqual(notlar.ana(["listele", "--etiket", "iş"]), 0)
        self.assertEqual(notlar.ana(["ekle", "x", "--etiket"]), 1)


if __name__ == "__main__":
    unittest.main()
