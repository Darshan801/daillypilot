@echo off
echo Starting DayPilot Backend Server...
cd /d "%~dp0\..\backend"
call venv\Scripts\activate.bat
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000