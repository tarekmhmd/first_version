@echo off
echo ========================================
echo Downloading Tesseract Portable
echo ========================================
echo.

echo This will download Tesseract OCR and extract it to the project folder.
echo No system installation required!
echo.

REM Create tesseract folder
if not exist "tesseract" mkdir tesseract

echo Downloading Tesseract OCR (portable version)...
echo This may take a few minutes (about 60 MB)...
echo.

REM Download using PowerShell
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe' -OutFile 'tesseract_installer.exe'}"

if exist "tesseract_installer.exe" (
    echo.
    echo Download complete!
    echo.
    echo Now installing Tesseract to project folder...
    echo.
    
    REM Install silently to project folder
    tesseract_installer.exe /S /D=%CD%\tesseract
    
    echo.
    echo Waiting for installation to complete...
    timeout /t 10 /nobreak
    
    REM Clean up installer
    del tesseract_installer.exe
    
    echo.
    echo ========================================
    echo Installation Complete!
    echo ========================================
    echo.
    echo Tesseract installed to: %CD%\tesseract
    echo.
    echo Now run: run.bat
    echo.
) else (
    echo.
    echo ERROR: Download failed!
    echo.
    echo Please check your internet connection and try again.
    echo Or download manually from:
    echo https://github.com/UB-Mannheim/tesseract/wiki
    echo.
)

pause
