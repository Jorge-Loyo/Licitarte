@echo off
echo ========================================
echo   CONFIGURACION LICITARTE-POSTGRES
echo ========================================
echo.

echo Contenedor: licitarte-postgres
echo Base de datos: licitarte
echo Usuario: postgres
echo Password: licitarte123
echo Puerto interno: 5432
echo.

echo Verificando contenedor...
docker ps --filter "name=licitarte-postgres" --format "{{.Names}} - {{.Status}}"

echo.
echo Verificando puerto mapeado...
docker port licitarte-postgres

echo.
echo Verificando conexion interna...
docker exec licitarte-postgres psql -U postgres -d licitarte -c "SELECT COUNT(*) as tablas FROM information_schema.tables WHERE table_schema='public';"

echo.
echo ========================================
echo   CONFIGURACION EN .env
echo ========================================
echo DATABASE_URL=postgresql://postgres:licitarte123@localhost:5432/licitarte
echo.
echo NOTA: Si el puerto no esta mapeado, ejecuta:
echo   docker rm -f licitarte-postgres
echo   docker run -d --name licitarte-postgres -p 5432:5432 -e POSTGRES_PASSWORD=licitarte123 -e POSTGRES_DB=licitarte postgres:16
echo.
pause
