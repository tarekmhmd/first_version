@echo off
echo ========================================
echo Tesseract Manual Download Guide
echo ========================================
echo.

echo The automatic download was blocked by the server.
echo Please follow these simple steps:
echo.

echo STEP 1: Download Tesseract
echo ----------------------------------------
echo.
echo Opening download page in your browser...
echo.
echo Please download this file:
echo   tesseract-ocr-w64-setup-5.3.3.20231005.exe
echo.
echo OR use this direct link:
echo   https://github.com/UB-Mannheim/tesseract/releases/download/v5.3.3/tesseract-ocr-w64-setup-5.3.3.20231005.exe
echo.

pause

echo.
echo Opening download page...
start https://github.com/UB-Mannheim/tesseract/wiki

echo.
echo ========================================
echo STEP 2: Install Tesseract
echo ========================================
echo.
echo After downloading:
echo.
echo 1. Run the downloaded file (tesseract-ocr-w64-setup-5.3.3.20231005.exe)
echo.
echo 2. When asked for installation location, choose:
echo    %CD%\tesseract
echo.
echo    (Copy this path and paste it in the installer)
echo.
echo 3. Click Install and wait
echo.
echo 4. After installation completes, come back here and press any key
echo.

pause

echo.
echo ========================================
echo STEP 3: Verify Installation
echo ========================================
echo.

if exist "tesseract\tesseract.exe" (
    echo SUCCESS! Tesseract is installed correctly!
    echo Location: %CD%\tesseract\tesseract.exe
    echo.
    echo You can now run: run.bat
    echo.
) else (
    echo Tesseract not found in project folder.
    echo.
    echo Please make sure you installed it to:
    echo %CD%\tesseract
    echo.
    echo If you installed it elsewhere, you can:
    echo 1. Move the tesseract folder here
    echo 2. Or run setup_tesseract_path.bat to add it to PATH
    echo.
)

pause
