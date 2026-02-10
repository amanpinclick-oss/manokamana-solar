@echo off
echo ===================================================
echo   Manokamana Solar - Website Deployment Tool
echo ===================================================

echo [1/3] Initializing local Git...
git init
git add .
git commit -m "Initial website launch"

echo.
echo [2/3] Connecting to GitHub...
set /p repo_url="Paste your GitHub Repository URL (e.g., https://github.com/yourname/solar-website.git): "

git remote add origin %repo_url%
git branch -M main

echo.
echo [3/3] Uploading files...
echo (You may be asked to sign in to GitHub in a popup window)
git push -u origin main

echo.
echo ===================================================
echo   Done! Your files are now on GitHub.
echo   I will now tell you how to turn on the website link.
echo ===================================================
pause
