# Directory 
* [pathlib](https://docs.python.org/3/library/pathlib.html )
* [import error: ModuleNotFound](https://towardsdatascience.com/how-to-fix-modulenotfounderror-and-importerror-248ce5b69b1c)
# DB 
* [sqlite3-tutorial](https://www.sqlitetutorial.net/)
* [pandas-docu](https://pandas.pydata.org/pandas-docs/stable/reference/frame.html)
* [pandas-csv](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html)
* [pandas-sqlite3-fullstack](https://www.fullstackpython.com/blog/export-pandas-dataframes-sqlite-sqlalchemy.html)
* [pandas-sqlite3](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html)
* [sqllite browser](https://sqlitebrowser.org/about/)
* [ORM: SQL Alchemy](https://www.sqlalchemy.org/)
* [SQLAlchemy tutotial](https://docs.sqlalchemy.org/en/13/core/tutorial.html)

get the table related by a foreign key
- `employees`: table name
- `employee_dept`: column Foreign Kex

`list(employees.columns.employee_dept.foreign_keys)[0].column.table`

get the "key" of a column, which defaults to its name, but can be any user-defined string:
`employees.columns.employee_name.key`

# Pandas Excel
* [pandas-excel](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#excel-files)
* [convert to excel](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_excel.html#pandas.DataFrame.to_excel)
  ```
  DataFrame.to_excel(excel_writer, sheet_name='Sheet1', na_rep='', float_format=None, columns=None, header=True, index=True, index_label=None, startrow=0, startcol=0, engine=None, merge_cells=True, encoding=None, inf_rep='inf', verbose=True, freeze_panes=None, storage_options=None)
  ```

>`freeze_panes`: tuple of int (length 2), optional
Specifies the one-based bottommost row and rightmost column that is to be frozen.

If you wish to write to more than one sheet in the workbook, it is necessary to specify an ExcelWriter object:

```
df2 = df1.copy()
with pd.ExcelWriter('output.xlsx') as writer:  
    df1.to_excel(writer, sheet_name='Sheet_name_1')
    df2.to_excel(writer, sheet_name='Sheet_name_2')
```

# Excel libs
## xlwings
[xlwings quickstart](https://docs.xlwings.org/en/stable/quickstart.html) 
[xlwings API](https://docs.xlwings.org/en/stable/api.html)
### in nutshell
```
import xlwings as xw

wb = xw.Book()  # opens a new workbook
wb = xw.Book("FileName.xlsx") # connect to a file
wb = xw.Book(r'C:\path\to\file.xlsx') # with the full path
sheet = wb.sheets['sheet name']
sheet.range("A1")
sheet.range("A1:C3")
sheet.range((1,1))
sheet.range((1,1), (3,3))
sheet.range("NamedRange")
# Or using index/slice notation
sheet["A1"]
sheet["A1:C3"]
sheet[0, 0]
sheet[0:4, 0:4]
sheet["NamedRange"]
```

## openpyxl
[openpyxl](https://openpyxl.readthedocs.io/en/stable/)
```
from openpyxl import Workbook
wb = Workbook()
```
grab the active worksheet
```
ws = wb.active
```
Data can be assigned directly to cells
```
ws['A1'] = 42
```
Rows can also be appended
```
ws.append([1, 2, 3])
```
Python types will automatically be converted
```
import datetime

ws['A2'] = datetime.datetime.now()
```

Save the file
```
wb.save("sample.xlsx")
```