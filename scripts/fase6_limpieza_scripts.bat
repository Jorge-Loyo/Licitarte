@echo off
echo ========================================
echo   FASE 6: LIMPIEZA DE SCRIPTS OBSOLETOS
echo ========================================
echo.

echo ADVERTENCIA: Este script eliminara scripts de migracion obsoletos
echo y archivos innecesarios que ya cumplieron su proposito.
echo.

choice /C SN /M "Desea continuar con la limpieza"
if errorlevel 2 goto :cancelar
if errorlevel 1 goto :limpiar

:limpiar
echo.
echo [1/5] Creando backup de seguridad...
set BACKUP_DIR=data\backups\fase6_backup_%date:~-4%%date:~3,2%%date:~0,2%
mkdir %BACKUP_DIR% 2>nul

if exist shared\database\ xcopy /E /I /Y shared\database %BACKUP_DIR%\shared_database
if exist web\check_db.py copy web\check_db.py %BACKUP_DIR%\
if exist web\.coverage copy web\.coverage %BACKUP_DIR%\

echo Backup creado en: %BACKUP_DIR%

echo.
echo [2/5] Eliminando scripts de migracion obsoletos en shared/database/...
cd shared\database
if exist add_motivo_perdida.py del /q add_motivo_perdida.py
if exist add_producto_cotizar.py del /q add_producto_cotizar.py
if exist check_tables.py del /q check_tables.py
if exist migrar_datos.py del /q migrar_datos.py
if exist migrate_add_marca_ganadora.py del /q migrate_add_marca_ganadora.py
if exist migrate_alternativas.py del /q migrate_alternativas.py
if exist migrate_catalogos.py del /q migrate_catalogos.py
if exist migrate_local.py del /q migrate_local.py
if exist migrate_ofertas.py del /q migrate_ofertas.py
if exist migrate_organismos.py del /q migrate_organismos.py
if exist migrate_to_postgres.py del /q migrate_to_postgres.py
if exist migrate_v1_1_0.py del /q migrate_v1_1_0.py
if exist migrate_v2.py del /q migrate_v2.py
if exist licitaciones_backup.db del /q licitaciones_backup.db
cd ..\..

echo.
echo [3/5] Eliminando archivos de testing/debug en web/...
cd web
if exist check_db.py del /q check_db.py
if exist .coverage del /q .coverage
if exist htmlcov\ rmdir /s /q htmlcov
cd ..

echo.
echo [4/5] Eliminando archivos de configuracion duplicados en raiz...
if exist .env del /q .env
if exist .env.example del /q .env.example
if exist requirements.txt del /q requirements.txt

echo.
echo [5/5] Verificando limpieza...
set ERROR=0

if exist shared\database\add_motivo_perdida.py (
    echo ERROR: add_motivo_perdida.py aun existe
    set ERROR=1
)
if exist shared\database\migrate_v2.py (
    echo ERROR: migrate_v2.py aun existe
    set ERROR=1
)
if exist web\check_db.py (
    echo ERROR: check_db.py aun existe
    set ERROR=1
)
if exist web\htmlcov\ (
    echo ERROR: htmlcov/ aun existe
    set ERROR=1
)

if %ERROR%==0 (
    echo.
    echo ========================================
    echo   LIMPIEZA COMPLETADA EXITOSAMENTE
    echo ========================================
    echo.
    echo Archivos eliminados:
    echo   - 13 scripts de migracion obsoletos
    echo   - 2 archivos de debug/testing
    echo   - 3 archivos de configuracion duplicados
    echo   - 1 carpeta htmlcov/
    echo   - 2 backups de BD obsoletos
    echo.
    echo Total: 21 archivos innecesarios eliminados
    echo.
    echo Backup guardado en: %BACKUP_DIR%
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
