
from callback import *
# text elements


# Definition of the pages
main_page_footer = f"""


<|content|>
<br/>
<br/>
The {app_name}.
"""

main_page = f"""
<|menu|lov=comming soon;comming soon|>
# {app_name}

{main_page_footer}
"""

sub_page_cfg_month = """
# Stelle den Monat ein:

<|{month}|input|label=Monat|>
<|{year}|input|label=Jahr|>
<|button|label=laden|hover_text="Lade den neuen Report"|on_action=load_report|active=True|>
"""

sub_page_cfg_db = """
# Konfiguriere den Pfad zu der Datenbank:
<|{db_path}|file_selector|id=db_selector|on_action=set_db_path|hover_text=Select path to db file|>
<|{db_path}|>
"""

sub_page_cfg_csv = """
<br/>
<br/>
### Importiere neue CSV Datei:
<|{csv_path}|file_selector|id=csv_selector|on_action=set_csv_path|hover_text=Select path to csv file|>
<|{csv_path}|>
<|button|label=import CSV|hover_text="Importiere CSV in die Datenbank"|on_action=import_csv_file|active=True|>
"""

partial_instruction_def = """
<|Show Instructions|expandable|expanded=False|partial={partial_instructions}|>
"""

page_config = f"""
<|navbar|>
{partial_instruction_def}
# Konfiguration
<|layout|columns=1 1|
   <|
{sub_page_cfg_month}
    |>
    <|
{sub_page_cfg_csv}
    |>    
|>

"""

# ----------------------------------------------------------------
sub_page_table_month = """
<|{month_table}|table|width=99%|>
"""


page_show = f"""
<|navbar|>
{partial_instruction_def}
# Anzeige
<|layout|columns=1 1|
   <|
{sub_page_table_month}
    |>
    <|
{sub_page_table_month}
    |>    
|>

"""