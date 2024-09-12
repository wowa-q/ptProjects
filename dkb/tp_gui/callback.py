

# variables used by the GUI
db_path = 'File not selected'
csv_path = 'File not selected'
app_name = "Home Finance Manager"
month = 12
year = 2022
month_table = []
month_table = ['checksum', 
            'Datum', 
            'Debitor', 
            'Buchungstext', 
            'Verwendung',
            'Betrag',
            'Klasse',
            'Typ']

# month_table.append(__header)

# GUI callback functions
# generic callback function
def on_change(state, var_name: str, var_value):
    if var_name == "month":
        state.month = var_value
    if var_name == "year":
        state.year = var_value

def load_report(state):
    # invoke here the function to get month
    print('load_report')
    print(state.month)
    print(state.year)

def set_db_path(state):
    # invoke here a function to set path to DB file
    print('set_db_path')
    db_path=state.db_path
    print(state.db_path)

def set_csv_path(state):
    # invoke here a function to set path to CSV file
    print('set_csv_path')
    csv_path = state.csv_path
    print(state.csv_path)  

def import_csv_file(state):
    # invoke here a function to import CSV file into database
    print('import_csv_file')
    print(state.csv_path)
