# OPL
## General
- [ ] Define how the tool shall be used
- [ ] Define how the excel shall look like (create a template?)
- [ ] Test month import manually

## DB Tables
- [ ] dkb-table should have the account per entry
- [ ] dkb-table should have ForeignKey to the meta data
- [ ] when retriving the month data ForeignKeys, csv-meta, classes and category shall be exported
- [ ] Create new table for logging data

## Excel
- [ ] The imported table should have a filter
- [ ] Excel should have a GUI to associate a class with a row from DKB-Table
- [ ] Define ranges for meta data, month data: Date of first entry and last entry
- [ ] Implement column finder 
- [ ] `write_month` shall use data input and validate it and not use hard coded columns


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
