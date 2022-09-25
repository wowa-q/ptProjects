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

#### Fixed issues
*
#### Known issues and limitations
* doesn't check data which are imported - can import the same df many times

#### Release Tests
**not tested**

## OPL
* DKB should read the meta data
* DKB should check if data are already created by using metadata
* ORM should check if csv_df was already imported into db
* ORM should create meta table and be used as ForeignKey in DKB-Table
* create more tests for ORM
* ORM create table with clases and be used as ForeignKey in DKB-Table
* DKB shall invoke the ORM directly (not to be done by user) **?**
* remove the DB module - not needed