@echo off



echo %DATE% %TIME% >> %LOGFILE%
SET PYTHON_ENV=C:\Users\wakl8754\Miniconda3\envs\genericEnv\python.exe
echo "Python configured: " %PYTHON_ENV% >> %LOGFILE%


SET PROJECT_MAIN=%CD%
echo "PROJECT_MAIN configured: " %PROJECT_MAIN% >> %LOGFILE%

::SET PROJECT_MAIN=%~dp0 >> %LOGFILE%
::echo "PROJECT_MAIN configured: " %PROJECT_MAIN% >> %LOGFILE%

popd
SET RUNNER=%PROJECT_MAIN%\runner.py
echo "RUNNER configured: " %RUNNER% >> %LOGFILE%




:EOF
:: label to finish configuration
echo - configuration completed
