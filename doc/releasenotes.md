# Release Notes - dkb module

## Release information

|Package name   |package name short     |Version   
|---------------|---                    | ----
|DKB   	        |dkb.py   	            |0.0.0   
|DB   	        |db.py   		        |0.0.0   
|fileLoader     |fileLoader.py 	        |0.0.0   

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


### DKB-Handler: CsvImporter
#### New or changed features
* `CsvImporter` defines the header of the table
* using the directory with the csv files and file loader to get the csv file list 
* `parseDkbData` using padas to parse the csv data from the list

#### Fixed issues
* 
#### Known issues and limitations
* parsing only first file from the file list
* df DataFrame is not returned (local variable)
#### Release Tests
* check the file list is not empty


### DKB-Handler: DB
#### New or changed features
* `DB` opens or creates aa sqlite3 db and creates connection to it with `createCnnection`
* `createNewTable` fix layout table is created in the db
* `close` the connection to the db 
* `save` commit changes to the db **not tested**

#### Fixed issues
*
#### Known issues and limitations
* no layout definition of table possible
* no changes to the table 
#### Release Tests
* test if new file was created
* test if connection is created
* test the table is created

## Log
* fileLoader.py:FileLoader class creates a list of the csv files, by given directory
* dkb.py:CsvImporter class to parse the dkb csv files, by using pandas 
* db.py:DB class open or create a new sqlite3 db creates connection