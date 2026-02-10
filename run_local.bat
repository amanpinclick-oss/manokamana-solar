@echo off
echo ===================================================
echo   Manokamana Solar - Digital Growth Engine Launcher
echo ===================================================

echo [1/3] Installing necessary Python libraries...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo [2/3] Seeding initial tasks...
python orchestrator.py
python seo_agent.py
python trend_agent.py

echo [3/3] Starting the Dashboard...
echo Dashboard will be available at http://localhost:8080
echo Keep this window open to keep the engine running.
echo ===================================================
python app.py
pause
