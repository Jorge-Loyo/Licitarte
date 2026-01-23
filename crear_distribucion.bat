@echo off
echo ========================================
echo   LICITARTE - DISTRIBUCION COMPLETA
echo ========================================
echo.

echo [1/5] Limpiando archivos anteriores...
rmdir /s /q dist 2>nul
rmdir /s /q build 2>nul
rmdir /s /q Licitarte_v1.0_Instalador 2>nul

echo.
echo [2/5] Instalando PyInstaller...
pip install pyinstaller

echo.
echo [3/5] Generando ejecutable...
pyinstaller --clean Licitarte.spec

echo.
echo [4/5] Creando carpeta de distribucion...
mkdir Licitarte_v1.0_Instalador
copy dist\Licitarte.exe Licitarte_v1.0_Instalador\
xcopy /E /I /Y Img Licitarte_v1.0_Instalador\Img
copy installer.bat Licitarte_v1.0_Instalador\
copy uninstaller.bat Licitarte_v1.0_Instalador\
copy LEEME.txt Licitarte_v1.0_Instalador\
copy MANUAL_USUARIO.md Licitarte_v1.0_Instalador\

echo.
echo [5/5] Verificando resultado...
if exist "Licitarte_v1.0_Instalador\Licitarte.exe" (
    echo.
    echo ========================================
    echo   EXITO: Distribucion lista
    echo   Carpeta: Licitarte_v1.0_Instalador
    echo ========================================
    echo.
    echo Contenido:
    dir Licitarte_v1.0_Instalador
    echo.
    echo SIGUIENTE PASO:
    echo Comprimir "Licitarte_v1.0_Instalador" en ZIP
    echo para distribuir
) else (
    echo.
    echo ========================================
    echo   ERROR: No se pudo crear la distribucion
    echo ========================================
)

echo.
pause
