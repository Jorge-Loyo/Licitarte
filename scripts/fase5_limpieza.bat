@echo off
echo ========================================
echo   FASE 5: LIMPIEZA FINAL - LICITARTE
echo ========================================
echo.

echo ADVERTENCIA: Este script eliminara archivos legacy duplicados
echo.
echo Archivos a eliminar:
echo   - modules/
echo   - database/
echo   - Img/
echo   - main.py
echo   - build_exe.bat
echo   - installer.bat
echo   - uninstaller.bat
echo   - Licitarte.spec
echo   - Licitarte_v1.0_Instalador/
echo   - migrar_db.py
echo   - crear_distribucion.bat
echo   - ejecutar_migracion.bat
echo.

choice /C SN /M "Desea continuar con la limpieza"
if errorlevel 2 goto :cancelar
if errorlevel 1 goto :limpiar

:limpiar
echo.
echo [1/4] Creando backup de seguridad...
set BACKUP_DIR=data\backups\fase5_backup_%date:~-4%%date:~3,2%%date:~0,2%
mkdir %BACKUP_DIR% 2>nul

if exist modules\ xcopy /E /I /Y modules %BACKUP_DIR%\modules
if exist database\ xcopy /E /I /Y database %BACKUP_DIR%\database
if exist Img\ xcopy /E /I /Y Img %BACKUP_DIR%\Img
if exist main.py copy main.py %BACKUP_DIR%\
if exist *.bat copy *.bat %BACKUP_DIR%\
if exist Licitarte.spec copy Licitarte.spec %BACKUP_DIR%\
if exist migrar_db.py copy migrar_db.py %BACKUP_DIR%\

echo Backup creado en: %BACKUP_DIR%

echo.
echo [2/4] Eliminando carpetas legacy...
if exist modules\ rmdir /s /q modules
if exist database\ rmdir /s /q database
if exist Img\ rmdir /s /q Img
if exist Licitarte_v1.0_Instalador\ rmdir /s /q Licitarte_v1.0_Instalador

echo.
echo [3/4] Eliminando archivos legacy...
if exist main.py del /q main.py
if exist build_exe.bat del /q build_exe.bat
if exist installer.bat del /q installer.bat
if exist uninstaller.bat del /q uninstaller.bat
if exist Licitarte.spec del /q Licitarte.spec
if exist crear_distribucion.bat del /q crear_distribucion.bat
if exist ejecutar_migracion.bat del /q ejecutar_migracion.bat
if exist migrar_db.py del /q migrar_db.py

echo.
echo [4/4] Verificando limpieza...
set ERROR=0

if exist modules\ (
    echo ERROR: modules/ aun existe
    set ERROR=1
)
if exist database\ (
    echo ERROR: database/ aun existe
    set ERROR=1
)
if exist main.py (
    echo ERROR: main.py aun existe
    set ERROR=1
)

if %ERROR%==0 (
    echo.
    echo ========================================
    echo   LIMPIEZA COMPLETADA EXITOSAMENTE
    echo ========================================
    echo.
    echo Backup guardado en: %BACKUP_DIR%
    echo.
    echo Estructura final:
    echo   - web/       (Aplicacion principal)
    echo   - desktop/   (Desktop organizado)
    echo   - shared/    (Codigo compartido)
    echo   - data/      (Datos)
    echo   - docs/      (Documentacion)
    echo   - scripts/   (Scripts utilidad)
    echo.
    echo Proyecto 100%% limpio y profesional
) else (
    echo.
    echo ========================================
    echo   ERROR: Limpieza incompleta
    echo ========================================
    echo.
    echo Revise los errores arriba
)

echo.
pause
exit

:cancelar
echo.
echo Limpieza cancelada.
echo.
pause
exit
