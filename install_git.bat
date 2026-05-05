@echo off
REM Git Installation Helper for Windows
REM This script will help you install Git

echo.
echo ========================================
echo   Git Installation Helper
echo ========================================
echo.

REM Check if Git is already installed
git --version >nul 2>&1
if not errorlevel 1 (
    echo [OK] Git is already installed!
    git --version
    echo.
    echo You can now run: setup_github.bat
    pause
    exit /b 0
)

echo Git is not installed on your system.
echo.
echo ========================================
echo   Installation Options
echo ========================================
echo.
echo 1. Download Git from official website (Recommended)
echo 2. Install using winget (Windows 10/11)
echo 3. View manual installation instructions
echo 4. Exit
echo.

set /p CHOICE="Enter your choice (1-4): "

if "%CHOICE%"=="1" goto DOWNLOAD
if "%CHOICE%"=="2" goto WINGET
if "%CHOICE%"=="3" goto MANUAL
if "%CHOICE%"=="4" goto EXIT

echo Invalid choice. Please try again.
pause
exit /b 1

:DOWNLOAD
echo.
echo ========================================
echo   Opening Git Download Page
echo ========================================
echo.
echo Opening https://git-scm.com/download/win in your browser...
echo.
echo After downloading:
echo 1. Run the installer (Git-2.xx.x-64-bit.exe)
echo 2. Click "Next" through the wizard (use default settings)
echo 3. After installation, close and reopen this window
echo 4. Run this script again to verify installation
echo.
start https://git-scm.com/download/win
pause
exit /b 0

:WINGET
echo.
echo ========================================
echo   Installing Git using winget
echo ========================================
echo.
echo Checking if winget is available...
winget --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: winget is not available on your system.
    echo Please use Option 1 to download Git manually.
    pause
    exit /b 1
)

echo Installing Git...
winget install --id Git.Git -e --source winget

echo.
echo Installation complete!
echo Please close and reopen this window, then run:
echo    git --version
echo.
pause
exit /b 0

:MANUAL
echo.
echo ========================================
echo   Manual Installation Instructions
echo ========================================
echo.
echo Windows:
echo 1. Go to: https://git-scm.com/download/win
echo 2. Download the installer
echo 3. Run the installer as Administrator
echo 4. Use default settings
echo 5. After installation, open a NEW Command Prompt
echo 6. Verify with: git --version
echo.
echo Alternative - Using Chocolatey:
echo    choco install git
echo.
echo Alternative - Using Winget:
echo    winget install --id Git.Git -e --source winget
echo.
echo For detailed instructions, see: INSTALL_GIT.md
echo.
pause
exit /b 0

:EXIT
echo.
echo Exiting...
exit /b 0
