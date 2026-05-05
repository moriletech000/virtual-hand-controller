@echo off
REM Quick Git Download - Opens the official Git download page

echo.
echo ========================================
echo   Downloading Git for Windows
echo ========================================
echo.
echo Opening Git download page in your browser...
echo.
echo After downloading:
echo 1. Run the installer (Git-2.xx.x-64-bit.exe)
echo 2. Click "Next" through the installation wizard
echo 3. Use the default settings (recommended)
echo 4. After installation, close and reopen Command Prompt
echo 5. Verify installation: git --version
echo 6. Run: setup_github.bat
echo.

start https://git-scm.com/download/win

echo Download page opened!
echo.
pause
