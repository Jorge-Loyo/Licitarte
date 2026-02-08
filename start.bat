@echo off
echo Verificando PostgreSQL Docker...

docker ps | findstr licitarte-postgres >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: PostgreSQL Docker no esta corriendo
    echo.
    echo Inicia el contenedor con:
    echo   docker start licitarte-postgres
    echo.
    echo O inicia docker-compose:
    echo   docker-compose up -d
    echo.
    pause
    exit /b 1
)

echo PostgreSQL OK - Iniciando aplicacion...
cd web
python app.py
