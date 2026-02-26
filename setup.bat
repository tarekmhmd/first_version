@echo off
echo ========================================
echo Medical AI Assistant - Setup
echo ========================================
echo.

echo [1/5] Checking Python version...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed!
    pause
    exit /b 1
)
echo.

echo [2/5] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created successfully!
) else (
    echo Virtual environment already exists.
)
echo.

echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo [4/5] Installing required packages...
pip install --upgrade pip
pip install -r requirements.txt
echo.

echo [5/5] Setting up database and downloading models...
python backend\setup_project.py
echo.

echo [6/6] Setting up Tesseract OCR (optional)...
echo.
if not exist "tesseract\tesseract.exe" (
    echo Tesseract OCR is needed for lab report analysis.
    echo.
    set /p install_tesseract="Do you want to install Tesseract now? (y/n): "
    if /i "%install_tesseract%"=="y" (
        call setup_tesseract.bat
    ) else (
        echo.
        echo Skipping Tesseract installation.
        echo You can install it later by running: setup_tesseract.bat
        echo.
    )
) else (
    echo Tesseract already installed in project folder!
)
echo.

echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To run the application, execute: run.bat
echo.
pause
