# 📥 Git Installation Guide

Git is not currently installed on your system. Here's how to install it:

---

## 🪟 Windows Installation (Recommended)

### Option 1: Download and Install (Easiest)

1. **Download Git:**
   - Go to: https://git-scm.com/download/win
   - The download should start automatically
   - Or click "Click here to download manually"

2. **Run the Installer:**
   - Double-click the downloaded file (Git-2.xx.x-64-bit.exe)
   - Click "Next" through the installation wizard
   - **Important settings:**
     - ✅ Use recommended default settings
     - ✅ Select "Git from the command line and also from 3rd-party software"
     - ✅ Use bundled OpenSSH
     - ✅ Use the OpenSSL library
     - ✅ Checkout Windows-style, commit Unix-style line endings
     - ✅ Use MinTTY
     - ✅ Default (fast-forward or merge)

3. **Verify Installation:**
   - Open a NEW Command Prompt or PowerShell
   - Run: `git --version`
   - You should see: `git version 2.xx.x`

### Option 2: Using Winget (Windows Package Manager)

If you have Windows 10/11 with winget:

```powershell
winget install --id Git.Git -e --source winget
```

### Option 3: Using Chocolatey

If you have Chocolatey installed:

```powershell
choco install git
```

---

## 🐧 Linux Installation

### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install git
```

### Fedora:
```bash
sudo dnf install git
```

### Arch Linux:
```bash
sudo pacman -S git
```

---

## 🍎 macOS Installation

### Option 1: Using Homebrew (Recommended)
```bash
brew install git
```

### Option 2: Using Xcode Command Line Tools
```bash
xcode-select --install
```

### Option 3: Download Installer
- Go to: https://git-scm.com/download/mac
- Download and run the installer

---

## ✅ Verify Installation

After installation, open a NEW terminal/command prompt and run:

```bash
git --version
```

You should see something like:
```
git version 2.43.0
```

---

## 🔧 Configure Git (First Time Setup)

After installing Git, configure your identity:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Verify configuration:
```bash
git config --list
```

---

## 🚀 After Installation

Once Git is installed, you can:

1. **Run the setup script:**
   ```bash
   # Windows:
   setup_github.bat
   
   # Linux/Mac:
   ./setup_github.sh
   ```

2. **Or manually set up the repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

---

## 🆘 Troubleshooting

### "git: command not found" after installation
- **Windows:** Close and reopen Command Prompt/PowerShell
- **Linux/Mac:** Run `source ~/.bashrc` or open a new terminal

### Installation fails
- **Windows:** Run installer as Administrator (right-click → Run as administrator)
- **Linux:** Make sure you have sudo privileges
- **macOS:** Install Xcode Command Line Tools first

### Git is slow on Windows
- This is normal for the first run
- Subsequent operations will be faster

---

## 📚 Learn Git Basics

After installation, you might want to learn Git basics:
- Official Git Tutorial: https://git-scm.com/docs/gittutorial
- GitHub Git Handbook: https://guides.github.com/introduction/git-handbook/
- Interactive Tutorial: https://learngitbranching.js.org/

---

## 🎯 Quick Reference

Common Git commands you'll use:

```bash
git init                    # Initialize repository
git add .                   # Stage all files
git commit -m "message"     # Commit changes
git push                    # Push to remote
git pull                    # Pull from remote
git status                  # Check status
git log                     # View history
```

---

## ✨ Next Steps

After installing Git:

1. ✅ Verify installation: `git --version`
2. ✅ Configure Git with your name and email
3. ✅ Run `setup_github.bat` to set up your repository
4. ✅ Create repository on GitHub
5. ✅ Push your code!

---

**Need help? The setup scripts will guide you through the process!**
