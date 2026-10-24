# -*- coding: utf-8 -*-
"""notlar testleri. Koş: python -m unittest notlar_test -v"""
import io, os, unittest
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

    def _listele_cikti(self, argv):
        """ana(argv) çalıştırır; (çıkış kodu, stdout, stderr) döner."""
        cikti, hata = io.StringIO(), io.StringIO()
        with mock.patch("sys.stdout", cikti), mock.patch("sys.stderr", hata):
            kod = notlar.ana(argv)
        return kod, cikti.getvalue(), hata.getvalue()

    def test_etiketli_ekle(self):
        self.assertEqual(self._listele_cikti(["ekle", "--etiket", "iş", "rapor", "yaz"])[0], 0)
        n = notlar.oku()
        self.assertEqual(n[0]["metin"], "rapor yaz")
        self.assertEqual(n[0]["etiket"], ["iş"])

    def test_etiketsiz_ekle_alan_yok(self):
        notlar.ekle("süt al")
        self.assertNotIn("etiket", notlar.oku()[0])

    def test_listele_etikete_gore(self):
        notlar.ekle("rapor", "iş")
        notlar.ekle("süt al")
        notlar.ekle("toplantı", "iş")
        kod, cikti, _ = self._listele_cikti(["listele", "--etiket", "iş"])
        self.assertEqual(kod, 0)
        self.assertEqual(cikti, "2026-01-02  rapor\n2026-01-02  toplantı\n")

    def test_listele_etiketsiz_hepsini_verir(self):
        notlar.ekle("rapor", "iş")
        notlar.ekle("süt al")
        _, cikti, _ = self._listele_cikti(["listele"])
        self.assertEqual(cikti, "2026-01-02  rapor\n2026-01-02  süt al\n")

    def test_listele_olmayan_etiket_bos(self):
        notlar.ekle("rapor", "iş")
        kod, cikti, _ = self._listele_cikti(["listele", "--etiket", "ev"])
        self.assertEqual((kod, cikti), (0, ""))

    def test_eski_kayit_etiketsiz_listelenir(self):
        notlar.yaz([{"tarih": "2025-12-31", "metin": "eski"}])
        _, hepsi, _ = self._listele_cikti(["listele"])
        _, suzulmus, _ = self._listele_cikti(["listele", "--etiket", "iş"])
        self.assertEqual(hepsi, "2025-12-31  eski\n")
        self.assertEqual(suzulmus, "")

    def test_etiket_degersiz_hata(self):
        kod, cikti, hata = self._listele_cikti(["listele", "--etiket"])
        self.assertEqual(kod, 1)
        self.assertIn("HATA:", hata)
        self.assertEqual(cikti, "")


if __name__ == "__main__":
    unittest.main()
