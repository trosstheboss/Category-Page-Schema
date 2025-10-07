@echo off
echo ========================================
echo Category Page Schema Generator
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo Python detected:
python --version
echo.

:: Check if pandas is installed
python -c "import pandas" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo Running schema generator...
echo.

python schema_generator.py

if errorlevel 1 (
    echo.
    echo ERROR: Schema generation failed
    echo Check the error messages above
) else (
    echo.
    echo SUCCESS: Schema files generated in output/ directory
)

echo.
pause
