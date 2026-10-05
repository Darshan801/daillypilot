@echo off
echo Running DayPilot Tests...

echo.
echo === Backend Tests ===
cd /d "%~dp0\..\backend"
call venv\Scripts\activate.bat
python -m pytest -v

echo.
echo === Frontend Tests ===
cd /d "%~dp0\..\frontend"
npm test -- --watchAll=false --passWithNoTests