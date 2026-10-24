# -*- coding: utf-8 -*-
"""Tarih yardımcıları. Testler SABIT değişkeniyle sahte tarih verir."""
import datetime

SABIT = None


def bugun():
    """Bugünün tarihi, ISO biçiminde (YYYY-MM-DD). SABIT doluysa onu döner."""
    if SABIT:
        return SABIT
    return datetime.date.today().isoformat()
