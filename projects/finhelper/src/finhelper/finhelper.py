def calc_restschuld(kreditsumme: int, tilgungsrate: int, zinssatz:int) -> dict:
    """Die Funktion berechnet die Beträge Kredit abbezahlt und Restsumme
    Args:
        kreditsumme (int): aufgenommene Kreditsumme
        tilgungsrate (int): Prozentsatz Tilgung
        zinssatz (int): Prozensatz Kredit

    Returns:
        status (dict): Beträge {abbezahlt (int), restschuld (int)} 
    """
    # Monatliche Rate berechnen
    monatlicher_tilgungsanteil = kreditsumme * tilgungsrate / 12  # Anfangs-Tilgung pro Monat
    monatlicher_zinsanteil = kreditsumme * zinssatz / 12  # Anfangs-Zinsen pro Monat
    monatliche_rate = monatlicher_tilgungsanteil + monatlicher_zinsanteil

    # Variablen initialisieren
    restschuld = kreditsumme
    abbezahlter_betrag = 0

    # Berechnung über 12 Monate
    for _ in range(12):
        zinsanteil = restschuld * zinssatz / 12
        tilgungsanteil = monatliche_rate - zinsanteil
        restschuld -= tilgungsanteil
        abbezahlter_betrag += tilgungsanteil
    
    return {'abbezahlt':abbezahlter_betrag,
            'restschuld':restschuld
            }

def calc_tilgungstrate(kreditsumme: int, monatssrate: int, zinssatz:int) -> dict:
    """Die Funktion berechnet die Beträge Kredit abbezahlt und Restsumme
    Args:
        kreditsumme (int): aufgenommene Kreditsumme
        monatssrate (int): Monatsrate gesamt (besteht aus Tilgungsrate und Zinsrate)
        zinssatz (int): Prozensatz Kredit

    Returns:
        status (dict): Beträge {abbezahlt (int), restschuld (int)} 
    """
    result = {'tilgungsrate': 0,
              'zinsrate': 0,
              'restschuld': 0}
    result['zinsrate'] = kreditsumme * zinssatz / 12
    result['tilgungsrate'] = monatssrate - result['zinsrate']
    result['restschuld'] = kreditsumme - result['tilgungsrate']
    return result
