@echo off
REM GitHub Repository Setup Script for Windows
REM This script will help you create and push to a new GitHub repository

echo.
echo ========================================
echo   GitHub Repository Setup
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed. Please install Git first.
    echo Download from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [OK] Git is installed
echo.

REM Get repository name
set /p REPO_NAME="Enter repository name (e.g., virtual-hand-controller): "

if "%REPO_NAME%"=="" (
    echo ERROR: Repository name cannot be empty
    pause
    exit /b 1
)

REM Get GitHub username
set /p GITHUB_USERNAME="Enter your GitHub username: "

if "%GITHUB_USERNAME%"=="" (
    echo ERROR: GitHub username cannot be empty
    pause
    exit /b 1
)

echo.
echo Repository Details:
echo    Name: %REPO_NAME%
echo    Username: %GITHUB_USERNAME%
echo    URL: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
echo.

set /p CONFIRM="Continue? (y/n): "

if /i not "%CONFIRM%"=="y" (
    echo Setup cancelled
    pause
    exit /b 0
)

echo.
echo Setting up repository...
echo.

REM Replace README_PUBLIC.md with README.md
if exist "README_PUBLIC.md" (
    echo [1/6] Replacing README.md with public version...
    copy /y README_PUBLIC.md README.md >nul
) else (
    echo [1/6] README_PUBLIC.md not found, skipping...
)

REM Initialize git repository
if not exist ".git" (
    echo [2/6] Initializing git repository...
    git init
) else (
    echo [2/6] Git repository already initialized
)

REM Add all files
echo [3/6] Adding files...
git add .

REM Create initial commit
echo [4/6] Creating initial commit...
git commit -m "Initial commit: Virtual Hand Controller with modern UI" -m "Features:" -m "- Virtual mouse control with hand gestures" -m "- Virtual keyboard with hover-to-type" -m "- Extreme detection (0.1 threshold) for easy hand detection" -m "- Modern UI with professional design" -m "- Works with either hand (left or right)" -m "- ~60 FPS performance" -m "- Automatic image enhancement"

REM Add remote
echo [5/6] Adding remote repository...
git remote remove origin >nul 2>&1
git remote add origin "https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git"

REM Set main branch
echo [6/6] Setting main branch...
git branch -M main

echo.
echo ========================================
echo   Local setup complete!
echo ========================================
echo.
echo Next steps:
echo 1. Go to https://github.com/new
echo 2. Create a new repository named: %REPO_NAME%
echo 3. Make it PUBLIC
echo 4. Do NOT initialize with README, .gitignore, or license
echo 5. After creating the repository, run:
echo.
echo    git push -u origin main
echo.
echo Your repository will be live at:
echo    https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
echo.
echo ========================================
echo.
pause
