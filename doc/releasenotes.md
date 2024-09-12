

# Release Notes - dkb module

## Release information

|Package name           |package name short     |Version   
|---------------        |---                    | ----
|DKB   	                |dkb.py   	            |1.0.0   
|ORM   	                |orm.py   		        |1.0.0   
|fileLoader             |fileLoader.py 	        |1.0.0  
|DB_Handler             |dkb_import_test.py 	|1.0.0   

----


## Packages

|Name   	    |Version   			|Supplier           |Purpose   
|---------      |--------           |-------            |-------
|Python   		|3.9.0   	        |Python   	        |interpreter   
|Django   		|3.1.5   	        |Django   	        |Web Application 
|Pillow         |9.0.1              |?                  |image display lib
|Bootstrap   	|?			        |Layout   	        |Layout
|asciidoc   	|?			        |Eclipse/VS Code   	|ASCII Doc plugin 

----

### DKB-Handler: FileLoader
#### New or changed features
* `fileList` gives the list of the csv files in the given directory

#### Fixed issues
* 
#### Known issues and limitations
* no check if the format is the DKB csv files
#### Release Tests
* test empty list is returned if empty directory string is given
* test the list is not empty if directory with csv files is fiven


### DKB-Handler: DKB
#### New or changed features
* `DKB` 
  * defines the header of the table
  * using the directory with the csv files and file loader to get the csv file list 
  * `parseDkbData` using padas to parse the csv data from the list
  * `getMeta` to provide a dictionary with the meta data from csv

#### Fixed issues
* parsing only first file from the file list - is fixed. Whenever DKB formated csv files are found, they will be concateneted
* df DataFrame is not returned (local variable) - is fixed. Whenever DKB formated csv files are found, they will be concateneted, If only one csv file exists df will be returned directly
#### Known issues and limitations
* df will be created without checking if data exist double - no check of meta data of the file
* no id id created, which can be used in db
#### Release Tests
* check the file list is not empty


### DKB-Handler: orm.DB_Handler
#### New or changed features
* `ORM` SQLAlchemy is used to create new DB 
* `createDkbMetaTable` to create meta table of the imported csv file - **not tested**
* `importDKBDF` uses df as input and imports it into DB by pandas
* `_checkColumnExists` can check if column in table already exists (used by `addCathColumn` and `addClassColumn`)
* `addCathColumn` and `addClassColumn` to add Fereign key columns in dkb table
* created class and Cathegory tables


#### Fixed issues
*
#### Known issues and limitations
* doesn't check data which are imported - can import the same df many times
* `addNewClass` and `addNewCath` do not work - connection to database is lost check [alchemy](https://docs.sqlalchemy.org/en/14/core/pooling.html#pool-disconnects)
* `_checkColumnExists` does not provide the correct result

#### Release Tests
**not tested**


### DKB-Handler: ExcelWriter
#### New or changed features
* `ExcelWriter` 
  * activates existing Excel by given file path
  * `createSheet` create new sheet or returns if it already exists
  * `writeMeta` writes meta data into the given sheet

#### Fixed issues
* no issues known
#### Known issues and limitations
* fix cells for meta data -> overwrite in case of new write
* no write of data
#### Release Tests 
* manual tests only via excel call: r"d:\005-pj\ptPj\dkb\ptProjects\test\fixtures\haushalt.xlsm"

### ui:api 
#### New or changed features
* Command interface created
* Invoker createdd supporting `set_on_start`, `set_main_command`, `set_on_finish`
* Command classes created:
  * `CmdNewMonth`: to create new month sheet in Excel by loading data from DB
  * `CmdUpdateDbTable`: to update the table in DB from Excel _UNTESTED_
  * `CmdImportNewCsv`: to import new csv file into DB _UNTESTED_
  * `CmdCreateNewDB`: to create new DB file, with all necessary tables
  * `CmdCheckFileSystem`: to check if the file exists _UNTESTED_ is needed?
  * ``

### ui:main2
#### New or changed features
* parsing the arguments and initializing the Invoker with the right command

### Release Test
* Manual test `CmdCreateNewDB` via Excel button
* Manual test `CmdNewMonth` via Excel button - to create new sheet
  * load data not implemented yet

### ui:haushalt.xlsm
#### New or changed features
* Button `NEW DB`
* Button `Januar` etc.
* Macro to initialize `CmdCreateNewDB`
* Macro to initialize `CmdNewMonth` 

### Release Test
* Manual test `CmdCreateNewDB` via Excel button
* Manual test `CmdNewMonth` via Excel button - to create new sheet
  * load data not implemented yet



