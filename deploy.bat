@echo off
echo ===================================================
echo   Manokamana Solar - Website Deployment Tool
echo ===================================================

echo [1/3] Preparing local files...
git init
git add .
git commit -m "Initial website launch"

echo.
echo [2/3] Connecting to GitHub...
set /p repo_url="Paste your GitHub Repository URL (e.g., https://github.com/yourname/solar-website.git): "

:: Try to remove old connection if it exists, then add new one
git remote remove origin >nul 2>&1
git remote add origin %repo_url%
git branch -M main

echo.
echo [3/3] Uploading files (Force Push)...
echo (You may be asked to sign in to GitHub in a popup window)
git push -u origin main --force

echo.
echo ===================================================
echo   Done! Your files are now on GitHub (Force Updated).
echo   Please check the "Actions" tab on your GitHub page.
echo ===================================================
pause
