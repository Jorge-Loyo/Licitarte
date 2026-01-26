@echo off
echo ========================================
echo   CONFIGURACION POSTGRESQL LOCAL
echo ========================================
echo.

echo 1. Iniciando PostgreSQL en Docker...
docker-compose up -d

echo.
echo 2. Esperando que PostgreSQL este listo...
timeout /t 5 /nobreak > nul

echo.
echo 3. Ejecutando migraciones...
cd database
py migrate_v2.py
py migrate_catalogos.py
py migrate_organismos.py

echo.
echo ========================================
echo   CONFIGURACION COMPLETADA
echo ========================================
echo.
echo PostgreSQL corriendo en: localhost:5432
echo Base de datos: licitarte_db
echo Usuario: licitarte
echo Password: licitarte123
echo.
echo Para iniciar la aplicacion:
echo   cd web
echo   py app.py
echo.
pause
