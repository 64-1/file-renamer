@echo off
REM Get the directory of the currently executing .bat file
set scriptdir=%~dp0

REM Change directory to the location of the Python script
cd /d "%scriptdir%"

REM Run the Python script
python general_renamer.py

REM Pause to keep the command prompt window open
pause
