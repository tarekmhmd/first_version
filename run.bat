@echo off
echo ========================================
echo Medical AI Assistant - Starting...
echo ========================================
echo.

if not exist "venv" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo Starting Flask server...
echo Application will be available at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python backend\app.py
pause
