@echo off
echo ========================================
echo   LIBERAR PUERTO 5432 Y REINICIAR
echo ========================================
echo.

echo [1/5] Identificando proceso en puerto 5432...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5432 ^| findstr LISTENING') do (
    echo Proceso encontrado: PID %%a
    echo Deteniendo proceso...
    taskkill /F /PID %%a 2>nul
)

echo.
echo [2/5] Deteniendo todos los contenedores Docker...
docker stop $(docker ps -aq) 2>nul

echo.
echo [3/5] Eliminando contenedores y volumenes antiguos...
docker-compose down -v

echo.
echo [4/5] Iniciando PostgreSQL limpio...
docker-compose up -d

echo.
echo [5/5] Esperando que PostgreSQL inicie (15 segundos)...
timeout /t 15 /nobreak

echo.
echo ========================================
echo   LISTO - Ahora ejecuta:
echo   cd web
echo   python app.py
echo ========================================
echo.
pause
