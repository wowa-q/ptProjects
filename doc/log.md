# OPL
* DKB: 
  
  * DKB should process only one csv file and add kontonummer to the meta data
  * DKB shall calculate the hash over the csv file, fetch the kontonummer and provide this to orm to be created in the meta table
* ORM
  * ORM should check if csv_df was already imported into db by checking the hash
  * ORM should create meta table and be used as ForeignKey in DKB-Table
  * Create new table for logging data
  * create more tests for ORM
* exc
  * Excel should have a GUI to associate a class with a row from DKB-Table

* Refactoring:
  * 
  * remove the DB module - not needed

# Checkout package: 
## Taipi for the GUI
  * [Taipi main](https://www.taipy.io/)
  * [Taipi Docs](https://docs.taipy.io/en/latest/)
  * [Taipi git](https://github.com/Avaiga/taipy)

## Packaging
* [packaging guideline by fedora](https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/)
* [packaging by py-pkgs.org](https://py-pkgs.org)
* [packaging by python.org](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
### Python project template
Git repository for Python project template including default configuration for Python development tools
* [Python project template](https://github.com/franneck94/Python-Project-Template)
