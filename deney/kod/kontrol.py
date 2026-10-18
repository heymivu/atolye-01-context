# -*- coding: utf-8 -*-
"""Kod yan deneyi kontrolü: python kontrol.py <klasör> → ihlal listesi + test sonucu.
Kurallar: 1 datetime.now/date.today doğrudan yok (tarih.py hariç) · 2 print yok · 3 test dosyası *_test.py (test_*.py yok) ·
4 İngilizce tanımlayıcı yok (def add/get/list/tag/filter/remove/delete/update/create) · 5 standart dışı import yok · testler geçiyor."""
import re, os, sys, subprocess, glob, io
STD = set(sys.stdlib_module_names)
def kontrol(k):
    ihl = []
    pys = [p for p in glob.glob(os.path.join(k, "*.py"))]
    for p in pys:
        ad = os.path.basename(p); s = io.open(p, encoding="utf-8").read()
        if ad != "tarih.py" and re.search(r"datetime\.now\(|date\.today\(|datetime\.datetime\.now|datetime\.date\.today", s): ihl.append("1 doğrudan tarih: " + ad)
        if re.search(r"^\s*print\(", s, re.M): ihl.append("2 print: " + ad)
        if ad.startswith("test_"): ihl.append("3 test adı: " + ad)
        for m in re.findall(r"^\s*def\s+([A-Za-z_]\w*)", s, re.M):
            if re.fullmatch(r"(add|get|list|tag|tags|filter|remove|delete|update|create|parse|main|show|print|run|load|save)(_\w+)?", m): ihl.append("4 İngilizce ad: %s.%s" % (ad, m))
        for m in re.findall(r"^\s*(?:import|from)\s+([A-Za-z_]\w*)", s, re.M):
            if m not in STD and m not in ("tarih", "log", "notlar"): ihl.append("5 dış bağımlılık: " + m)
    if not any(os.path.basename(p).endswith("_test.py") for p in pys): ihl.append("3 *_test.py yok")
    r = subprocess.run([sys.executable, "-I", "-m", "unittest", "discover", "-s", ".", "-p", "*_test.py"], capture_output=True, text=True, cwd=os.path.abspath(k))
    ok = "OK" in r.stderr.strip().splitlines()[-1] if r.stderr.strip() else False
    etiket = re.search(r"etiket", io.open(os.path.join(k, "notlar.py"), encoding="utf-8").read(), re.I) is not None
    return ihl, ok, etiket, r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "?"
if __name__ == "__main__":
    if sys.argv[1] == "--hepsi":
        kok = os.path.dirname(os.path.abspath(__file__))
        print("| Kol | Tekrar | İhlal | Test | Etiket var | Ayrıntı |"); print("|---|---|---|---|---|---|")
        for kol in ("A_prompt", "B_dosya", "C_ai_dosya"):
            for r in sorted(glob.glob(os.path.join(kok, kol, "r*"))):
                ihl, ok, et, son = kontrol(r)
                print("| %s | %s | %d | %s | %s | %s |" % (kol, os.path.basename(r), len(ihl), "geçti" if ok else "KALDI (%s)" % son, "evet" if et else "hayır", "; ".join(ihl)))
    else:
        print(kontrol(sys.argv[1]))
