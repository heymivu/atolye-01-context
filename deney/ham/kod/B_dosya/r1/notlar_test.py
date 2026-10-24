# -*- coding: utf-8 -*-
"""notlar testleri. Koş: python -m unittest notlar_test -v"""
import io, os, unittest
from contextlib import redirect_stdout
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

    def _listele_cikti(self, etiket=None):
        cikti = io.StringIO()
        with redirect_stdout(cikti):
            notlar.listele(etiket)
        return cikti.getvalue()

    def test_etiketli_ekle(self):
        notlar.ekle("rapor yaz", "iş")
        notlar.ekle("süt al")
        n = notlar.oku()
        self.assertEqual(n[0]["etiket"], "iş")
        self.assertNotIn("etiket", n[1])

    def test_listele_etikete_gore_filtreler(self):
        notlar.ekle("rapor yaz", "iş")
        notlar.ekle("süt al", "ev")
        notlar.ekle("etiketsiz")
        cikti = self._listele_cikti("iş")
        self.assertIn("rapor yaz", cikti)
        self.assertNotIn("süt al", cikti)
        self.assertNotIn("etiketsiz", cikti)

    def test_listele_etiketsiz_hepsini_yazar(self):
        notlar.ekle("rapor yaz", "iş")
        notlar.ekle("etiketsiz")
        cikti = self._listele_cikti()
        self.assertIn("rapor yaz", cikti)
        self.assertIn("etiketsiz", cikti)

    def test_ana_komut_satiri_etiketli(self):
        self.assertEqual(notlar.ana(["ekle", "--etiket", "iş", "toplantı", "notu"]), 0)
        self.assertEqual(notlar.ana(["ekle", "serbest"]), 0)
        n = notlar.oku()
        self.assertEqual(n[0]["metin"], "toplantı notu")
        self.assertEqual(n[0]["etiket"], "iş")
        cikti = io.StringIO()
        with redirect_stdout(cikti):
            self.assertEqual(notlar.ana(["listele", "--etiket", "iş"]), 0)
        self.assertIn("toplantı notu", cikti.getvalue())
        self.assertNotIn("serbest", cikti.getvalue())

    def test_etiket_degeri_eksikse_hata(self):
        self.assertEqual(notlar.ana(["listele", "--etiket"]), 1)


if __name__ == "__main__":
    unittest.main()
