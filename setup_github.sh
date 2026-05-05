#!/bin/bash

# GitHub Repository Setup Script
# This script will help you create and push to a new GitHub repository

echo "🚀 GitHub Repository Setup"
echo "=========================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

echo "✅ Git is installed"
echo ""

# Get repository name
read -p "Enter repository name (e.g., virtual-hand-controller): " REPO_NAME

if [ -z "$REPO_NAME" ]; then
    echo "❌ Repository name cannot be empty"
    exit 1
fi

# Get GitHub username
read -p "Enter your GitHub username: " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ GitHub username cannot be empty"
    exit 1
fi

echo ""
echo "📝 Repository Details:"
echo "   Name: $REPO_NAME"
echo "   Username: $GITHUB_USERNAME"
echo "   URL: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo ""

read -p "Continue? (y/n): " CONFIRM

if [ "$CONFIRM" != "y" ]; then
    echo "❌ Setup cancelled"
    exit 0
fi

echo ""
echo "🔧 Setting up repository..."

# Replace README_PUBLIC.md with README.md
if [ -f "README_PUBLIC.md" ]; then
    echo "📄 Replacing README.md with public version..."
    cp README_PUBLIC.md README.md
fi

# Initialize git repository
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
else
    echo "✅ Git repository already initialized"
fi

# Add all files (respecting .gitignore)
echo "📁 Adding files..."
git add .

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: Virtual Hand Controller with modern UI

Features:
- Virtual mouse control with hand gestures
- Virtual keyboard with hover-to-type
- Extreme detection (0.1 threshold) for easy hand detection
- Modern UI with professional design
- Works with either hand (left or right)
- ~60 FPS performance
- Automatic image enhancement"

# Add remote
echo "🔗 Adding remote repository..."
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

# Set main branch
echo "🌿 Setting main branch..."
git branch -M main

echo ""
echo "✅ Local setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Go to https://github.com/new"
echo "2. Create a new repository named: $REPO_NAME"
echo "3. Make it PUBLIC"
echo "4. Do NOT initialize with README, .gitignore, or license"
echo "5. After creating the repository, run:"
echo ""
echo "   git push -u origin main"
echo ""
echo "🎉 Your repository will be live at:"
echo "   https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo ""
