@echo off

:: import all environment variables
call bin\CFG.bat
if ERRORLEVEL 1 goto error
color 4
:: log the used Python interpreter
echo Python used: %PYTHON_ENV% >> %LOGFILE%

:: user iterface
:userif
cls
set /p dbname=definiere Name der Datenbank (z.B.: "example.db"):
set /p year=welches Jahr? (4 Stellen, z.B.: 2021):
set /p month=welchen Monat? (1-12):
echo DB name: %dbname% >> %LOGFILE%
set OPERATION=--cmd Create-new-Month --db_name %dbname% --year %year% --month %month%
echo %OPERATION% >> %LOGFILE%
%PYTHON_ENV% %RUNNER% %OPERATION%
:: TODO: prüfen ob db erstellt worden ist
 
:: label to finish in case of an error
:error
echo "something went'wrong"

:EOF
echo Neue datenbank erstellt