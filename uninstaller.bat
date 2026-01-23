@echo off
title Desinstalador Licitarte v1.0
color 0C

echo.
echo ========================================
echo    LICITARTE - DESINSTALADOR v1.0
echo ========================================
echo.

set "INSTALL_DIR=%PROGRAMFILES%\Licitarte"
set "DESKTOP_SHORTCUT=%USERPROFILE%\Desktop\Licitarte.lnk"

echo ADVERTENCIA: Esta accion eliminara:
echo.
echo - Aplicacion: %INSTALL_DIR%
echo - Acceso directo del escritorio
echo.
echo NOTA: La base de datos NO se eliminara
echo       (ubicada en la carpeta de instalacion)
echo.

choice /C SN /M "Desea continuar con la desinstalacion"
if errorlevel 2 goto :cancelar
if errorlevel 1 goto :desinstalar

:desinstalar
echo.
echo [1/3] Eliminando acceso directo...
if exist "%DESKTOP_SHORTCUT%" (
    del /Q "%DESKTOP_SHORTCUT%"
    echo Acceso directo eliminado
) else (
    echo No se encontro acceso directo
)

echo.
echo [2/3] Eliminando archivos de programa...
if exist "%INSTALL_DIR%" (
    rmdir /S /Q "%INSTALL_DIR%"
    echo Archivos eliminados
) else (
    echo No se encontro instalacion
)

echo.
echo [3/3] Verificando...
if not exist "%INSTALL_DIR%" (
    echo.
    echo ========================================
    echo   DESINSTALACION COMPLETADA
    echo ========================================
    echo.
    echo Licitarte ha sido desinstalado correctamente
) else (
    echo.
    echo ========================================
    echo   ERROR: No se pudo desinstalar
    echo ========================================
    echo.
    echo Intente ejecutar como administrador
)

echo.
pause
exit

:cancelar
echo.
echo Desinstalacion cancelada.
echo.
pause
exit
