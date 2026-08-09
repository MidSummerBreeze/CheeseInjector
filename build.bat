@echo off
setlocal enabledelayedexpansion

:: Set variables
set "ENTRY_POINT=main.py"
set "OUTPUT_EXE=CheeseInjector.exe"
set "OUTPUT_DIR=dist"
set "BUILD_DIR=build"

if not exist "%ENTRY_POINT%" (
    echo Entry point '%ENTRY_POINT%' not found in current directory.
    exit /b 1
)

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in system PATH.
    exit /b 1
)

python -c "import nuitka" >nul 2>&1
if %errorlevel% neq 0 (
    echo Nuitka not found. Attempting to install...
    python -m pip install nuitka
    if !errorlevel! neq 0 (
        echo Failed to install Nuitka. Please check your pip environment.
        exit /b 1
    )
)

if not exist "core\injector.ps1" (
    echo Missing 'core\injector.ps1'. Cannot build without injection script.
    exit /b 1
)

echo Cleaning previous build artifacts...
if exist "%OUTPUT_DIR%" rmdir /s /q "%OUTPUT_DIR%"
if exist "%BUILD_DIR%" rmdir /s /q "%BUILD_DIR%"
if exist "%ENTRY_POINT:~0,-3%.build" rmdir /s /q "%ENTRY_POINT:~0,-3%.build"
if exist "%ENTRY_POINT:~0,-3%.dist" rmdir /s /q "%ENTRY_POINT:~0,-3%.dist"

echo Starting compilation process...
python -m nuitka ^
    --onefile ^
    --windows-console-mode=disable ^
    --enable-plugin=pyqt5 ^
    --include-data-file="core\injector.ps1=core\injector.ps1" ^
    --output-dir=%OUTPUT_DIR% ^
    --output-filename=%OUTPUT_EXE% ^
    %ENTRY_POINT%

if %errorlevel% neq 0 (
    echo Build failed with exit code %errorlevel%.
    exit /b %errorlevel%
)

if not exist "%OUTPUT_DIR%\%OUTPUT_EXE%" (
    echo Build finished but executable not found in '%OUTPUT_DIR%'.
    exit /b 1
)

echo Build completed. Executable: %OUTPUT_DIR%\%OUTPUT_EXE%
exit /b 0