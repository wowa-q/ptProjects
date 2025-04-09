from unittest import result
import pytest

from . import finhelper

kreditsumme = 100000
monatsrate = 580.98
zinssatz = 2.05 #% (170.83)
abbezahlt = 410.15
rest = 99580.85
"""
-580,98 € (100.000€)
-683,33 € (250.000€)
-259,00 € (60.000€)
"""

@pytest.mark.parametrize("kreditsumme, monatsrate, zinssatz, tilgungsrate, zinsrate", [
    (100000, 580.98, 0.0205, 410.15, 170.83),
])
def test_tilgungsrate(kreditsumme, monatsrate, zinssatz, tilgungsrate, zinsrate):
    result = finhelper.calc_tilgungstrate(kreditsumme, monatsrate, zinssatz)
    trate = result.get('tilgungsrate')
    zrate = result.get('zinsrate')
    neu = result.get('restschuld')
    kredit_neu = kreditsumme - trate
    assert kredit_neu == neu, f"ist: {kredit_neu} / soll: {neu}"
    assert zrate == zinsrate, f"ist: {zrate} / soll: {zinsrate}"
    assert trate == tilgungsrate, f"ist: {trate} / soll: {tilgungsrate}"


@pytest.mark.skip()
@pytest.mark.parametrize("kreditsumme, tilgungsrate, zinssatz, abbezahlt, rest", [
    (100000, 0.02, 0.0205, 410.15, 99580.85 ),
])
def test_basic(kreditsumme, tilgungsrate, zinssatz, abbezahlt, rest):
    result = finhelper.calc_restschuld(kreditsumme,tilgungsrate,zinssatz)

    assert isinstance(result, dict), f"Return type not as expected" 
    assert result.get('abbezahlt') == abbezahlt, f"{result.get('abbezahlt')}"
    assert result.get('restschuld') == rest, f"{result.get('restschuld')}"