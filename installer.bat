@echo off
title Instalador Licitarte v1.0
color 0B

echo.
echo ========================================
echo      LICITARTE - INSTALADOR v1.0
echo   Gestion de Licitaciones Farmaceuticas
echo ========================================
echo.

set "INSTALL_DIR=%PROGRAMFILES%\Licitarte"

echo Ubicacion de instalacion:
echo %INSTALL_DIR%
echo.

choice /C SN /M "Desea continuar con la instalacion"
if errorlevel 2 goto :cancelar
if errorlevel 1 goto :instalar

:instalar
echo.
echo [1/3] Creando directorio de instalacion...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo [2/3] Copiando archivos...
xcopy /E /I /Y "Licitarte.exe" "%INSTALL_DIR%\"
xcopy /E /I /Y "_internal" "%INSTALL_DIR%\_internal"
if exist "Img" xcopy /E /I /Y "Img" "%INSTALL_DIR%\Img"

echo [3/3] Creando acceso directo en el escritorio...
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Licitarte.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\Licitarte.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'Licitarte - Gestion de Licitaciones'; $Shortcut.Save()"

echo.
echo [4/4] Copiando desinstalador...
copy uninstaller.bat "%INSTALL_DIR%\"

echo.
echo ========================================
echo   INSTALACION COMPLETADA
echo ========================================
echo.
echo Acceso directo creado en el escritorio
echo.
echo Para desinstalar:
echo Ejecute: %INSTALL_DIR%\uninstaller.bat
echo (como administrador)
echo.
pause
exit

:cancelar
echo.
echo Instalacion cancelada.
echo.
pause
exit
