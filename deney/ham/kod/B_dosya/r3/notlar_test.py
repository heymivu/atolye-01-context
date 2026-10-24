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

    def _listele_ciktisi(self, argv):
        """ana(argv) çağrısında log.bilgi'ye giden satırları döner."""
        with mock.patch("log.bilgi") as bilgi:
            kod = notlar.ana(argv)
        self.assertEqual(kod, 0)
        return [c.args[0] for c in bilgi.call_args_list]

    def test_etiketli_ekle(self):
        with mock.patch("log.bilgi"):
            notlar.ana(["ekle", "--etiket", "iş", "rapor yaz"])
        n = notlar.oku()
        self.assertEqual(n[0]["etiket"], "iş")
        self.assertEqual(n[0]["metin"], "rapor yaz")

    def test_etiketli_listele_filtreler(self):
        with mock.patch("log.bilgi"):
            notlar.ana(["ekle", "--etiket", "iş", "rapor yaz"])
            notlar.ana(["ekle", "süt al"])
            notlar.ana(["ekle", "--etiket", "ev", "çamaşır"])
        satirlar = self._listele_ciktisi(["listele", "--etiket", "iş"])
        self.assertEqual(len(satirlar), 1)
        self.assertIn("rapor yaz", satirlar[0])

    def test_etiketsiz_listele_hepsini_gosterir(self):
        with mock.patch("log.bilgi"):
            notlar.ana(["ekle", "--etiket", "iş", "rapor yaz"])
            notlar.ana(["ekle", "süt al"])
        satirlar = self._listele_ciktisi(["listele"])
        self.assertEqual(len(satirlar), 2)

    def test_etiketsiz_ekle_eskisi_gibi(self):
        with mock.patch("log.bilgi"):
            notlar.ana(["ekle", "süt", "al"])
        n = notlar.oku()
        self.assertEqual(n[0], {"tarih": "2026-01-02", "metin": "süt al"})

    def test_etiket_degersiz_hata(self):
        with mock.patch("log.hata"):
            self.assertEqual(notlar.ana(["listele", "--etiket"]), 1)


if __name__ == "__main__":
    unittest.main()
