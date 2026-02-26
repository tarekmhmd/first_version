@echo off
echo ========================================
echo Setting up Tesseract OCR Path
echo ========================================
echo.

echo Checking common Tesseract installation paths...
echo.

set TESSERACT_PATH=""

if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
    set TESSERACT_PATH=C:\Program Files\Tesseract-OCR
    echo Found Tesseract at: C:\Program Files\Tesseract-OCR
) else if exist "C:\Program Files (x86)\Tesseract-OCR\tesseract.exe" (
    set TESSERACT_PATH=C:\Program Files (x86)\Tesseract-OCR
    echo Found Tesseract at: C:\Program Files (x86)\Tesseract-OCR
) else (
    echo Tesseract not found in common locations.
    echo.
    echo Please enter the full path where Tesseract is installed:
    echo Example: C:\Program Files\Tesseract-OCR
    echo.
    set /p TESSERACT_PATH="Enter path: "
)

echo.
echo Adding Tesseract to system PATH...
echo.

REM Add to user PATH
setx PATH "%PATH%;%TESSERACT_PATH%"

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Tesseract path added to system PATH.
echo.
echo IMPORTANT: You need to RESTART the command prompt for changes to take effect.
echo.
echo After restarting:
echo 1. Close this window
echo 2. Open a NEW command prompt
echo 3. Run: run.bat
echo.
pause
