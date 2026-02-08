@echo off
echo ========================================
echo   REINICIAR POSTGRESQL DOCKER
echo ========================================
echo.

echo [1/3] Deteniendo contenedor...
docker-compose down -v

echo.
echo [2/3] Eliminando volumen antiguo...
docker volume rm licitarte_postgres_data 2>nul

echo.
echo [3/3] Iniciando contenedor limpio...
docker-compose up -d

echo.
echo Esperando que PostgreSQL inicie (10 segundos)...
timeout /t 10 /nobreak

echo.
echo ========================================
echo   POSTGRESQL REINICIADO
echo ========================================
echo.
echo Credenciales:
echo   Host: localhost:5432
echo   Usuario: licitarte
echo   Password: licitarte123
echo   Base de datos: licitarte_db
echo.
echo Ahora ejecuta:
echo   cd web
echo   python app.py
echo.
pause
