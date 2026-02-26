@echo off
echo ========================================
echo Installing Tesseract OCR
echo ========================================
echo.

echo Tesseract OCR is required for lab report analysis.
echo.
echo Please follow these steps:
echo.
echo 1. Download Tesseract installer from:
echo    https://github.com/UB-Mannheim/tesseract/wiki
echo.
echo 2. Download: tesseract-ocr-w64-setup-5.3.3.20231005.exe
echo    Direct link: https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe
echo.
echo 3. Run the installer
echo.
echo 4. During installation, note the installation path (usually C:\Program Files\Tesseract-OCR)
echo.
echo 5. After installation, press any key to continue...
pause
echo.

echo Opening download page in browser...
start https://github.com/UB-Mannheim/tesseract/wiki

echo.
echo After installing Tesseract, run: setup_tesseract_path.bat
echo.
pause
