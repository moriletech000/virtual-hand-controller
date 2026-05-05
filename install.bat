@echo off
echo ========================================
echo Virtual Mouse & Keyboard Installer
echo Python 3.14 Compatible
echo ========================================
echo.

echo Checking Python installation...
py --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from python.org
    pause
    exit /b 1
)

echo.
echo Creating virtual environment...
py -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing dependencies (this may take a few minutes)...
pip install -r requirements.txt

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo To run the project:
echo 1. Activate virtual environment: venv\Scripts\activate
echo 2. Run: python main.py
echo.
pause
