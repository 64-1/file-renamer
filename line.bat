@echo off

REM Detect the location of the batch file
set script_dir=%~dp0

REM Detect the location of python.exe
for /f "tokens=* delims=" %%i in ('where python') do set python_path=%%i

REM Prompt user for thickness value
set /p thickness=Enter thickness value (0-255): 

REM Run the Python script with the user-provided thickness value
"%python_path%" "%script_dir%genshin_set_outlines.py" --thickness %thickness%

pause
