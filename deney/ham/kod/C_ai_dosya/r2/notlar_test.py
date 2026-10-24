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

    def _calistir(self, *argv):
        """ana() çağırır; (çıkış kodu, stdout, stderr) döner."""
        cikti, hata = io.StringIO(), io.StringIO()
        with mock.patch("sys.stdout", cikti), mock.patch("sys.stderr", hata):
            kod = notlar.ana(list(argv))
        return kod, cikti.getvalue(), hata.getvalue()

    def test_etiketli_ekle(self):
        kod, _, _ = self._calistir("ekle", "--etiket", "iş", "toplantı", "notu")
        self.assertEqual(kod, 0)
        n = notlar.oku()
        self.assertEqual(n[0]["metin"], "toplantı notu")
        self.assertEqual(n[0]["etiket"], ["iş"])

    def test_etiketsiz_ekle_eski_gibi(self):
        self._calistir("ekle", "süt al")
        self.assertEqual(notlar.oku()[0], {"tarih": "2026-01-02", "metin": "süt al"})

    def test_listele_etikete_gore_suzer(self):
        self._calistir("ekle", "--etiket", "iş", "rapor yaz")
        self._calistir("ekle", "--etiket", "ev", "süt al")
        self._calistir("ekle", "etiketsiz not")
        kod, cikti, _ = self._calistir("listele", "--etiket", "iş")
        self.assertEqual(kod, 0)
        self.assertEqual(cikti, "2026-01-02  rapor yaz\n")

    def test_listele_etiketsiz_hepsini_yazar(self):
        self._calistir("ekle", "--etiket", "iş", "a")
        self._calistir("ekle", "b")
        _, cikti, _ = self._calistir("listele")
        self.assertEqual(cikti, "2026-01-02  a\n2026-01-02  b\n")

    def test_eski_kayitta_etiket_alani_yok(self):
        notlar.yaz([{"tarih": "2025-12-31", "metin": "eski not"}])
        _, cikti, _ = self._calistir("listele", "--etiket", "iş")
        self.assertEqual(cikti, "")
        _, cikti, _ = self._calistir("listele")
        self.assertEqual(cikti, "2025-12-31  eski not\n")

    def test_listele_olmayan_etiket_bos(self):
        self._calistir("ekle", "--etiket", "iş", "a")
        kod, cikti, _ = self._calistir("listele", "--etiket", "yok")
        self.assertEqual((kod, cikti), (0, ""))

    def test_birden_cok_etiket(self):
        self._calistir("ekle", "--etiket", "iş", "--etiket", "acil", "x")
        self.assertEqual(notlar.oku()[0]["etiket"], ["iş", "acil"])
        _, cikti, _ = self._calistir("listele", "--etiket", "acil")
        self.assertEqual(cikti, "2026-01-02  x\n")

    def test_etiket_degeri_eksik_hata(self):
        kod, _, hata = self._calistir("ekle", "metin", "--etiket")
        self.assertEqual(kod, 1)
        self.assertIn("HATA", hata)
        kod, _, hata = self._calistir("listele", "--etiket")
        self.assertEqual(kod, 1)
        self.assertFalse(os.path.exists(notlar.DOSYA))

    def test_etiketli_ekle_metinsiz_hata(self):
        kod, _, _ = self._calistir("ekle", "--etiket", "iş")
        self.assertEqual(kod, 1)
        self.assertFalse(os.path.exists(notlar.DOSYA))

    def test_listele_fazla_arguman_hata(self):
        kod, _, _ = self._calistir("listele", "fazla")
        self.assertEqual(kod, 1)


if __name__ == "__main__":
    unittest.main()
