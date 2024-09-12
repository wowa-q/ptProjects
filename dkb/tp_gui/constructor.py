from taipy import Gui

import pages 
from callback import *

instructions = """
# Anleitung 
## Importieren neuer CSV Datei
* Wechsle in "KONFIGURATIO" Tab
* Selektiere CSV Datei
* Drücke Import Knopf
## Monat auswählen
* Tippe Monat von 1-12 ein
* Tippe Jahr ein z.B. 2022 ein
"""

pages = {
     "/": pages.main_page,
     "Konfiguration": pages.page_config,
     "Anzeige": pages.page_show
   }

gui=Gui(pages=pages)
partial_instructions = gui.add_partial(instructions)
gui.run(dark_mode=False, port=8080)