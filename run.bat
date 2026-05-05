@echo off
echo Starting Virtual Mouse and Keyboard...
echo.

REM Check if virtual environment exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

echo Running application...
python main.py

pause
