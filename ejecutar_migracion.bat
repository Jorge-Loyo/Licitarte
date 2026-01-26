@echo off
echo ========================================
echo   MIGRACION A VERSION 2.0 - LICITARTE
echo ========================================
echo.

cd database
python migrate_v2.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Intentando con 'py' en lugar de 'python'...
    py migrate_v2.py
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: No se pudo ejecutar Python
    echo Por favor verifica que Python este instalado
    echo.
)

pause
