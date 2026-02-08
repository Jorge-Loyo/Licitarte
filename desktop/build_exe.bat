@echo off
echo ========================================
echo   LICITARTE - Generador de Ejecutable
echo ========================================
echo.

echo [1/4] Instalando PyInstaller...
pip install pyinstaller

echo.
echo [2/4] Limpiando archivos anteriores...
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build

echo.
echo [3/4] Generando ejecutable...
pyinstaller --clean Licitarte.spec

echo.
echo [4/4] Verificando resultado...
if exist "dist\Licitarte.exe" (
    echo.
    echo ========================================
    echo   EXITO: Ejecutable creado
    echo   Ubicacion: dist\Licitarte.exe
    echo ========================================
    echo.
    echo Para distribuir, comprime la carpeta "dist" completa
) else (
    echo.
    echo ========================================
    echo   ERROR: No se pudo crear el ejecutable
    echo ========================================
)

echo.
pause
