@echo off
echo Starting DFS/Props Picks App...
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the app
echo App starting at http://localhost:8000
echo Press Ctrl+C to stop
echo.
uvicorn app.main:app --reload