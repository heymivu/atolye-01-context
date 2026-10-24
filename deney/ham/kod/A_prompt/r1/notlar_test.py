# -*- coding: utf-8 -*-
"""notlar testleri. Koş: python -m unittest notlar_test -v"""
import os, unittest
from unittest import mock
import notlar, tarih


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


    def test_etiketli_ekle(self):
        self.assertEqual(notlar.ana(["ekle", "--etiket", "iş", "rapor yaz"]), 0)
        n = notlar.oku()
        self.assertEqual(n[0]["etiket"], "iş")
        self.assertEqual(n[0]["metin"], "rapor yaz")

    def test_etiketsiz_ekle_eskisi_gibi(self):
        notlar.ana(["ekle", "süt", "al"])
        n = notlar.oku()
        self.assertEqual(n[0]["metin"], "süt al")
        self.assertNotIn("etiket", n[0])

    def test_listele_etikete_gore_filtreler(self):
        notlar.ana(["ekle", "--etiket", "iş", "rapor"])
        notlar.ana(["ekle", "--etiket", "ev", "süpür"])
        notlar.ana(["ekle", "etiketsiz"])
        with mock.patch("log.bilgi") as bilgi:
            notlar.ana(["listele", "--etiket", "iş"])
        satirlar = [c.args[0] for c in bilgi.call_args_list]
        self.assertEqual(len(satirlar), 1)
        self.assertIn("rapor", satirlar[0])

    def test_listele_etiketsiz_hepsini_yazar(self):
        notlar.ana(["ekle", "--etiket", "iş", "a"])
        notlar.ana(["ekle", "b"])
        with mock.patch("log.bilgi") as bilgi:
            notlar.ana(["listele"])
        self.assertEqual(bilgi.call_count, 2)

    def test_etiket_degersiz_hata(self):
        with mock.patch("log.hata"):
            self.assertEqual(notlar.ana(["listele", "--etiket"]), 1)


if __name__ == "__main__":
    unittest.main()
