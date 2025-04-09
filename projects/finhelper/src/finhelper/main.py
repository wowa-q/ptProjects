def calc_tax(income):
    """Rechnet welchen Betrag man an Steuern zahlen muss.
    Ja, die offiziellen Formeln zur Berechnung der Einkommensteuer in Deutschland sind im Einkommensteuergesetz (§ 32a EStG) festgelegt. 
    Für das Jahr 2025 gelten gemäß § 32a EStG die folgenden Berechnungsvorschriften:

1. **Grundfreibetrag**:  
   Für ein zu versteuerndes Einkommen bis 12.096 Euro fällt keine Einkommensteuer an.

2. **Erste Progressionszone** (12.097 € bis 17.443 €):  
   In diesem Bereich steigt der Steuersatz von 14% auf 24%. Die Einkommensteuer \( E \) wird mit der Formel berechnet:

   \[   E = (1.015,13 \cdot y + 1.400) \cdot y   \]

   Dabei ist \( y = \frac{zvE - 12.096}{10.000} \), wobei \( zvE \) das zu versteuernde Einkommen in Euro ist.

3. **Zweite Progressionszone** (17.444 € bis 68.480 €):  
   Hier steigt der Steuersatz weiter von 24% auf 42%. Die Einkommensteuer \( E \) wird mit der Formel berechnet:

   \[   E = (180,69 \cdot z + 2.239) \cdot z + 965,58   \]

   Dabei ist \( z = \frac{zvE - 17.443}{10.000} \).

4. **Dritte Zone** (68.481 € bis 277.825 €):  
   In diesem Bereich beträgt der Steuersatz konstant 42%. Die Einkommensteuer \( E \) berechnet sich wie folgt:

   \[   E = 0,42 \cdot zvE - 9.136,63   \]

5. **Vierte Zone** (ab 277.826 €):  
   Für Einkommen oberhalb von 277.825 Euro beträgt der Steuersatz 45%. Die Einkommensteuer \( E \) wird berechnet durch:

   \[   E = 0,45 \cdot zvE - 17.571,38   \]

Diese Formeln ermöglichen eine genaue Berechnung der Einkommensteuer basierend auf dem zu versteuernden Einkommen. Für detaillierte Informationen und Beispiele können Sie § 32a EStG direkt einsehen. citeturn0search6 

    Args:
        income (float): Einkommen

    Returns:
        float: Zu zahlender Betrag an Steuern
    """
    TAXRANGE = {
        'Stufe1': [0, 12096],
        'Stufe2': [12097, 17443],
        'Stufe3': [17444, 68480],
        'Stufe4': [68481, 277825],
        'Stufe5': [277826, 999999999]
    }

    if income <= TAXRANGE['Stufe1'][1]:  # Einkommen unterhalb des Grundfreibetrags
        return 0
    
    elif income <= TAXRANGE['Stufe2'][1]:  # Erste Progressionszone
        y = (income - TAXRANGE['Stufe1'][1]) / 10_000
        tax = (1_015.13 * y + 1_400) * y
        return tax
    
    elif income <= TAXRANGE['Stufe3'][1]:  # Zweite Progressionszone
        z = (income - TAXRANGE['Stufe2'][1]) / 10_000
        tax = (180.69 * z + 2.239) * z + 965.58
        return tax
    
    elif income <= TAXRANGE['Stufe4'][1]:  # Dritte Steuerstufe (42 %)
        tax = 0.42 * income - 9_136.63
        return tax
    
    else:  # Vierte Steuerstufe (45 %)
        tax = 0.45 * income - 17_571.38
        return tax


if __name__ == '__main__':
    print('Stufe2: 13.000€', calc_tax(13000))
    print('Stufe3: 20.000€', calc_tax(20000))
    print('Stufe4: 80.000€', calc_tax(80000))
    print('Stufe4: 141.727,98€', calc_tax(141_727.98))
    print('Stufe5: 300.000', calc_tax(300000))
