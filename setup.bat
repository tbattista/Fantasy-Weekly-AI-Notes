@echo off
echo ========================================
echo DFS/Props Picks App - Windows Setup
echo ========================================
echo.

echo Step 1: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment created
echo.

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated
echo.

echo Step 3: Upgrading pip...
python -m pip install --upgrade pip
echo ✓ Pip upgraded
echo.

echo Step 4: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To run the app:
echo   1. Make sure virtual environment is activated: venv\Scripts\activate
echo   2. Run: uvicorn app.main:app --reload
echo   3. Open: http://localhost:8000
echo.
echo Press any key to start the app now...
pause >nul

echo.
echo Starting the app...
uvicorn app.main:app --reload