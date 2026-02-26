@echo off
echo ========================================
echo Tesseract OCR Setup
echo ========================================
echo.

REM Check if Tesseract already exists in project
if exist "tesseract\tesseract.exe" (
    echo Tesseract already installed in project folder!
    echo Location: %CD%\tesseract
    echo.
    echo Ready to use! Run: run.bat
    echo.
    pause
    exit /b 0
)

echo Tesseract OCR is required for lab report analysis.
echo.
echo Choose installation method:
echo.
echo 1. Download to project folder (Recommended - No admin rights needed)
echo 2. Install system-wide (Requires admin rights)
echo 3. Skip (Use demo mode)
echo.

set /p choice="Enter choice (1, 2, or 3): "

if "%choice%"=="1" goto portable
if "%choice%"=="2" goto systemwide
if "%choice%"=="3" goto skip

:portable
echo.
echo ========================================
echo Downloading Tesseract (Portable)
echo ========================================
echo.

REM Create tesseract folder
mkdir tesseract 2>nul

echo Downloading Tesseract OCR...
echo Size: ~60 MB, this may take a few minutes...
echo.

REM Try GitHub release (more reliable)
echo Trying GitHub mirror...
powershell -Command "& {Write-Host 'Downloading from GitHub...' -ForegroundColor Yellow; [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $ProgressPreference = 'SilentlyContinue'; try { Invoke-WebRequest -Uri 'https://github.com/UB-Mannheim/tesseract/releases/download/v5.3.3/tesseract-ocr-w64-setup-5.3.3.20231005.exe' -OutFile 'tesseract_installer.exe' -UserAgent 'Mozilla/5.0'; Write-Host 'Download complete!' -ForegroundColor Green } catch { Write-Host 'GitHub download failed, trying alternative...' -ForegroundColor Red }}"

REM If GitHub failed, try original source
if not exist "tesseract_installer.exe" (
    echo.
    echo Trying original source...
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $ProgressPreference = 'SilentlyContinue'; try { Invoke-WebRequest -Uri 'https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe' -OutFile 'tesseract_installer.exe' -UserAgent 'Mozilla/5.0'; Write-Host 'Download complete!' -ForegroundColor Green } catch { Write-Host 'Download failed!' -ForegroundColor Red }}"
)

if exist "tesseract_installer.exe" (
    echo.
    echo Installing to project folder...
    echo.
    
    REM Install silently to project folder
    start /wait tesseract_installer.exe /S /D=%CD%\tesseract
    
    REM Wait a bit for installation
    timeout /t 5 /nobreak >nul
    
    REM Clean up installer
    del tesseract_installer.exe
    
    if exist "tesseract\tesseract.exe" (
        echo.
        echo ========================================
        echo Installation Successful!
        echo ========================================
        echo.
        echo Tesseract installed to: %CD%\tesseract
        echo.
        echo Ready to use! Run: run.bat
        echo.
    ) else (
        echo.
        echo Installation may still be in progress...
        echo Please wait a moment and check if tesseract\tesseract.exe exists.
        echo.
    )
) else (
    echo.
    echo ========================================
    echo Automatic Download Failed
    echo ========================================
    echo.
    echo The server blocked automatic download.
    echo.
    echo SOLUTION: Manual Download (Easy!)
    echo.
    echo Please run: download_tesseract_manual.bat
    echo.
    echo It will:
    echo 1. Open the download page in your browser
    echo 2. Guide you through manual installation
    echo 3. Takes only 2 minutes!
    echo.
    echo OR you can download directly from:
    echo https://github.com/UB-Mannheim/tesseract/releases
    echo.
)
goto end

:systemwide
echo.
echo Opening download page in browser...
echo.
echo Please:
echo 1. Download the installer
echo 2. Run it with administrator rights
echo 3. Note the installation path
echo 4. Run setup_tesseract_path.bat after installation
echo.
start https://github.com/UB-Mannheim/tesseract/wiki
goto end

:skip
echo.
echo Skipping Tesseract installation.
echo.
echo The application will run in DEMO MODE:
echo - Skin analysis: Works 100%%
echo - Chatbot: Works 100%%
echo - Sound analysis: Works 100%%
echo - Lab analysis: Uses demo data (not real OCR)
echo.
echo To enable full functionality later, run this script again.
echo.
goto end

:end
pause
