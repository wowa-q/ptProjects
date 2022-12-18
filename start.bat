@echo off

pushd %~dp0
color 3
SET LOGFILE=bin\batch_log.txt
echo %DATE% %TIME% > %LOGFILE%
:: import all environment variables
call bin\CFG.bat
if ERRORLEVEL 1 goto error

if not exist "%RUNNER%" (
   echo "%RUNNER%" does not exist!
   goto error
)
if not exist "%LOGFILE%" (
   echo "%LOGFILE%" does not exist!
   goto error
)
if not exist "%PYTHON_ENV%" (
   echo "%PYTHON_ENV%" does not exist!
   goto error
)

:userif
:: user iterface
cls
echo Wilkommen! Das sind deine Optionen:
echo - neue Datenbank erstellen: ------------ 0
echo - neue csv importieren: ---------------- 1
echo - neue Monatsuebersicht erstellen: ----- 2
echo - Labels in die Datenbank importieren: - 3
echo - Beenden: ----------------------------- 10

set /p usercmd=Was moechtest du tun?: 
echo %TIME% >> %LOGFILE%
echo Option gewaehlt: %usercmd% >> %LOGFILE%

if %usercmd%==0 goto create_new_db
if %usercmd%==1 goto import_new_csv
if %usercmd%==2 goto create_new_month
if %usercmd%==3 goto import_label
if %usercmd%==10 goto EOF

:create_new_db
call bin/_create-new-db.bat
if ERRORLEVEL 1 goto error
goto userif

:import_new_csv
call bin/1_import-csv.bat
if ERRORLEVEL 1 goto error
goto userif

:create_new_month
call bin/2_erstelle-neuen-Monat.bat
if ERRORLEVEL 1 goto error
goto userif

:import_label
call bin/3_import-labels.bat
if ERRORLEVEL 1 goto error
goto userif



:: to jump over the error statement
goto EOF
:error
:: label to finish in case of an error
 echo "something went'wrong"
:: echo errormessage
 echo %ERRORLEVEL%

:EOF
echo - Programm beendet