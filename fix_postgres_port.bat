@echo off
echo ========================================
echo   MAPEAR PUERTO LICITARTE-POSTGRES
echo ========================================
echo.

echo [1/5] Haciendo backup de la base de datos...
docker exec licitarte-postgres pg_dump -U postgres licitarte > backup_licitarte.sql
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: No se pudo hacer backup
    pause
    exit /b 1
)
echo Backup creado: backup_licitarte.sql

echo.
echo [2/5] Deteniendo contenedor actual...
docker stop licitarte-postgres

echo.
echo [3/5] Eliminando contenedor (los datos estan en backup)...
docker rm licitarte-postgres

echo.
echo [4/5] Creando nuevo contenedor con puerto mapeado...
docker run -d --name licitarte-postgres -p 5432:5432 -e POSTGRES_PASSWORD=licitarte123 -e POSTGRES_DB=licitarte postgres:16

echo.
echo [5/5] Esperando que PostgreSQL inicie (10 segundos)...
ping 127.0.0.1 -n 11 > nul

echo.
echo Restaurando backup...
docker exec -i licitarte-postgres psql -U postgres licitarte < backup_licitarte.sql

echo.
echo ========================================
echo   COMPLETADO
echo ========================================
echo.
echo Contenedor licitarte-postgres recreado con puerto 5432 mapeado
echo Base de datos restaurada desde backup
echo.
echo Configuracion en .env:
echo DATABASE_URL=postgresql://postgres:licitarte123@localhost:5432/licitarte
echo.
echo Ahora ejecuta:
echo   cd web
echo   py app.py
echo.
pause
