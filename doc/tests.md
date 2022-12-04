
# test spec:
- done: can create new db file 
- done: import the same csv twice must not be possible
- done: import the same entry into dkb-table 
    - from the same file must not be possible
    - from the different files must not be possible
- done: requesting month data must return correct values
- after csv was imported it was moved to archive and zipped
    - csv was archived in a new zip file 
    - csv was added to the existing archive
- done: new class can be added
- done: new category can be added 
- done: after csv import meta table was updated
- class can be assosiated with dkb entry

# ressources:
- test/fixtures - DB:
    - db2test.db: 
        good db with real data - used to retrieve data (test1.csv from productive imported)
    - db4test.db: 
        - good db without any data - only header
- test/fixtures - CSV:
    - test1.csv: good csv file with real data to test import
        - DE90120300001001670080 / Girokonto
        - 7 entries 
        - all from June 2016
        - all data are unique - all need to be imported
    - test2.csv: good csv, repeating 4 different entries from test1.csv
        - DE90120300001001670080 / Girokonto
        - 7 entries 
        - all from June 2016
        - 4 rows are the same as in test1
        - 2 rows are equal 
            - only 2 rows must be imported
    - test3.csv: good csv with entries all in year 2023 with different month
        - DE90120300001001670080 / Girokonto
        - 7 entries 
        - all data are unique - all need to be imported
        - all from year 2023
        - 1 x 06, 2 x 07, 2 x 08, 1 x 12, 1 x 11
    - test4.csv: good csv with entries all in month 01 from different years
        - DE90120300001001670080 / Girokonto
        - 7 entries 
        - all data are unique - all need to be imported
        - all from month January
        - year 2016 - 2021
    - move.csv: good csv with 8 entries all in month 01 from different years
