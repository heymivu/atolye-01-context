# -*- coding: utf-8 -*-
"""Ekrana yazma tek kapıdan: bilgi() stdout, hata() stderr."""
import sys


def bilgi(mesaj):
    """Bilgi satırı."""
    sys.stdout.write(mesaj + "\n")


def hata(mesaj):
    """Hata satırı."""
    sys.stderr.write("HATA: " + mesaj + "\n")
