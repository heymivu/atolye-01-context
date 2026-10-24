# -*- coding: utf-8 -*-
"""notlar testleri. Koş: python -m unittest notlar_test -v"""
import contextlib, io, os, unittest
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
        notlar.ana(["ekle", "--etiket", "iş", "toplantı hazırla"])
        n = notlar.oku()
        self.assertEqual(n[0]["etiket"], "iş")
        self.assertEqual(n[0]["metin"], "toplantı hazırla")

    def test_etiketsiz_ekle_etiket_alani_yok(self):
        notlar.ana(["ekle", "süt", "al"])
        n = notlar.oku()
        self.assertEqual(n[0]["metin"], "süt al")
        self.assertNotIn("etiket", n[0])

    def _listele(self, argv):
        cikti = io.StringIO()
        with contextlib.redirect_stdout(cikti):
            kod = notlar.ana(argv)
        self.assertEqual(kod, 0)
        return cikti.getvalue()

    def test_listele_etikete_gore_suzer(self):
        notlar.ana(["ekle", "--etiket", "iş", "rapor"])
        notlar.ana(["ekle", "--etiket", "ev", "çamaşır"])
        notlar.ana(["ekle", "etiketsiz"])
        cikti = self._listele(["listele", "--etiket", "iş"])
        self.assertIn("rapor", cikti)
        self.assertNotIn("çamaşır", cikti)
        self.assertNotIn("etiketsiz", cikti)

    def test_listele_etiketsiz_hepsini_gosterir(self):
        notlar.ana(["ekle", "--etiket", "iş", "rapor"])
        notlar.ana(["ekle", "etiketsiz"])
        cikti = self._listele(["listele"])
        self.assertIn("rapor", cikti)
        self.assertIn("etiketsiz", cikti)

    def test_etiket_degeri_eksikse_hata(self):
        hata = io.StringIO()
        with contextlib.redirect_stderr(hata):
            kod = notlar.ana(["ekle", "metin", "--etiket"])
        self.assertEqual(kod, 1)
        self.assertEqual(notlar.oku(), [])


if __name__ == "__main__":
    unittest.main()
